from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from flask import Flask,request,jsonify, current_app
from utils import IndexUtils, DataType
from globals import global_chatbots, project_session, chat_history
from chatbot import ChatBot
import os
import requests




service_ns = Namespace('service',description="File management")

query_model = service_ns.model('Query', {
    'project_name': fields.String(required=True, description='Focus Project Name'),
    'session_id': fields.String(required=True, description='Remain the talk in the same session'),
    'query': fields.String(required=True, description='query string from customer'),
})

@service_ns.route("/query")
class Query(Resource):
    @service_ns.expect(query_model)
    @jwt_required()
    def post(self):
        data = request.get_json()

        project_name = data.get('project_name')
        session_id = data.get('session_id')
        query = data.get('query')
        query_origin = query

        if query != "":
            url = "https://api.deepl.com/v2/translate"
            headers = {
                "Authorization": "DeepL-Auth-Key 2334a9ef-4325-44a5-be9c-362a30a0dc8b"
            }
            data = {
                "text": f"{query}",
                "target_lang": "EN"
            }

            query_translate = requests.post(url, headers=headers, data=data)

            query = query_translate.json()["translations"][0]["text"]

        if project_name is None or session_id is None or query is None: 
            return jsonify({'error': 'No project name in the request'}), 400

        project_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], project_name)

        if session_id not in global_chatbots.keys():
            # Make sure the project directory exists
            if not os.path.exists(project_dir):
                os.makedirs(project_dir)

            indexUtils = IndexUtils(current_app.config["INDEX_SAVE_PATH"],project_name)

            # Read all files in the project directory
            index_set = {}
            for data_type in DataType:
                if data_type == DataType.DOCX:
                    docx_dir = os.path.join(project_dir, "docx")
                    if not os.path.exists(docx_dir):
                        os.makedirs(docx_dir)
                    doc_pathes = os.listdir(docx_dir) 
                    doc_pathes = [os.path.join(project_dir, "docx", doc_path) for doc_path in doc_pathes]
                    index_set.update(indexUtils.dataLoader(doc_pathes, data_type))
                elif data_type == DataType.PDF:
                    pdf_dir = os.path.join(project_dir, "pdf")
                    if not os.path.exists(pdf_dir):
                        os.makedirs(pdf_dir)
                    pdf_pathes = os.listdir(pdf_dir)
                    pdf_pathes = [os.path.join(project_dir, "pdf", pdf_path) for pdf_path in pdf_pathes]
                    index_set.update(indexUtils.dataLoader(pdf_pathes, data_type))
                elif data_type == DataType.HTML:
                    html_dir = os.path.join(project_dir, "html")
                    if not os.path.exists(html_dir):
                        os.makedirs(html_dir)
                    html_pathes = os.listdir(os.path.join(project_dir, "html"))
                    html_pathes = [os.path.join(project_dir, "html", html_path) for html_path in html_pathes]
                    index_set.update(indexUtils.dataLoader(html_pathes, data_type))
                elif data_type == DataType.AUDIO:
                    audio_dir = os.path.join(project_dir, "audio") # mp3, m4a
                    if not os.path.exists(audio_dir):
                        os.makedirs(audio_dir)
                    audio_pathes = os.listdir(audio_dir)
                    audio_pathes = [os.path.join(project_dir, "audio", audio_path) for audio_path in audio_pathes]
                    index_set.update(indexUtils.dataLoader(audio_pathes, data_type))
            print("Index set: ", index_set)
            chatbot = ChatBot(index_set,None,project_name=project_name)
            global_chatbots[session_id] = chatbot
            if project_name not in project_session.keys():
                project_session[project_name] = [session_id]
            else:
                project_session[project_name].append(session_id)
        chatbot = global_chatbots[session_id]
        response = chatbot.run(query)
        print("Response: ", response)
        # return response

        result = ""
        if response != "":
            url = "https://api.deepl.com/v2/translate"
            headers = {
                "Authorization": "DeepL-Auth-Key 2334a9ef-4325-44a5-be9c-362a30a0dc8b"
            }
            data = {
                "text": f"{response}",
                "target_lang": "ZH"
            }

            response = requests.post(url, headers=headers, data=data)
            print(response.json())

            result = response.json()["translations"][0]["text"]
        else:
            result =  response
        
        record = {"query":query_origin, "response":result} 
        if session_id not in chat_history.keys():
            chat_history[session_id] = [record]
        else:
            chat_history[session_id].append(record)
        
        return result

@service_ns.route("/sessions/<string:project_name>")
@service_ns.param('project_name', 'Project name')
class Sessions(Resource):
    @jwt_required()
    def get(self, project_name):
        if project_name not in project_session.keys():
            return {'error': 'Project name not found'}, 404

        session_ids = project_session[project_name]
        return {'sessions': session_ids}

@service_ns.route("/chat_history/<string:session_id>")
class ChatHistory(Resource):
    @jwt_required()
    def get(self, session_id):
        if session_id not in chat_history.keys():
            return jsonify({'error': 'Session ID not found'}), 404
        history = chat_history[session_id]
        # serialize response as JSON only if it's a string
        history_serialized = [{'query': r['query'], 'response': r['response']} 
                              for r in history if isinstance(r['response'], str)]

        print(chat_history)
        return {'chat_history': history_serialized}