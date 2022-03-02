# updated 2 March 2022
# generate mc commands from Maze

from Maze import Maze

commands = []

def generateCommands(maze: Maze, coords: tuple[int], cmdCoords: tuple[int], cmdDirection: tuple[int]):
    pass

def generate(maze: Maze, coords: tuple[int], cmdCoords: tuple[int], cmdDirection: tuple[int], filename: str):
    generateCommands(maze, coords, cmdCoords, cmdDirection)
    with open(filename, "w") as f:
        f.write("\n".join(commands))