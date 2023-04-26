from flask import Flask, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/home')
def home():
    return 'Hello World'

if __name__ == '__main__':
    app.run()