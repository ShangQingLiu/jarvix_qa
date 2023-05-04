from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_restx import Api
from models import db
from dotenv import load_dotenv
import os

from config import Config
from routes import configure_routes
from globals import global_chatbots,mail

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
print(app.config["UPLOAD_FOLDER"])
# set OPEN_AI_KEY
os.environ['OPENAI_API_KEY'] = os.environ.get('OPEN_API_KEY')

CORS(app)
jwt = JWTManager(app)
mail.init_app(app)
db.init_app(app)

authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}
api_security = {'Bearer': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'}}
api = Api(app, version='1.0', title='Jarvix QA', authorizations=api_security, security=api_security)
# This is where the duck typing magic comes in
jwt._set_error_handler_callbacks(api)
@jwt.expired_token_loader
def expired_token_callback():
    return {"msg": "Token has expired"}, 401

@jwt.invalid_token_loader
def invalid_token_callback():
    return {"msg": "Invalid token"}, 401

#ns = api.namespace('/api/', description='test')

@app.before_first_request
def create_tables():
    db.create_all()

app = configure_routes(api, app, mail, db, global_chatbots)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
