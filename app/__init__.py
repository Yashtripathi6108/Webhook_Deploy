from flask import Flask
from app.webhook.routes import webhook
from app.extensions import client, db 

def create_app():
    app = Flask(__name__)
    
  
    app.register_blueprint(webhook)


    @app.route('/')
    def greetings() -> str:
        return 'Welcome to the webhook'

    
    return app
