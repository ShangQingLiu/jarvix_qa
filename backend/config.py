import os

class Config:
    DEBUG = True
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") 
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") 
    MAIL_DEFAULT_SENDER = ('Synergies', os.environ.get("MAIL_DEFAULT_SENDER"))

    UPLOAD_FOLDER = os.path.join(os.getcwd(), os.environ.get('UPLOAD_FOLDER'))
    INDEX_SAVE_PATH = os.environ.get('INDEX_SAVE_PATH')
    OPEN_API_KEY = os.environ.get('OPEN_API_KEY')
    SERVER_NAME = os.environ.get('SERVER_NAME')
    ROOT_PATH = os.getcwd()
    PREFERRED_URL_SCHEME='https'
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60