from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import jwt_required
from utils import IndexUtils, DataType
from flask import request,jsonify, current_app
import os
import mimetypes
from utils import check_dir_exists, IndexUtils, get_files_for_project
from werkzeug.datastructures import FileStorage


file_ns = Namespace('file',description="File management")

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('files', location='files', type=FileStorage, action='append', required=True, help='The files to upload')
upload_parser.add_argument('project_name', location='args', type=str, help='Project_name for the file')

file_all = file_ns.model('File', {
    'project_name': fields.String(required=True, description='Focus Project Name'),
})

delete_file = file_ns.model('delete file', {
    'filename': fields.String(required=True, description='Focus File Name'),
    'project_name': fields.String(required=True, description='Focus Project Name'),
})


@file_ns.route("/list_files")
class listFile(Resource):
    @file_ns.expect(file_all)
    @jwt_required() 
    def post(self):

        data = request.get_json()
        project_name = data.get("project_name")
        if not project_name:
            return jsonify({'error': 'Project name is empty in the request'}), 400

        file_list = get_files_for_project(project_name)
        return jsonify({"files": file_list})

@file_ns.route('/upload')
class UploadFile(Resource):
    @file_ns.expect(upload_parser)
    @jwt_required() 
    def post(self): 
        files = request.files.getlist('files')

        for file in files:

            # Get the file's MIME type
            content_type = file.content_type

            # Get the file extension based on the MIME type
            file_extension = mimetypes.guess_extension(content_type)
            project_name = request.args.get("project_name")
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], project_name)

            if file_extension[1:].lower() == 'm4a':
                upload_folder = os.path.join(upload_folder, 'audio')
            else:
                upload_folder = os.path.join(upload_folder, file_extension[1:].lower())
            # Check if the upload directory exists, create it if not
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            # Save the file to the UPLOAD_FOLDER
            file.save(os.path.join(upload_folder, file.filename))

        return {'message': 'Files uploaded successfully'}, 200

@file_ns.route("/prepareIndex")
class prepare_index(Resource):
    @file_ns.expect(file_all)
    @jwt_required() 
    def post(self):
        data = request.get_json()
        
        print("Preparing index...")
        project_name = data.get("project_name")
        project_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], project_name)

        # Make sure the project directory exists
        check_dir_exists(project_dir)

        print("Loading indexUtils...")
        indexUtils = IndexUtils(current_app.config["INDEX_SAVE_PATH"], project_name)

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

        return {'message': 'Index created successfully'}, 200
        
@file_ns.route('/delete')
class DeleteFile(Resource):
    @file_ns.expect(delete_file)
    @jwt_required()
    def delete(self):
        data = request.get_json()
        project_name = data.get("project_name")
        filename = data.get("filename")

        if not project_name:
            return {'error': 'Project name is empty in the request'}, 400

        if not filename:
            return {'error': 'Filename is empty in the request'}, 400

        file_extension = os.path.splitext(filename)[1][1:].lower()

        project_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], project_name)
        file_type_path = os.path.join(project_dir,file_extension)
        file_path = os.path.join(file_type_path, filename)
        print(file_path)

        if not os.path.exists(file_path):
            return {'error': f'File {filename} not found in project {project_name}'}, 404

        try:
            os.remove(file_path)
        except Exception as e:
            return {'error': f'Error deleting file {filename}: {str(e)}'}, 500

        return {'message': f'File {filename} deleted successfully from project {project_name}'}, 200

@file_ns.route("/checkIndex")
class CheckIndex(Resource):
    @file_ns.expect(file_all)
    @jwt_required()
    def post(self):
        data = request.get_json()
        project_name = data.get("project_name")
        if not project_name:
            return jsonify({'error': 'Project name is empty in the request'}), 400

        # Check if the project index exists
        index_file_path = os.path.join(current_app.config["ROOT_PATH"],current_app.config["INDEX_SAVE_PATH"])
        if len(os.listdir(index_file_path))!=0:
            return {"message": "Index exists"}, 200
        else:
            return {"message": "Index does not exist"}, 404


