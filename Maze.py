# updated 5 March 2022
from enum import Enum

class Cell:
    def __init__(self, x : int, y : int, max: tuple[int], element):
        self.x = x
        self.y = y
        self.element = element
        self.max_x, self.max_y = max

    def up(self) -> tuple[int]:
        return (self.x, self.y-1) if self.y > 0 else None
    
    def right(self) -> tuple[int]:
        return (self.x+1, self.y) if self.x < self.max_x else None

    def down(self) -> tuple[int]:
        return (self.x, self.y+1) if self.y < self.max_y else None

    def left(self) -> tuple[int]:
        return (self.x-1, self.y) if self.x > 0 else None

class DIR(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    HERE = 5

class Maze:
    def __init__(self, maze: list[list[int]]):
        self.maze = {}
        self.max_x = len(maze[0])
        self.max_y = len(maze)
        for y in range(self.max_y):
            for x in range(self.max_x):
                self.maze[(x,y)] = Cell(x, y, (self.max_x, self.max_y), maze[y][x])
    
    def __str__(self) -> str:
        l = []
        for y in range(self.max_y):
            t = []
            for x in range(self.max_x):
                t.append(self.maze[(x,y)].element)
            l.append(t)
        return "\n".join([" ".join([str(x) if x != 0 else " " for x in t]) for t in l])

    def isPath(self, x: int, y: int, dir: DIR, path_codes = [1,2]) -> bool:
        match dir:
            case DIR.UP:
                return self.maze[(x, y-1)].element in path_codes
            case DIR.RIGHT:
                return self.maze[(x+1, y)].element in path_codes
            case DIR.DOWN:
                return self.maze[(x, y+1)].element in path_codes
            case DIR.LEFT:
                return self.maze[(x-1, y)].element in path_codes
            case DIR.HERE:
                return self.maze[(x, y)].element in path_codes
            case _:
                return False

    def get(self, x: int, y: int, dir: DIR = DIR.HERE) -> int:
        match dir:
            case DIR.UP:
                return self.maze[(x, y-1)].element
            case DIR.RIGHT:
                return self.maze[(x+1, y)].element
            case DIR.DOWN:
                return self.maze[(x, y+1)].element
            case DIR.LEFT:
                return self.maze[(x-1, y)].element
            case DIR.HERE:
                return self.maze[(x, y)].element
            case _:
                return None

    def getCell(self, x: int, y: int) -> Cell:
        return self.maze[(x, y)]

    def set(self, x: int, y: int, element: int) -> None:
        self.maze[(x, y)].element = element

    def go(self, x: int, y: int, dir: DIR) -> tuple[int]:
        match dir:
            case DIR.UP:
                return (x, y-1)
            case DIR.RIGHT:
                return (x+1, y)
            case DIR.DOWN:
                return (x, y+1)
            case DIR.LEFT:
                return (x-1, y)
            case _:
                return None

    def isFalsePath(self, x: int, y: int, dir: DIR) -> bool:
        if self.isPath(x, y, dir):
            x, y = self.go(x, y, dir)
        
        coords = [(x, y)]

        for x,y in coords:
            for d in [DIR.UP, DIR.RIGHT, DIR.DOWN, DIR.LEFT]:
                if self.go(x, y, d) in coords: continue
                elif self.get(x, y, d) == 3:
                    return True
                elif self.get(x, y, d) == 1:
                    coords.append(self.go(x, y, d))
        return False