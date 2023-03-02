# updated 1 March 2023

###########################################################

# Create an App object, then simply call the appropriate puzzle function
# each time a signal is recieved

# This is a controller to link the listener and the generation modules.

###########################################################

import subprocess
import cv2
# import re

from MazeGeneration.Maze import Maze
from MazeGeneration.generate import generate
from runCommands.refocus import setFocus
import opencv.gridReaderFinal as gr

class App:    
    def __init__(self, board_size:int = 15):
        self._grid_size = board_size
        self._x = 0
        self._y = -50
        self._z = 0
        self._grid = None
        self._commands = []
        self.hasCamera = False
        self.gotBlank = False
        
    def __del__(self):
        self.releaseCamera()
        
    def grabCamera(self):
        self._cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.hasCamera = True
        print("Grabbed Camera")
        
    def releaseCamera(self):
        self._cam.release()
        self.hasCamera = False
        print("Released Camera")
        
    def takeImage(self, imgName):
        if not self.hasCamera:
            self.grabCamera()
        ret, frame = self._cam.read()
        if not ret:
            print("Failed to find camera")
            return
        
        cv2.imwrite(imgName, frame)
        
        if imgName == "blank.png":
            self.gotBlank = True
    
    def captureGrid(self):
        self.takeImage("path.png")
        reader = gr.GridReader("path.png", "blank.png", self._grid_size)
        grid = reader.readGrid()
        self._grid = grid.tolist()
    
    def callMaze(self):
        self.captureGrid()
        maze = Maze(self._grid)
        print(maze)
        coords = (self._x, self._y, self._z)
        cmdCoords = (self._x + maze.max_x + 5, self._y + 1, self._z + maze.max_y)
        cmdDirection = (0, -1)
        
        commands = generate(maze, coords, cmdCoords, cmdDirection, {"falsePaths": True, "light": False})
        
        # compare old commands with new ones to only execute the difference
        # the command block commands are compared this way, the commands which build the actual maze all have to
        # be run to allow for a different generation of false paths with the new user-defined path
        # to_execute = []
        # for c in commands:
        #     if re.search("fill [-0-9]+ [-0-9]+ [-0-9]+ [-0-9]+ [-0-9]+ [-0-9]+ black_concrete", c) != None:
        #         to_execute.append(c)
        #         break
        #     if c not in self._commands:
        #         to_execute.append(c)
        
        with open("build.mcfunction", "w") as f:
            f.write("\n".join(commands))
        
        setFocus(".*Minecraft.*")
        subprocess.call(["runCommands\\runCommands.exe", "build.mcfunction"])
        
        self._commands = commands
        
    def callSound(self):
        pass