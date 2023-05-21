from flask import request, render_template, make_response, current_app , redirect, url_for, flash, get_flashed_messages
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
    'role': fields.String(description='New memeber role'),
})

# define a data model for the project input
project_input_model = project_ns.model('ProjectInput', {
    'name': fields.String(required=True, description='Project name'),
    'description': fields.String(required=False, description='Project description'),
})

user_model = project_ns.model('User', {
    'id': fields.String(required=True, description='User ID'),
    'username': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email'),
    'role': fields.String(required=True, description='User role'),
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
        role = data.get('role', 'User')

        project = Project.query.get(project_id)
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        # Check if the invite user is already a member of the project
        invited_user = User.query.filter_by(email=recipient_email).first()
        if invited_user is not None and  invited_user in project.members:
            return {"message": "User is already a member of the project."}

        sender = current_user
        invitation = Invitation(sender=sender, recipient_email=recipient_email, project=project, role=role)
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
        '''Process the invitation acceptance and render the project join successful page'''
        invitation = Invitation.query.get(invitation_id)
        if invitation:
            if not invitation.accepted:
                # Mark the invitation as accepted
                invitation.accepted = True
                db.session.commit()
                # Check if user already exists
                user = User.query.filter_by(email=invitation.recipient_email).first()
                new_user_details = None
                if not user:
                    # Create new user
                    print("Create New User")
                    username = invitation.recipient_email.split('@')[0]
                    password = "HiSoSupreme"  # Generate default password
                    user = User(username=username, email=invitation.recipient_email, password=password, role=invitation.role)
                    db.session.add(user)
                    db.session.commit()
                    # Flash message with username and password
                    # Pass the username and password to the template
                    new_user_details = {
                        'username': username,
                        'default_password': password
                    }
                    

                # Add user to project
                project = invitation.project
                project.members.append(user)
                db.session.commit()
                print(new_user_details)
                return make_response(render_template('join_project.html', invitation=invitation, project=project, new_user_details=new_user_details), 200, {'Content-Type': 'text/html'})
            else:
                user = User.query.filter_by(email=invitation.recipient_email).first()
                project = invitation.project
                if user.verify_password("HiSoSupreme"):
                    new_user_details = {
                        'username': user.username,
                        'default_password': "HiSoSupreme"
                    }
                else:
                    new_user_details = {
                        'username': user.username,
                    }
                return make_response(render_template('join_project.html', invitation=invitation, project=project, new_user_details=new_user_details), 200, {'Content-Type': 'text/html'})
        else:
            return make_response("Invalid invitation ID", 404)


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

@project_ns.route('/<int:project_id>/users')
class UsersByProject(Resource):
    @jwt_required()
    @admin_required
    @project_ns.marshal_with(user_model)
    def get(self, project_id):
        '''Get all users by project'''
        project = Project.query.get(project_id)
        if not project:
            project_ns.abort(404, f'Project {project_id} not found')
        
        users = project.members
        return users

@project_ns.route('/<int:project_id>/user/<int:user_id>/remove')
class RemoveUserFromProject(Resource):
    @jwt_required()
    @admin_required
    def delete(self, project_id, user_id):
        '''Remove user from project'''
        project = Project.query.get(project_id)
        user = User.query.get(user_id)

        if not project:
            project_ns.abort(404, f'Project {project_id} not found')

        if not user:
            project_ns.abort(404, f'User {user_id} not found')

        if user not in project.members:
            return {'message': 'The user is not a member of the project'}, 400

        project.members.remove(user)
        db.session.commit()

        return {'message': f'Removed user {user_id} from project {project_id}'}, 200

