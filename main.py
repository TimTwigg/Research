# updated 5 June 2023

import atexit
import threading
import subprocess
import ctypes
from datetime import datetime
import webbrowser

LOGFILE = "log.txt"

def log(msg: str):
    prefix = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    with open(LOGFILE, "a") as f:
        f.write(f"[{prefix}] {msg}\n")

# adapted from https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
class EndableThread(threading.Thread):
    def getID(self) -> int:
        if hasattr(self, "_thread_id"):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    
    def end(self):
        thread_id = ctypes.c_long(self.getID())
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, None)
            log(f"[ERROR] Failed to end thread: {self.name}")
            raise SystemError("PyThreadState_SetAsyncExc failed")
        log(f"[End] {self.name}")

def exit_handler():
    for t in threads:
        t.end()
    print("Program Terminated.")

def server():
    log("[Start] Server")
    subprocess.call(["python", "flaskServe.py"], **kwargs)

def website():
    log("[Start] WebInterface")
    subprocess.call(["gooey\\start.bat"], **kwargs)

def openBrowser():
    webbrowser.open_new("http://localhost:3000")

if __name__ == "__main__":
    atexit.register(exit_handler)
    
    threads: list[EndableThread] = []
    
    kwargs = {
        "stdin": subprocess.PIPE,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
    }
    
    threads.append(EndableThread(target = server, name = "ServerThread", daemon = True))
    threads.append(EndableThread(target = website, name = "WebInterfaceThread", daemon = True))
    
    for t in threads:
        t.start()
    
    print("Server Started")
    print("Web Interface started")
    print("Press CTRL+C to quit")
    threading.Timer(1, openBrowser).start()
    while True:
        # loop to avoid exits that don't cause a KeyboardInterrupt error
        # other exits will call the exit handler but not actually kill the threads
        input("")