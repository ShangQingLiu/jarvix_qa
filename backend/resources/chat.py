from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from flask import Flask,request,jsonify, current_app
from utils import IndexUtils, DataType
from globals import global_chatbots
from chatbot import ChatBot
import os


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
        chatbot = global_chatbots[session_id]
        response = chatbot.run(query)
        print("Response: ", response)
        return response