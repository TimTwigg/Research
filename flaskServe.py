from pathlib import Path
import sys
import os
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

# https://stackoverflow.com/questions/35851281/python-finding-the-users-downloads-folder
def get_download_path() -> str:
    """Returns the default downloads path for linux or windows"""
    if os.name == "nt":
        import winreg
        sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        downloads_guid = "{374DE290-123F-4565-9164-39C4925E467B}"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser("~"), "downloads")

app = Flask(__name__)
CORS(app)

@app.route("/data/")
def test():
    log(f"<REQUEST> {request.url}")
    
    # get params from request
    gridsize = int(request.args.get("gridsize"))
    falsePaths = request.args.get("falsePaths")
    lightMode = request.args.get("lightMode")
    reset = request.args.get("reset")
    filename = request.args.get("filename")
    # analze params from strings
    falsePaths = falsePaths is None or falsePaths.lower() == "true" # falsePaths defaults to True
    lightMode = lightMode is not None and lightMode.lower() == "true" # lightMode defaults to False
    reset = reset is not None and reset.lower() == "true" # reset defaults to False
    
    # convert filename
    downloadPath = get_download_path()
    filename = f"{downloadPath}/{filename}"
    
    if reset:
        PG.setBlank(filename)
        return {}
    
    # call PuzzleGenerator
    PG.setSize(gridsize)
    try:
        PG.callMaze(filename, falsePaths, lightMode)
    except UnboundLocalError:
        return Response(status=500)
    return {}

if __name__ == "__main__":
    PG = PuzzleGenerator()
    app.run()