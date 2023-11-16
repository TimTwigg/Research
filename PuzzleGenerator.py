# updated 16 November 2023

import subprocess
import cv2

from MazeGeneration.Maze import Maze
from MazeGeneration.generate import generate
from runCommands.refocus import setFocus
import opencv.gridReaderFinal as gr

class PuzzleGenerator:
    """Generator for Minecraft Puzzle Generation"""
    def __init__(self, board_size: int = 15):
        """Create a PuzzleGenerator

        Args:
            board_size (int, optional): the length/width of the square grid. Defaults to 15.
        """
        self._grid_size: int = board_size
        self._x: int = 0
        self._y: int = -50
        self._z: int = 0
        self._grid: list[list[int]] = None
        self._commands: list[str] = []
        self.hasCamera: bool = False
        self.gotBlank: bool = False
        self._blank_file_: str = None
        
    def __del__(self):
        try:
            self.releaseCamera()
        except AttributeError:
            pass
    
    def setSize(self, board_size: int):
        """Set/Change the grid board size

        Args:
            board_size (int): the new size
        """
        self._grid_size = board_size
    
    def setBlank(self, filename: str):
        """Set the black filename

        Args:
            filename (str): filename of blank file
        """
        self._blank_file_ = filename
        
    def grabCamera(self, cameraID: int = 0):
        """Grab a camera

        Args:
            cameraID (int, optional): the id of the camera on the local system. Defaults to 0.
        """
        self._cam = cv2.VideoCapture(cameraID, cv2.CAP_DSHOW)
        self.hasCamera = True
        print("Grabbed Camera")
        
    def releaseCamera(self):
        """Release the grabbed camera"""
        self._cam.release()
        self.hasCamera = False
        print("Released Camera")
        
    def takeImage(self, imgName: str):
        """Use the grabbed camera to take an image

        Args:
            imgName (str): the filename to save the image under
        """
        if not self.hasCamera:
            self.grabCamera()
        ret, frame = self._cam.read()
        if not ret:
            print("Failed to find camera")
            return
        
        cv2.imwrite(imgName, frame)
        
        if imgName == "blank.png":
            self.gotBlank = True
    
    def captureGrid(self, imageFile: str):
        """Analyze and read images and set grid attribute."""
        if self._blank_file_ is None:
            raise Exception()
        reader = gr.GridReader(imageFile, self._blank_file_, self._grid_size)
        grid = reader.readGrid()
        self._grid = grid.tolist()
    
    def callMaze(self, imageFile: str, falsePaths: bool = True, lightMode: bool = False):
        """Create a Maze puzzle.

        Args:
            imageFile (str): filename for the image of the path grid
            falsePaths (bool, optional): whether to generate false paths. Defaults to True.
            lightMode (bool, optional): whether to create the maze in light mode. Defaults to False.
        """
        # get the grid from the image
        self.captureGrid(imageFile)
        maze = Maze(self._grid)
        # print the maze to console
        print(maze)
        # create params for generate function
        coords = (self._x, self._y, self._z)
        cmdCoords = (self._x + maze.max_x + 5, self._y + 1, self._z + maze.max_y)
        cmdDirection = (0, -1)
        
        # generate the list of commands
        commands = generate(maze, coords, cmdCoords, cmdDirection, falsePaths, lightMode)
        
        # !!!! DON'T UNCOMMENT !!!!
        # ########################
        # This was an attempt to streamline edits of an existing maze in Minecraft. It is incomplete and will break the maze
        # if any edits were made to the maze as opposed to simple additions.
        #
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
        # ########################
        
        # save commands to file
        with open("build.mcfunction", "w") as f:
            f.write("\n".join(commands))
        
        # change window to Minecraft, then run the commands
        setFocus(".*Minecraft.*")
        subprocess.call(["runCommands\\runCommands.exe", "build.mcfunction"])
        
        self._commands = commands
        
    def callSound(self):
        pass