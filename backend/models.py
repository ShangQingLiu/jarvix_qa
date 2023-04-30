from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import hashlib
from werkzeug.security import check_password_hash, generate_password_hash
import os

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = hashlib.sha256(
            (password + os.environ.get('SALT', 'default_salt')).encode('utf-8')
        ).hexdigest()

    def verify_password(self, password):
        return self.password == hashlib.sha256(
            (password + os.environ.get('SALT', 'default_salt')).encode('utf-8')
        ).hexdigest()

    def set_password(self, password):
        self.passwordh = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)