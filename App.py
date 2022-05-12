# updated 12 May 2022

import tkinter as tk
from tkinter import messagebox
import sys
import json
import shutil
from pathlib import Path

from MazeGeneration.Maze import Maze
from MazeGeneration.generate import generate
from opencv.gridReaderFinal import GridReader

class App(tk.Tk):
    """Minecraft Maze Generator"""
    def __init__(self):
        super().__init__()
        self.title("Minecraft Maze Generation")
        self.resizable(0, 0)
        self.config(borderwidth = 3, relief = "ridge")

        self._setup()
        self._load()

        self.protocol("WM_DELETE_WINDOW", sys.exit)
        self.mainloop()

    def _setup(self):
        """Set up window"""
        self.mcpath = tk.StringVar()
        self.save = tk.StringVar()
        self.func = tk.StringVar()
        self.x = tk.IntVar()
        self.y = tk.IntVar()
        self.z = tk.IntVar()
        self.false = tk.BooleanVar()
        self.light = tk.BooleanVar()

        l1 = tk.Label(self, text = "MC Path")
        l1.grid(row = 0, column = 0, sticky = "w")
        e1 = tk.Entry(self, textvariable = self.mcpath)
        e1.grid(row = 0, column = 1)

        l2 = tk.Label(self, text = "MC World Name")
        l2.grid(row = 1, column = 0, sticky = "w")
        e2 = tk.Entry(self, textvariable = self.save)
        e2.grid(row = 1, column = 1)

        l3 = tk.Label(self, text = "Function Name")
        l3.grid(row = 2, column = 0, sticky = "w")
        e3 = tk.Entry(self, textvariable = self.func)
        e3.grid(row = 2, column = 1)

        l4 = tk.Label(self, text = "North-West Corner x,y,z")
        l4.grid(row = 3, column = 0, sticky = "w")
        f = tk.Frame(self)
        f.grid(row = 3, column = 1)

        num1 = tk.Entry(f, width = 5, textvariable = self.x)
        num1.config(validate = "key", vcmd = (num1.register(self._validate), "%s", "%S", "%d"))
        num1.grid(row = 0, column = 0)

        num2 = tk.Entry(f, width = 5, textvariable = self.y)
        num2.config(validate = "key", vcmd = (num2.register(self._validate), "%s", "%S", "%d"))
        num2.grid(row = 0, column = 1)

        num3 = tk.Entry(f, width = 5, textvariable = self.z)
        num3.config(validate = "key", vcmd = (num3.register(self._validate), "%s", "%S", "%d"))
        num3.grid(row = 0, column = 2)

        cb1 = tk.Checkbutton(self, text = "False Paths", variable = self.false)
        cb1.grid(row = 4, column = 0)
        cb2 = tk.Checkbutton(self, text = "Light", variable = self.light)
        cb2.grid(row = 4, column = 1)

        b = tk.Button(self, text = "Generate", command = self.done)
        b.grid(row = 5, column = 0, columnspan = 2)

    def _load(self):
        """Load existing config"""
        fhand = open("config.json")
        data = json.loads(fhand.read())
        fhand.close()
        self.mcpath.set(data["mcpath"])
        self.save.set(data["save"])
        self.func.set(data["func"])
        self.x.set(data["coords"]["x"])
        self.y.set(data["coords"]["y"])
        self.z.set(data["coords"]["z"])
        self.false.set(True)
        self.light.set(False)

    def _validate(self, prevStr, inStr, actTyp):
        if actTyp == "1":
            if not inStr.isnumeric() and inStr != "-":
                return False
            if inStr == "-" and prevStr != "":
                return False
        return True

    def _functionPath(self) -> str:
        """Build function path from provided MC path and world name"""
        return f"{self.mcpath.get()}\\saves\\{self.save.get()}\\datapacks\\maze\\data\\{self.func.get()}\\functions"

    def _metaPath(self) -> str:
        """Build meta pack path from provided MC path and world name"""
        return f"{self.mcpath.get()}\\saves\\{self.save.get()}\\datapacks\\maze\\pack.mcmeta"

    def _sourcePath(self) -> str:
        """Build mcfunction source path"""
        p = Path().resolve() / f"{self.func.get()}.mcfunction"
        return str(p)

    def _make_path(self):
        """Create directory tree and meta pack"""
        PACKMETA = {
            "pack": {
                "pack_format": 1,
                "description": self.func.get()
            }
        }

        Path(self._functionPath()).mkdir(parents = True, exist_ok = True)
        if not Path(self._metaPath()).exists():
            with open(self._metaPath(), "w+") as f:
                json.dump(PACKMETA, f, indent = 4)

    def done(self):
        """Begin generation process, called by button"""
        if len(self.mcpath.get()) < 1 or len(self.save.get()) < 1 or len(self.func.get()) < 1:
            messagebox.showerror("Generation Error", "All fields are required")
            return
        elif not Path(self.mcpath.get()).exists():
            messagebox.showerror("MC Path", "Could not find Minecraft")
            return
        elif not Path(f"{self.mcpath.get()}\\saves\\{self.save.get()}").exists():
            messagebox.showerror("MC World", "Could not find Minecraft world")
            return

        data = {
            "mcpath": self.mcpath.get(),
            "save": self.save.get(),
            "func": self.func.get(),
            "coords": {
                "x": self.x.get(),
                "y": self.y.get(),
                "z": self.z.get()
            }
        }
        with open("config.json", "w") as f:
            json.dump(data, f, indent = 4)

        self._make_path()
        self._generate()
    
    def _generate(self):
        """Call generate function and move mcfunction file"""
        with open("data.json", "r") as f:
            data = json.loads(f.read())
        maze = Maze(data["maze"])

        coords = (self.x.get(), self.y.get(), self.z.get())
        cmdCoords = (self.x.get() + maze.max_x + 5, self.y.get() + 1, self.z.get() + maze.max_y)
        cmdDirection = (0, -1)

        generate(maze, coords, cmdCoords, cmdDirection, f"{self.func.get()}.mcfunction", light = self.light.get(), falsePaths = self.false.get())
        shutil.move(self._sourcePath(), self._functionPath() + f"\\{self.func.get()}.mcfunction")
        sys.exit()