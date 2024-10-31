from flask import Flask

app = Flask(__name__)

# Define routes
@app.route('/')
def home():
    return "Hello, World!"
