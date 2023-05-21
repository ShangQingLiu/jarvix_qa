from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User
import uuid
from flask_mail import Message
from globals import mail

# Create a namespace for the users endpoint
user_ns = Namespace('user management', description='user management')

get_user_model = user_ns.model('Get_user', {
    'id': fields.String(required=True, description='The username of the user'),
    'username': fields.String(required=True, description='The username of the user'),
    'email': fields.String(required=True, description='The email of the user'),
    'password': fields.String(required=True, description='The password of the user'),
    'role': fields.String(required=True, description='The role of the user'),
})

user_info = user_ns.model('User info', {
    'id': fields.String(required=True, description='The username of the user'),
    'username': fields.String(required=True, description='The username of the user'),
    'email': fields.String(required=True, description='The email of the user'),
    'role': fields.String(required=True, description='The role of the user'),
})

user_model = user_ns.model('User', {
    'username': fields.String(required=True, description='The username of the user'),
    'email': fields.String(required=True, description='The email of the user'),
    'password': fields.String(required=True, description='The password of the user'),
})

forgot_password_model = user_ns.model('ForgotPassword', {
    'email': fields.String(required=True, description='The email address')
})

@user_ns.route('/user_list')
class UserList(Resource):
    @user_ns.doc('list_users')
    @user_ns.marshal_list_with(get_user_model)
    @jwt_required() 
    def get(self):
        '''Fetch all users'''
        return User.query.all()

    @user_ns.doc('create_user')
    @user_ns.expect(user_model)
    @user_ns.marshal_with(get_user_model, code=201)
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

@user_ns.route('/<int:user_id>')
@user_ns.response(404, 'User not found')
@user_ns.param('user_id', 'The user identifier')
class UserResource(Resource):
    @user_ns.doc('get_user')
    @user_ns.marshal_with(user_model)
    @jwt_required() 
    def get(self, user_id):
        '''Fetch a user given its identifier'''
        user = User.query.get(user_id)
        if not user:
            current_app.api.abort(404)
        return user

    @user_ns.doc('update_user')
    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model)
    @jwt_required() 
    def put(self, user_id):
        '''Update a user given its identifier'''
        data = request.get_json()
        print(data)
        user = User.query.get(user_id)
        if not user:
            current_app.api.abort(404)
        user.username = data.get('username')
        user.email = data.get('email')
        user.set_password(data.get('password'))
        db.session.commit()
        return user

    @user_ns.doc('delete_user')
    @user_ns.response(204, 'User deleted')
    @jwt_required() 
    def delete(self, user_id):
        '''Delete a user given its identifier'''
        user = User.query.get(user_id)
        if not user:
            return {"message":"Invalid User ID"}, 404

        user.projects = []
        
        db.session.delete(user)
        db.session.commit()
        return '', 204

@user_ns.route('/forgot_password')
class ForgotPassword(Resource):
    @user_ns.expect(forgot_password_model)
    def post(self):
        data = user_ns.payload
        email = data.get('email')

        # Lookup user by email
        user = User.query.filter_by(email=email).first()

        if user:
            # Generate new password
            new_password = uuid.uuid4().hex.upper()[0:6]

            # Update user's password
            user.set_password(new_password) 
            db.session.commit()

            # Send email with new password
            msg = Message('Forgot Password', sender='noreply@example.com', recipients=[email])
            msg.body = f'Your new password is: {new_password}'
            mail.send(msg)

            return {'message': 'Email sent with new password'}, 200

        # User not found
        return {'message': 'User not found with this email'}, 404

@user_ns.route('/info')
class UserInfo(Resource):
    @user_ns.marshal_with(user_info)
    @jwt_required() 
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user is None:
            return {'error': 'User not found'}, 404
        user_info = {'id': user.id, 'username': user.username, 'email': user.email, 'role':user.role}
        return user_info, 200

@user_ns.route('/create_user')
class CreateUser(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'User')  # Default role is 'User' if not specified

        # Check if the user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            return {"message": "User already exists."}, 400

        # Create the new user and save it to the database
        user = User(username=username, email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()

        return {"message": f"User {username} created with role {role}."}

