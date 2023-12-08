# updated 16 November 2023
# This module uses threading to run both the server and the website from one terminal, with one command/click

import atexit
import threading
import subprocess
import ctypes
from datetime import datetime
import webbrowser

LOGFILE = "log.txt"
HIDE_OUTPUT = False

def log(msg: str):
    """Log a message to the log file defined by the LOGFILE constant

    Args:
        msg (str): the message to log
    """
    prefix = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    with open(LOGFILE, "a") as f:
        f.write(f"[{prefix}] {msg}\n")

# adapted from https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
class EndableThread(threading.Thread):
    """Subclass of Thread to add method for killing the thread directly"""
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
    
    def getID(self) -> int:
        """Get the thread's ID

        Returns:
            int: the ID
        """
        if hasattr(self, "_thread_id"):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    
    def end(self):
        """Kill this thread"""
        thread_id = ctypes.c_long(self.getID())
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, None)
            log(f"[ERROR] Failed to end thread: {self.name}")
            raise SystemError("PyThreadState_SetAsyncExc failed")
        log(f"[End] {self.name}")

def exit_handler():
    """Handle program exit by killing all threads"""
    for t in threads:
        t.end()
    print("Program Terminated.")

def server():
    """Start server"""
    log("[Start] Server")
    subprocess.call(["python", "flaskServe.py"], **kwargs)

def website():
    """Start website"""
    log("[Start] WebInterface")
    # subprocess.call(["gui\\start.bat"], **kwargs) # new NextJS site
    subprocess.call(["gooey\\start.bat"], **kwargs) # old Create-React-App site (framework is deprecated)

def openBrowser():
    """Open the browser to the localhost address hosted by the server"""
    webbrowser.open_new("http://localhost:3000")

if __name__ == "__main__":
    # register the exit handler
    atexit.register(exit_handler)
    
    threads: list[EndableThread] = []
    
    if HIDE_OUTPUT:
        kwargs = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
        }
    else:
        kwargs = {}
    
    # create threads
    threads.append(EndableThread(target = server, name = "ServerThread", daemon = True))
    threads.append(EndableThread(target = website, name = "WebInterfaceThread", daemon = True))
    
    # start threads
    for t in threads:
        t.start()
        print(f"{t.name} started")
    
    print("Press CTRL+C to quit")
    # wait 1 second then open the browser
    threading.Timer(1, openBrowser).start()
    while True:
        # loop to avoid exits that don't cause a KeyboardInterrupt error
        # other exits will call the exit handler but not actually kill the threads
        input("")