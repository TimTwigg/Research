# updated 6 October 2023

from enum import Enum

class Cell:
    """
    Class Cell
    
    A single cell in the Maze
    """
    def __init__(self, x : int, y : int, max: tuple[int], element: int):
        """
        Args:
            x (int): the cell's x coord
            y (int): the cell's y coord
            max (tuple[int]): (x, y) maximum coords in the Maze, effectively the size of the underlying grid
            element (int): the cell type
        """
        self.x = x
        self.y = y
        self.element = element
        self.max_x, self.max_y = max

    def __str__(self) -> str:
        return f"Cell: x({self.x}), y({self.y}), element({self.element}), max({(self.max_x, self.max_y)})"

    def up(self) -> tuple[int]:
        return (self.x, self.y-1) if self.y > 0 else None

    def right(self) -> tuple[int]:
        return (self.x+1, self.y) if self.x < self.max_x-1 else None

    def down(self) -> tuple[int]:
        return (self.x, self.y+1) if self.y < self.max_y-1 else None

    def left(self) -> tuple[int]:
        return (self.x-1, self.y) if self.x > 0 else None

class DIR(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    HERE = 5

class Maze:
    """
    class Maze
    
    Wrapper on 2D maze represented by 2D matrix. Intended for use with generate function in generate.py
    """
    def __init__(self, maze: list[list[int]]):
        """
        Args:
            maze (list[list[int]]): 2D array of lists containing ints. Use 0 as the stock, with the desired path demarcated by 1.
                No turns, false paths, alternate paths, etc should be marked.
        """
        self.maze: dict[tuple[int, int]: Cell] = {}
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

    def isPath(self, x: int, z: int, dir: DIR = DIR.HERE, path_codes = [1,2]) -> bool:
        """Check if the block in the given (x, y) coordinate is a path block

        Args:
            x (int): the x coord
            z (int): the z coord
            dir (DIR, optional): if specified, allows to check the path status of a block adjacent to the current one. Defaults to DIR.HERE.
            path_codes (list, optional): the int cell types accepted as path blocks. Defaults to [1,2].

        Returns:
            bool: True if the block is a path block
        """
        try:
            match dir:
                case DIR.UP:
                    return self.maze[(x, z-1)].element in path_codes
                case DIR.RIGHT:
                    return self.maze[(x+1, z)].element in path_codes
                case DIR.DOWN:
                    return self.maze[(x, z+1)].element in path_codes
                case DIR.LEFT:
                    return self.maze[(x-1, z)].element in path_codes
                case DIR.HERE:
                    return self.maze[(x, z)].element in path_codes
                case _:
                    return False
        except KeyError:
            return False

    def get(self, x: int, z: int, dir: DIR = DIR.HERE) -> int:
        """Get the cell type of a certain cell

        Args:
            x (int): the x coord
            z (int): the z coord
            dir (DIR, optional): allows for the retrieval of an adjacent block's type instead of the current block. Defaults to DIR.HERE.

        Returns:
            int: the int block type
        """
        if x < 0 or z < 0 or x >= self.max_x or z >= self.max_y:
            return None
        match dir:
            case DIR.UP:
                return self.maze[(x, z-1)].element
            case DIR.RIGHT:
                return self.maze[(x+1, z)].element
            case DIR.DOWN:
                return self.maze[(x, z+1)].element
            case DIR.LEFT:
                return self.maze[(x-1, z)].element
            case DIR.HERE:
                return self.maze[(x, z)].element
            case _:
                return None

    def getNeighbours(self, x: int, z: int) -> list[tuple[int]]:
        """Get all neighbors of a block

        Args:
            x (int): the x coord
            z (int): the z coord

        Returns:
            list[tuple[int]]: the list of valid neighbors
        """
        cell = self.getCell(x, z)
        return [i for i in [cell.up(), cell.down(), cell.right(), cell.left()] if i is not None]

    def getCell(self, x: int, z: int) -> Cell:
        """Get a cell from the maze

        Args:
            x (int): the x coord
            z (int): the y coord

        Returns:
            Cell: the Cell in the location
        """
        return self.maze[(x, z)]

    def set(self, x: int, z: int, element: int) -> None:
        """Set the block type of a cell

        Args:
            x (int): the x coord
            z (int): the y coord
            element (int): the block type
        """
        self.maze[(x, z)].element = element

    def go(self, x: int, z: int, dir: DIR) -> tuple[int]:
        """Get the coordinates of a move towards a certain direction

        Args:
            x (int): the starting x coord
            z (int): the starting y coord
            dir (DIR): the direction to move in

        Returns:
            tuple[int]: the coordinates of a 1 unit move in the given direction
        """
        match dir:
            case DIR.UP:
                return (x, z-1)
            case DIR.RIGHT:
                return (x+1, z)
            case DIR.DOWN:
                return (x, z+1)
            case DIR.LEFT:
                return (x-1, z)
            case _:
                return None
