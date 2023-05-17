from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# @app.route("/home")
# def home():
#     return "Hello World"

@app.route("/maze/query", methods = ["POST"])
def generateMaze():
    data = request.get_json()
    print(data)
    return data

@app.route("/maze/photo")
def takePhotoWithPython():
    
    return 0


if __name__ == "__main__":
    app.run()