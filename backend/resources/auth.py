from flask_restx import Namespace, Resource, fields
from flask import current_app
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token

auth_ns = Namespace('auth', description='Authentication related operations')

# Define request and response models
login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='User name'),
    'password': fields.String(required=True, description='Password'),
})

reset_password_model = auth_ns.model('ResetPassword', {
    'email': fields.String(required=True, description='Email address'),
})
@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
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
            return {'access_token': "Bearer "+token}, 200

        # Invalid credentials
        return {'message': 'Invalid username or password'}, 401

@auth_ns.route('/refresh')
class RefreshToken(Resource):
    @jwt_required()
    def post(self):
        # Get the current user identity
        current_user = get_jwt_identity()
        
        # Generate a new access token using the identity of the currently authenticated user
        new_token = create_refresh_token(identity=current_user)

        return {'access_token': 'Bearer ' + new_token}, 200