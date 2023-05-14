from flask import request, render_template, make_response, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_restx import Namespace, Resource, fields
from flask_cors import cross_origin
from flask_mail import Message
from functools import wraps
from models import db, Project, User, Invitation
from globals import mail
import os

project_ns = Namespace('project management', description='project management')

project_model = project_ns.model('Project', {
    'name': fields.String(required=True, description='Project name'),
    'description': fields.String(required=True, description='Project description'),
})

project_model_with_id = project_ns.model('Project All', {
    'id': fields.String(required=True, description='Project ID'),
    'name': fields.String(required=True, description='Project name'),
    'description': fields.String(required=True, description='Project description'),
})

get_project_model = project_ns.model('get project', {
    'id': fields.String(required=True, description='Project ID'),
    'name': fields.String(required=True, description='Project name'),
    'description': fields.String(required=True, description='Project description'),
})

project_invite_model = project_ns.model('invite model', {
    'email': fields.String(required=True, description='New memeber email'),
})

# define a data model for the project input
project_input_model = project_ns.model('ProjectInput', {
    'name': fields.String(required=True, description='Project name'),
    'description': fields.String(required=False, description='Project description'),
})

def jwt_project_access_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        project_id = kwargs['project_id']
        user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id).filter(Project.members.any(User.id == user_id)).first()
        if not project:
            project_ns.abort(403, f'User does not have access to project {project_id}')
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()  # Ensure the JWT is present in the request
        identity = get_jwt_identity()  # Get the identity from the JWT token

        # Retrieve the user from the identity (e.g., querying from the database)
        user = User.query.get(identity)

        if user and user.role == 'Admin':
            return fn(*args, **kwargs)
        else:
            return {'message': 'You do not have permission to access this resource.'}, 403

    return wrapper

# Admin
@project_ns.route('/')
class create_project(Resource): 
    @project_ns.doc('create_project')
    @project_ns.expect(project_model)
    @project_ns.marshal_with(get_project_model, code=201)
    @admin_required
    def post(self):
        '''create project'''
        print("here")
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        if not name:
            return {'error': 'Project name is required'}, 400
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        project = Project(name=name, description=description)
        project.members.append(current_user)
        db.session.add(project)
        db.session.commit()
        return project, 201

# Admin
@project_ns.route('/<int:project_id>/invite')
class invite(Resource):
    @project_ns.doc('invite people to the project')
    @project_ns.expect(project_invite_model)
    @admin_required
    def post(self, project_id):
        '''send invitation'''
        data = request.get_json()
        recipient_email = data.get('email')
        project = Project.query.get(project_id)
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        sender = current_user
        invitation = Invitation(sender=sender, recipient_email=recipient_email, project=project)
        db.session.add(invitation)
        db.session.commit()

        # send email
        msg = Message('Invitation to join project', recipients=[recipient_email])
        msg.body = render_template('invitation_email.txt', invitation=invitation)
        mail.send(msg)

        return {"message":"Successful send the invitation."}

@project_ns.route('/invitation/<int:invitation_id>/accept')
class accept_invitation(Resource):
    def get(self, invitation_id):
        '''Invitation Accept page'''
        invitation = Invitation.query.get(invitation_id)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('accept_invitation.html', invitation=invitation),200,
                                              headers)
    
    def post(self, invitation_id):
        '''Project join successful page'''
        invitation = Invitation.query.get(invitation_id)

        # check if user already exists
        user = User.query.filter_by(email=invitation.recipient_email).first()
        if not user:
            # create new user
            username = invitation.recipient_email.split('@')[0]
            password = os.urandom(8).hex()  # generate random password
            user = User(username=username, email=invitation.recipient_email, password=password)
            db.session.add(user)
            db.session.commit()

        # add user to project
        project = invitation.project
        project.members.append(user)
        db.session.commit()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('join_project.html', invitation=invitation,project=project),200,
                                              headers)

@project_ns.route('/<int:project_id>')
class Project_manage(Resource):
    @project_ns.marshal_with(project_model)
    @jwt_project_access_required
    def get(self, project_id):
        '''get proejct'''
        project = Project.query.get(project_id)
        if not project:
            current_app.api.abort(404, f'Project {project_id} not found')
        return project
    # Admin
    @project_ns.expect(project_input_model)
    @project_ns.marshal_with(project_model)
    @jwt_project_access_required
    @admin_required
    def put(self, project_id):
        '''Update project'''
        project = Project.query.get(project_id)
        if not project:
            project_ns.abort(404, f'Project {project_id} not found')

        # update project attributes
        project.name = project_ns.payload['name']
        project.description = project_ns.payload.get('description', '')

        db.session.commit()
        return project
    # Admin
    @jwt_project_access_required
    @admin_required
    def delete(self, project_id):
        '''Delete project'''
        project = Project.query.get(project_id)
        if not project:
            project_ns.abort(404, f'Project {project_id} not found')

        db.session.delete(project)
        db.session.commit()
        return '', 204

@project_ns.route('/user/<int:user_id>')
class ProjectsByUser(Resource):
    @jwt_required()
    @project_ns.marshal_with(project_model_with_id)
    def get(self, user_id):
        '''get projects by user'''
        user = User.query.get(user_id)
        if not user:
            project_ns.abort(404, f'User {user_id} not found')
        
        projects = user.projects.all()
        return projects

@project_ns.route('/projects')
class ProjectList(Resource):
    @project_ns.marshal_with(project_model_with_id, envelope='projects')
    def get(self):
        projects = Project.query.all()
        return projects, 200

