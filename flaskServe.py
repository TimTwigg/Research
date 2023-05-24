from pathlib import Path
import sys
sys.path.append(str(Path().absolute() / "Flask"))
from flask import Flask, request
from flask_cors import CORS
from PuzzleGenerator import PuzzleGenerator

app = Flask(__name__)
CORS(app)

@app.route("/data/")
def test():
    gridsize = request.args.get("gridsize")
    deviceID = request.args.get("deviceID")
    falsePaths = request.args.get("falsePaths")
    PG.setSize(gridsize)
    PG.captureGrid()
    PG.releaseCamera()
    # TODO
    return {}

if __name__ == "__main__":
    PG = PuzzleGenerator()
    app.run()