from app import create_app
from flask_cors import CORS

app = create_app()

CORS(app, resources={r"/webhook/*": {"origins": "*"}})

@app.route('/')

def greetings() -> str:
    return 'Welcome to the webhook'



