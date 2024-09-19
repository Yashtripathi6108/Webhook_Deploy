from app import create_app
from flask_cors import CORS

app = create_app()

CORS(app, origins=["https://66ebabad2ffe93169d4aa107--fastidious-platypus-481cda.netlify.app"])

@app.route('/')
def greetings() -> str:
    return 'Welcome to the webhook'



if __name__ == '__main__': 
    app.run(debug=True)

