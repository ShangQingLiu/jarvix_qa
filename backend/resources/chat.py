from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask,request,jsonify, current_app, make_response
from utils import IndexUtils, DataType
from globals import global_chatbots, project_session, chat_history
from chatbot import ChatBot
from models import Project, User
import os
import requests
import logging




service_ns = Namespace('service',description="File management")

query_model = service_ns.model('Query', {
    'project_name': fields.String(required=True, description='Focus Project Name'),
    'session_id': fields.String(required=True, description='Remain the talk in the same session'),
    'query': fields.String(required=True, description='query string from customer'),
    'language': fields.String(description='return language'),
})

validation_form_model = service_ns.model('ValidationForm', {
    'validation_form': fields.String(required=True, description='Validation form string'),
    'project_name': fields.String(required=True, description='Focus Project Name'),
    'session_id': fields.String(required=True, description='Remain the talk in the same session'),
})

answer_model = service_ns.model('Answer', {
    'question': fields.String(required=True, description='Question'),
    'expect_answer': fields.String(required=True, description='Expected Answer'),
    'query_answer': fields.String(required=True, description='Queried Answer'),
    'is_correct': fields.Boolean(required=True, description='Is the Answer Correct?')
})

response_model = service_ns.model('Response', {
    'answer': fields.List(fields.Nested(answer_model), required=True, description='List of Answer Objects'),
    'correct_number': fields.Integer(required=True, description='Number of Correct Answers'),
    'wrong_number': fields.Integer(required=True, description='Number of Wrong Answers'),
    'total_number': fields.Integer(required=True, description='Total Number of Answers')
})

def get_files(upload_dir:str, file_type:str):
    file_dir = os.path.join(upload_dir, file_type) 
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_pathes = os.listdir(file_dir)
    result = [os.path.join(upload_dir, file_type, file_path) for file_path in file_pathes]
    return result

def get_all_upload_files(upload_dir:str, file_type:str):
    # for pdf extract also tabular data and image data
    result = []
    if file_type == "pdf":
        pass
        # tabular
        result += get_files(upload_dir,"pdf_tabular")
    
    result += get_files(upload_dir,file_type)
     
    return result

def answer(project_name,session_id, query, is_yes_no_q=False):
    # Prepare Index
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], project_name)
    if session_id not in global_chatbots.keys():
        # Make sure the project directory exists
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        indexUtils = IndexUtils(current_app.config["INDEX_SAVE_PATH"],project_name)

        # Read all files in the project directory
        index_set = {}
        _FAISS = os.getenv("USING_FAISS", 'False').lower() in ('true', '1', 't') 
        if _FAISS: 
            file_pathes = []
            for data_type in DataType:
                file_pathes += get_all_upload_files(upload_dir,data_type.name.lower())
            index_set = indexUtils.dataLoader(file_pathes, None)
        else:
            for data_type in DataType:
                file_pathes = get_all_upload_files(upload_dir,data_type.name.lower())
                index_set.update(indexUtils.dataLoader(file_pathes, data_type))

        # print("Index set: ", index_set)
        chatbot = ChatBot(index_set,None,project_name=project_name)
        global_chatbots[session_id] = chatbot
        if project_name not in project_session.keys():
            project_session[project_name] = [session_id]
        else:
            project_session[project_name].append(session_id)
    # Find Answer
    chatbot = global_chatbots[session_id]
    if is_yes_no_q:
        response = chatbot.run_yes_no(query)
    else:
        response = chatbot.run(query)
    return response

def translate(text,language:str): # language: ZH, EN
    result = ""

    if text != "":
        try:
            url = "https://api.deepl.com/v2/translate"
            headers = {
                "Authorization": f"DeepL-Auth-Key {os.environ.get('DEEP_L_KEY')}"
            }
            data = {
                "text": f"{text}",
                "target_lang": f"{language}"
            }

            text = requests.post(url, headers=headers, data=data)
            # print(response.json())
            result = text.json()["translations"][0]["text"]
        except: 
            result = text
    else:
        result =  text
    return result

def get_query_answer(project_name,session_id, query):
    response = answer(project_name,session_id, query, is_yes_no_q=True)
    # response = translate(response,"ZH")
    return response

@service_ns.route("/validation_form")
class ValidationForm(Resource):
    @service_ns.expect(validation_form_model)
    @service_ns.marshal_with(response_model)
    @jwt_required()
    def post(self):
        data = request.get_json()
        validation_form = data.get('validation_form')
        project_name = data.get('project_name')
        session_id = data.get('session_id')

        if project_name is None or session_id is None: 
            return {'error': 'No project name or session id  in the request'}, 400

        if validation_form is None:
            return {'error': 'No validation form in the request'}, 400

        # Assuming the validation form string format is: "Q1,ExpectedAnswer\nQ2,ExpectedAnswer\n..."
        form_lines = validation_form.split('\n')
        
        answer_list = []
        correct_number = 0
        wrong_number = 0

        for line in form_lines:
            question, expect_answer = line.split(',')
            # print(expect_answer)

            # Assuming the function get_query_answer(question) is available and returns the answer to a given question
            query_answer = get_query_answer(project_name,session_id,question)
            is_correct = (expect_answer.lower() in query_answer.lower())

            answer_list.append({
                'question': question,
                'expect_answer': expect_answer,
                'query_answer': query_answer,
                'is_correct': is_correct
            })

            if is_correct:
                correct_number += 1
            else:
                wrong_number += 1

        response = {
            'answer': answer_list,
            'correct_number': correct_number,
            'wrong_number': wrong_number,
            'total_number': correct_number + wrong_number
        }

        return response
        

@service_ns.route("/query")
class Query(Resource):
    @service_ns.expect(query_model)
    @jwt_required()
    def post(self):
        data = request.get_json()

        project_name = data.get('project_name')
        session_id = data.get('session_id')
        query = data.get('query')
        language = data.get('language')
        language = language if language is not None else "ZH_TW"
        query_origin = query

        if project_name is None or session_id is None or query is None: 
            return {'error': 'No project name in the request'}, 400

        # Prepare Index
        logging.info("prepare index")
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], project_name)
        if session_id not in global_chatbots.keys():
            # Make sure the project directory exists
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            indexUtils = IndexUtils(current_app.config["INDEX_SAVE_PATH"],project_name)

            # Read all files in the project directory
            index_set = {}
            _FAISS = os.getenv("USING_FAISS", 'False').lower() in ('true', '1', 't') 
            if _FAISS: 
                file_pathes = []
                for data_type in DataType:
                    file_pathes += get_all_upload_files(upload_dir,data_type.name.lower())
                index_set = indexUtils.dataLoader(file_pathes, None)
            else:
                for data_type in DataType:
                    file_pathes = get_all_upload_files(upload_dir,data_type.name.lower())
                    index_set.update(indexUtils.dataLoader(file_pathes, data_type))

            # print("Index set: ", index_set)
            logging.info("Start to build chatbot")
            logging.info("language: ", language)
            chatbot = ChatBot(index_set,None,project_name=project_name, language=language)
            global_chatbots[session_id] = chatbot
            if project_name not in project_session.keys():
                project_session[project_name] = [session_id]
            else:
                project_session[project_name].append(session_id)
        # Find Answer
        chatbot = global_chatbots[session_id]
        response = chatbot.run(query)
        record = {"query":query_origin, "response":response} 
        logging.debug("record: ", record)

        # Record 
        if session_id not in chat_history.keys():
            chat_history[session_id] = [record]
        else:
            chat_history[session_id].append(record)
        
        return response

@service_ns.route("/sessions/<string:project_name>")
@service_ns.param('project_name', 'Project name')
class Sessions(Resource):
    @jwt_required()
    def get(self, project_name):
        if project_name not in project_session.keys():
            return {'sessions': []}

        session_ids = project_session[project_name]
        return {'sessions': session_ids}

@service_ns.route("/sessions/<string:project_id>")
@service_ns.param('project_id', 'Project ID')
class Sessions(Resource):
    @jwt_required()
    def get(self, project_id):
        user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id).filter(Project.members.any(User.id == user_id)).first()
        if project.name not in project_session.keys():
            return {'sessions': []}

        session_ids = project_session[project.name]
        return {'sessions': session_ids}

# TODO: Long time storage in the file system
@service_ns.route("/chat_history/<string:session_id>")
class ChatHistory(Resource):
    @jwt_required()
    def get(self, session_id):
        if session_id not in chat_history.keys():
            return {'error': 'Session ID not found'}, 404
        history = chat_history[session_id]
        # serialize response as JSON only if it's a string
        history_serialized = [{'query': r['query'], 'response': r['response']} 
                              for r in history if isinstance(r['response'], str)]

        # print(chat_history)
        return {'chat_history': history_serialized}