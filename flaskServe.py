from pathlib import Path
import sys
sys.path.append(str(Path().absolute() / "Flask"))
from flask import Flask, request
from flask_cors import CORS
import json
from PuzzleGenerator import PuzzleGenerator

app = Flask(__name__)
CORS(app)

@app.route("/data/")
def test():
    # data = json.loads(jsdata)
    gridsize = request.args.get('gridsize')
    deviceID = request.args.get('deviceID')
    print(data["gridsize"])
    return 0

@app.route("/maze/photo")
def takePhotoWithPython():

    
    return 0

if __name__ == "__main__":
    PG = PuzzleGenerator()
    app.run()