from flask_mail import Mail
mail = Mail()
global_chatbots = {}
project_session = {}
chat_history = {}
upload_hashes = {} # key: Project id, value: hash