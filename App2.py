# updated 3 November 2022

###########################################################

# Create an App object, then simply call the appropriate puzzle function
# each time a signal is recieved

# This is a controller to link the listener and the generation modules.

###########################################################

import subprocess
import cv2

from MazeGeneration.Maze import Maze
from MazeGeneration.generate import generate
from runCommands.refocus import setFocus
import opencv.gridReaderFinal as gr

class App:    
    def __init__(self):
        self._grid_size = 15
        self._x = 0
        self._y = -50
        self._z = 0
        self._grid = None
        self._commands = []
        
    def __del__(self):
        self.releaseCamera()
        
    def grabCamera(self):
        self._cam = cv2.VideoCapture(1)
        print("Grabbed Camera")
        
    def releaseCamera(self):
        self._cam.release()
        print("Released Camera")
    
    def captureGrid(self):
        ret, frame = self._cam.read()
        if not ret:
            print("Failed to find camera")
            return
        
        cv2.imwrite("opencv_frame_0.png", frame)
        reader = gr.GridReader("opencv_frame_0.png", self._grid_size)
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
        to_execute = [i for i in commands if i not in self._commands]
        with open("build.mcfunction", "w") as f:
            f.write("\n".join(to_execute))
        
        setFocus(".*Minecraft.*")
        subprocess.call(["runCommands\\runCommands.exe", "build.mcfunction"])
        
        self._commands = commands
        
    def callSound(self):
        pass