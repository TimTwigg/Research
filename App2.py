# updated 23 October 2022

###########################################################

# Create an App object, then simply call the appropriate puzzle function
# each time a signal is recieved

# This is a controller to link the listener and the generation modules.

###########################################################

import subprocess
from MazeGeneration.Maze import Maze
from MazeGeneration.generate import generate
from opencv.gridcapture import screenshot
from runCommands.refocus import setFocus

class App:    
    def __init__(self):
        self._grid_size = 15
        self._x = 0
        self._y = -50
        self._z = 0
        self._grid = None
        self._commands = []
    
    def captureGrid(self):
        self._grid = screenshot(self._grid_size)
    
    def callMaze(self):
        self.captureGrid()
        maze = Maze(self._grid)
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