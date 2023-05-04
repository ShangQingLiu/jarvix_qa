from flask import request, jsonify
from flask_restx import Resource, fields
from models import User
from werkzeug.security import generate_password_hash
from flask_restx import Api, Resource, fields, Namespace
from resources.user import  user_ns
from resources.auth import  auth_ns
from resources.chat import service_ns
from resources.file import file_ns
from resources.project import project_ns
import uuid


def create_namespaces(api:Api):

    api.add_namespace(user_ns,path='/api/user-management')
    api.add_namespace(auth_ns,path='/api/auth')
    api.add_namespace(service_ns,path='/api/service')
    api.add_namespace(file_ns,path='/api/file')
    api.add_namespace(project_ns,path='/api/project-management')




def configure_routes(api, app, mail, db, global_chatbots):
    
    create_namespaces(api)

    return app

