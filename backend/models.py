from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import hashlib
from datetime import datetime
import os

db = SQLAlchemy()

class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='User')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('invitations', lazy='dynamic'))
    sender = db.relationship('User', backref=db.backref('sent_invitations', lazy='dynamic'))
    accepted = db.Column(db.Boolean, default=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # many-to-many relationship between users and projects
    members = db.relationship('User', secondary='user_project', backref=db.backref('projects', lazy='dynamic'))

# join table for many-to-many relationship between users and projects
user_project = db.Table('user_project',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='User')


    def __init__(self, username, email, password, role='User'):
        self.username = username
        self.email = email
        self.password = hashlib.sha256(
            (password + os.environ.get('SALT', 'default_salt')).encode('utf-8')
        ).hexdigest()
        self.role = role

    def verify_password(self, password):
        return self.password == hashlib.sha256(
            (password + os.environ.get('SALT', 'default_salt')).encode('utf-8')
        ).hexdigest()

    def set_password(self, password):
        self.password = hashlib.sha256(
            (password + os.environ.get('SALT', 'default_salt')).encode('utf-8')
        ).hexdigest()
