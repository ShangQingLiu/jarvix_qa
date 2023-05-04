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
    MAIL_USERNAME = 'osmallfrogo.hchs@gmail.com'
    MAIL_PASSWORD = 'kxfnbottjtfcuhaz'
    MAIL_DEFAULT_SENDER = ('Synergies', 'osmallfrogo.hchs@gmail.com')

    UPLOAD_FOLDER = os.path.join(os.getcwd(), os.environ.get('UPLOAD_FOLDER'))
    INDEX_SAVE_PATH = os.environ.get('INDEX_SAVE_PATH')
    OPEN_API_KEY = os.environ.get('OPEN_API_KEY')
    ROOT_PATH = os.getcwd()