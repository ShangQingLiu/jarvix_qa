from flask import Flask,request,jsonify
from openapi_schema_pydantic import SecurityRequirement
from config import Config
from utils import IndexUtils, DataType
from chatbot import ChatBot 
from dotenv import load_dotenv
import openai
from os import walk
import mimetypes
from flask_cors import CORS

from flask_restx import Api, Resource, fields, Namespace
from models import db, User

import jwt
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token




import os

load_dotenv()
app = Flask(__name__)
CORS(app)
JWTManager(app)

api = Api(app,version='1.0',title='Jarvix QA',authorizations={
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
},security=[
        {'jwt':[]}
    ]
)
# Create a namespace for the users endpoint
user_management_ns = Namespace('user management', description='user management')

user_model = api.model('User', {
    'username': fields.String(required=True, description='The username of the user'),
    'email': fields.String(required=True, description='The email of the user'),
    'password': fields.String(required=True, description='The password of the user'),
})

app.config['OPEN_API_KEY'] = os.environ.get('OPEN_API_KEY')
app.config['INDEX_SAVE_PATH'] = os.environ.get('INDEX_SAVE_PATH')
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd() ,os.environ.get('UPLOAD_FOLDER'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

db.init_app(app)
global_chatbots = {}


@app.before_first_request
def create_tables():
    db.create_all()

auth_ns = Namespace('auth', description='Authentication operations')

user_login = auth_ns.model('UserLogin', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(user_login, validate=True)
    def post(self):
        data = auth_ns.payload
        username = data.get('username')
        password = data.get('password')

        # Lookup user by username
        user = User.query.filter_by(username=username).first()

        # Verify password
        if user and user.verify_password(password):
            # Password is valid, create token
            token = create_access_token(identity=user.id)
            return {'access_token': token}, 200

        # Invalid credentials
        return {'message': 'Invalid username or password'}, 401
    
@user_management_ns.route('/user_list')
class UserList(Resource):
    @user_management_ns.doc('list_users')
    @user_management_ns.marshal_list_with(user_model)
    def get(self):
        '''Fetch all users'''
        return User.query.all()

    @user_management_ns.doc('create_user')
    @user_management_ns.expect(user_model)
    @user_management_ns.marshal_with(user_model, code=201)
    def post(self):
        '''Create a new user'''
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user = User(username=username, email=email,password=password)
        db.session.add(user)
        db.session.commit()
        return user, 201

@user_management_ns.route('/<int:user_id>')
@user_management_ns.response(404, 'User not found')
@user_management_ns.param('user_id', 'The user identifier')
class UserResource(Resource):
    @user_management_ns.doc('get_user')
    @user_management_ns.marshal_with(user_model)
    def get(self, user_id):
        '''Fetch a user given its identifier'''
        user = User.query.get(user_id)
        if not user:
            api.abort(404)
        return user

    @user_management_ns.doc('update_user')
    @user_management_ns.expect(user_model)
    @user_management_ns.marshal_with(user_model)
    def put(self, user_id):
        '''Update a user given its identifier'''
        data = request.get_json()
        user = User.query.get(user_id)
        if not user:
            api.abort(404)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        db.session.commit()
        return user

    @user_management_ns.doc('delete_user')
    @user_management_ns.response(204, 'User deleted')
    def delete(self, user_id):
        '''Delete a user given its identifier'''
        user = User.query.get(user_id)
        if not user:
            api.abort(404)
        db.session.delete(user)
        db.session.commit()
        return '', 204

@api.route('/')
class HelloWorld(Resource):
    def get(self):
        return "<p>This is the QA system based on llama index!</p>"

@api.route('/protected')
class Protected(Resource):
    @api.doc(security='jwt')
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {'message': f'Hello, {current_user}!'}

# Upload File
@app.route("/upload", methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'project_name' not in request.form:
        return jsonify({'error': 'No file part or project name in the request'}), 400

    file = request.files['file']

    # Get the file's MIME type
    content_type = file.content_type

    # Get the file extension based on the MIME type
    file_extension = mimetypes.guess_extension(content_type)

    project_name = request.form['project_name']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], project_name)
    if file_extension[1:].lower() == 'm4a':
        upload_folder = os.path.join(upload_folder, 'audio')
    else:
        upload_folder = os.path.join(upload_folder, file_extension[1:].lower())
    # Check if the upload directory exists, create it if not
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Save the file to the UPLOAD_FOLDER
    file.save(os.path.join(upload_folder, file.filename))

    return jsonify({'message': 'File uploaded successfully'}), 200


@app.route("/prepareIndex", methods=['POST'])
def prepare_index():
    def check_dir_exists(dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    if 'project_name' not in request.form:
        return jsonify({'error': 'No project name in the request'}), 400
    
    print("Preparing index...")
    project_name = request.form['project_name']
    project_dir = os.path.join(app.config['UPLOAD_FOLDER'], project_name)

    # Make sure the project directory exists
    check_dir_exists(project_dir)

    print("Loading indexUtils...")
    indexUtils = IndexUtils(app.config["INDEX_SAVE_PATH"], project_name)

    # Read all files in the project directory
    print("Reading files...")
    index_set = {}
    for data_type in DataType:
        if data_type == DataType.DOCX:
            docx_path = os.path.join(project_dir, "docx")
            check_dir_exists(docx_path)
            doc_pathes = os.listdir(docx_path)
            doc_pathes = [os.path.join(docx_path, doc_path) for doc_path in doc_pathes]
            print("doc_pathes: ", doc_pathes)
            if len(doc_pathes) == 0:
                continue
            print("Loading data...DOCX")
            index_set.update(indexUtils.dataLoader(doc_pathes, data_type))
        elif data_type == DataType.PDF:
            pdf_path = os.path.join(project_dir, "pdf")
            check_dir_exists(pdf_path)
            pdf_pathes = os.listdir(pdf_path)
            pdf_pathes = [os.path.join(pdf_path, pdf_e) for pdf_e in pdf_pathes]
            if len(pdf_pathes) == 0:
                continue
            index_set.update(indexUtils.dataLoader(pdf_pathes, data_type))
        elif data_type == DataType.HTML:
            html_path = os.path.join(project_dir, "html")
            check_dir_exists(html_path)
            html_pathes = os.listdir(html_path)
            html_pathes = [os.path.join(html_path, html_e) for html_e in html_pathes]
            if len(html_pathes) == 0:
                continue
            index_set.update(indexUtils.dataLoader(html_pathes, data_type))
        elif data_type == DataType.AUDIO:
            audio_path = os.path.join(project_dir, "audio")
            check_dir_exists(audio_path)
            audio_pathes = os.listdir(audio_path)
            audio_pathes = [os.path.join(audio_path, audio_e) for audio_e in audio_pathes]
            if len(audio_pathes) == 0:
                continue
            index_set.update(indexUtils.dataLoader(audio_pathes, data_type))
        elif data_type == DataType.XLSX:
            xlsx_path = os.path.join(project_dir, "xlsx")
            check_dir_exists(xlsx_path)
            xlsx_pathes = os.listdir(xlsx_path)
            xlsx_pathes = [os.path.join(xlsx_path, xlsx_e) for xlsx_e in xlsx_pathes]
            print(f"xlsx_pathes", xlsx_pathes)
            if len(xlsx_pathes) == 0:
                continue
            index_set.update(indexUtils.dataLoader(xlsx_pathes, data_type))

    return jsonify({'message': 'Index created successfully'}), 200


@app.route("/query", methods=['POST'])
def query():
    data = request.get_json()

    project_name = data.get('project_name')
    session_id = data.get('session_id')
    query = data.get('query')

    if project_name is None or session_id is None or query is None: 
        return jsonify({'error': 'No project name in the request'}), 400

    project_dir = os.path.join(app.config['UPLOAD_FOLDER'], project_name)

    if session_id not in global_chatbots.keys():
        # Make sure the project directory exists
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        indexUtils = IndexUtils(app.config["INDEX_SAVE_PATH"],project_name)

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
                audio_dir = os.path.join(project_dir, "audio")
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

def get_files_for_project(project_name):
    # Assuming your uploaded files are stored in a folder named after the project_name
    project_folder = os.path.join(app.config['UPLOAD_FOLDER'], project_name)

    f = []
    for data_fd in  os.listdir(project_folder):
        f.extend(os.listdir(os.path.join(project_folder,data_fd)))

    return f

@app.route("/list_files", methods=["POST"])
def list_files():
    project_name = request.form["project_name"]
    file_list = get_files_for_project(project_name)
    return jsonify({"files": file_list})


api.add_namespace(user_management_ns,path='/api/user-management')
api.add_namespace(auth_ns,path='/api/auth')

if __name__ == '__main__':
    app.run(debug=True)