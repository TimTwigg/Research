from pathlib import Path
import sys
from datetime import datetime
sys.path.append(str(Path().absolute() / "Flask"))
from flask import Flask, request, Response
from flask_cors import CORS
from PuzzleGenerator import PuzzleGenerator

LOGFILE = "log.txt"

def log(msg: str):
    prefix = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    with open(LOGFILE, "a") as f:
        f.write(f"[{prefix}] {msg}\n")

app = Flask(__name__)
CORS(app)

@app.route("/data/")
def test():
    log(f"<REQUEST> {request.url}")
    
    # get params from request
    gridsize = int(request.args.get("gridsize"))
    deviceID = int(request.args.get("deviceID"))
    falsePaths = request.args.get("falsePaths")
    lightMode = request.args.get("lightMode")
    reset = request.args.get("reset")
    # analze params from strings
    falsePaths = falsePaths is None or falsePaths.lower() == "true" # falsePaths defaults to True
    lightMode = lightMode is not None and lightMode.lower() == "true" # lightMode defaults to False
    reset = reset is not None and reset.lower() == "true" # reset defaults to False
    
    # call PuzzleGenerator
    PG.setSize(gridsize)
    PG.grabCamera(deviceID)
    if not PG.gotBlank or reset:
        PG.takeImage("blank.png")
        log("Taken Blank")
        PG.releaseCamera()
    else:
        PG.takeImage("path.png")
        log("Taken Image")
        PG.releaseCamera()
        try:
            PG.callMaze(falsePaths, lightMode)
        except UnboundLocalError:
            # catch "cannot access local variable 'biggest'" error from gridreader.warp
            log("Could not interpret grid from image.")
            return Response(status = 500)
    return {}

if __name__ == "__main__":
    PG = PuzzleGenerator()
    app.run()