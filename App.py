# updated 19 October 2022
# tkinter App allowing user to set config options for challenge generation

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import sys
import json
from pathlib import Path
import subprocess

from MazeGeneration.Maze import Maze
from MazeGeneration.generate import generate
from opencv.gridcapture import screenshot
from opencv.gridReaderFinal import GridReader
from runCommands.refocus import setFocus

class MazeFrame(tk.Frame):
    """Frame containing maze-specific config options"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.false = tk.BooleanVar()
        self.light = tk.BooleanVar()

        cb1 = tk.Checkbutton(self, text = "False Paths", variable = self.false)
        cb1.grid(row = 0, column = 0)
        cb2 = tk.Checkbutton(self, text = "Light", variable = self.light)
        cb2.grid(row = 0, column = 1)

    def resolve(self):
        """Return a dict containing all the config values"""
        return {"falsePaths": self.false.get(), "light": self.light.get()}

    def load(self, options: dict):
        """Load default config values"""
        self.false.set(options["falsePaths"])
        self.light.set(options["light"])

class SoundFrame(tk.Frame):
    """Frame containing soundPuzzle-specific config options"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
    
    def resolve(self):
        """Return a dict containing all the config values"""
        return {}
    
    def load(self, options: dict):
        """Load default config values"""
        pass

class App(tk.Tk):
    """Minecraft Challenge Generator"""
    def __init__(self):
        super().__init__()
        self.title("Minecraft Challenge Generation")
        self.resizable(0, 0)
        self.config(borderwidth = 3, relief = "ridge")

        self._setup()
        self._load()

        self.protocol("WM_DELETE_WINDOW", sys.exit)
        self.mainloop()

    def _setup(self):
        """Set up window"""
        self.x = tk.IntVar()
        self.y = tk.IntVar()
        self.z = tk.IntVar()
        self.puzzleType = tk.StringVar()
        self.photo = tk.BooleanVar()

        self.puzzleTypes = ["Maze", "Sound Puzzle"]

        # coordinate entries
        l3 = tk.Label(self, text = "North-West Corner x,y,z")
        l3.grid(row = 2, column = 0, sticky = "w")
        f = tk.Frame(self)
        f.grid(row = 2, column = 1)
        # x
        num1 = tk.Entry(f, width = 5, textvariable = self.x)
        num1.config(validate = "key", vcmd = (num1.register(self._validate), "%s", "%S", "%d"))
        num1.grid(row = 0, column = 0)
        # y
        num2 = tk.Entry(f, width = 5, textvariable = self.y)
        num2.config(validate = "key", vcmd = (num2.register(self._validate), "%s", "%S", "%d"))
        num2.grid(row = 0, column = 1)
        # z
        num3 = tk.Entry(f, width = 5, textvariable = self.z)
        num3.config(validate = "key", vcmd = (num3.register(self._validate), "%s", "%S", "%d"))
        num3.grid(row = 0, column = 2)

        # puzzle type selector
        l4 = tk.Label(self, text = "Puzzle Type")
        l4.grid(row = 3, column = 0, sticky = "w")
        combo1 = ttk.Combobox(self, state = "readonly", textvariable = self.puzzleType)
        combo1["values"] = self.puzzleTypes
        combo1.bind("<<ComboboxSelected>>", self._loadframe)
        combo1.grid(row = 3, column = 1)

        # photo selector
        l5 = tk.Label(self, text = "Take New Image")
        l5.grid(row = 4, column = 0, sticky = "w")
        chb = tk.Checkbutton(self, variable = self.photo)
        chb.grid(row = 4, column = 1)

        # config frames - gridded later in _loadframe()
        self.mazeFrame = MazeFrame(self)
        self.soundFrame = SoundFrame(self)

        # generate button
        b = tk.Button(self, text = "Generate", command = self.done)
        b.grid(row = 6, column = 0, columnspan = 2)

    def _load(self):
        """Load existing config"""
        try:
            fhand = open("config.json")
            data = json.loads(fhand.read())
            fhand.close()
        except FileNotFoundError:
            return
        finally:
            self.puzzleType.set("Maze")
            self._loadframe()

        self.x.set(data["coords"]["x"])
        self.y.set(data["coords"]["y"])
        self.z.set(data["coords"]["z"])
        self.mazeFrame.load(data["mazeOptions"])
        self.soundFrame.load(data["soundOptions"])

    def _loadframe(self, event = None):
        """Grid the appropriate challenge-dependent frame gui options"""
        if self.puzzleType.get() == "Maze":
            self.soundFrame.grid_forget()
            self.mazeFrame.grid(row = 5, column = 0, columnspan = 2)
        elif self.puzzleType.get() == "Sound Puzzle":
            self.mazeFrame.grid_forget()
            self.soundFrame.grid(row = 5, column = 0, columnspan = 2)

    def _validate(self, prevStr, inStr, actTyp):
        """Validation function to allow only negative sign and numeric values"""
        if actTyp == "1":
            if not inStr.isnumeric() and inStr != "-":
                return False
            if inStr == "-" and prevStr != "":
                return False
        return True

    def _sourcePath(self) -> str:
        """Build mcfunction source path"""
        p = Path().resolve() / f"build.mcfunction"
        return str(p)

    def done(self):
        """Begin generation process, called by button
        Just saves the config options, then calls the actual generation"""

        data = {
            "coords": {
                "x": self.x.get(),
                "y": self.y.get(),
                "z": self.z.get()
            },
            "mazeOptions": self.mazeFrame.resolve(),
            "soundOptions": self.soundFrame.resolve()
        }
        with open("config.json", "w") as f:
            json.dump(data, f, indent = 4)

        self._generate()
    
    def _generate(self):
        """Read image and call appropriate generate function for puzzle type"""

        size = 15

        if self.photo.get():
            grid = screenshot(size)
        else:
            gr = GridReader("opencv_frame_0.png", size)
            grid = gr.readGrid()

        if type(grid) is str or len(grid) != size:
            messagebox.showerror("Grid Capture", "Grid was not captured correctly")
            return

        coords = (self.x.get(), self.y.get(), self.z.get())

        try:
            if self.puzzleType.get() == "Maze":
                maze = Maze(grid)
                cmdCoords = (self.x.get() + maze.max_x + 5, self.y.get() + 1, self.z.get() + maze.max_y)
                cmdDirection = (0, -1)
                generate(maze, coords, cmdCoords, cmdDirection, f"build.mcfunction", **self.mazeFrame.resolve())
            
            elif self.puzzleType.get() == "Sound Puzzle":
                pass

            setFocus(".*Minecraft.*")
            subprocess.call(["runCommands\\runCommands.exe", "build.mcfunction"])
        
        except AssertionError:
            messagebox.showerror("Maze Generation", "Maze generation threw error: " + sys.exc_info()[1].args[0])
            return
        
        print("Complete")
        sys.exit()