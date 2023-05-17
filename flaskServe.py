from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/data/<jsdata>")
def test(jsdata):
    data = json.loads(jsdata)
    print(data["gridsize"])
    return {"name": "test"}

@app.route("/maze/photo")
def takePhotoWithPython():
    
    return 0


if __name__ == "__main__":
    app.run()