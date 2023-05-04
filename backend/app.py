from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_restx import Api
from models import db
from dotenv import load_dotenv
import os

from config import Config
from routes import configure_routes
from globals import global_chatbots,mail

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
print(app.config["UPLOAD_FOLDER"])
# set OPEN_AI_KEY
os.environ['OPENAI_API_KEY'] = os.environ.get('OPEN_API_KEY')

CORS(app)
<<<<<<< HEAD
jwt = JWTManager(app)
mail.init_app(app)
db.init_app(app)

authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}
api_security = {'Bearer': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'}}
api = Api(app, version='1.0', title='Jarvix QA', authorizations=api_security, security=api_security)
# This is where the duck typing magic comes in
jwt._set_error_handler_callbacks(api)
@jwt.expired_token_loader
def expired_token_callback():
    return {"msg": "Token has expired"}, 401

@jwt.invalid_token_loader
def invalid_token_callback():
    return {"msg": "Invalid token"}, 401
=======
api = Api(app)
app.config['OPEN_API_KEY'] = os.environ.get('OPEN_API_KEY')
app.config['INDEX_SAVE_PATH'] = os.environ.get('INDEX_SAVE_PATH')
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd() ,os.environ.get('UPLOAD_FOLDER'))
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
global_chatbots = {}
>>>>>>> main

#ns = api.namespace('/api/', description='test')

<<<<<<< HEAD
@app.before_first_request
def create_tables():
    db.create_all()
=======

#ns.route('/')
class HelloWorld(Resource):
    def get(self):
        return "<p>This is the QA system based on llama index!</p>"
api.add_resource(HelloWorld, '/api/')
#@app.route("/")
#def hello_world():
#    return "<p>This is the QA system based on llama index!</p>"
#
#@app.route("/api/")
#def hello_world_t():
#    return "<p>This is the QA system based on llama index!</p>"
>>>>>>> main

app = configure_routes(api, app, mail, db, global_chatbots)

<<<<<<< HEAD
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
=======

# Upload File
@app.route("/api/upload", methods=['POST'])
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


@app.route("/api/prepareIndex", methods=['POST'])
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


@app.route("/api/query", methods=['POST'])
def query():
    data = request.get_json()

    project_name = data.get('project_name')
    session_id = data.get('session_id')
    query = data.get('query')

    if project_name is None or session_id is None or query is None: 
        return jsonify({'error': 'No project name in the request'}), 400

    project_dir = os.path.join(app.config['UPLOAD_FOLDER'], project_name)
    print(f"gloabl_chatbots keys:{global_chatbots.keys()}")
    if session_id not in global_chatbots.keys():
        print("Loading index")
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
        chatbot = ChatBot(index_set,True,project_name=project_name,chunk_size_limit=512)
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

@app.route("/api/list_files", methods=["POST"])
def list_files():
    project_name = request.form["project_name"]
    file_list = get_files_for_project(project_name)
    return jsonify({"files": file_list})

if __name__ == '__main__':
    app.run(debug=False,threaded=True)
>>>>>>> main
