# updated 25 March 2022
# generate mc commands from Maze

from Maze import Maze, DIR
from enum import Enum
from transform import transform, generateFalsePaths

class Direction(Enum):
    UP = (0, -5)
    RIGHT = (5, 0)
    DOWN = (0, 5)
    LEFT = (-5, 0)

class Blocks(Enum):
    PATH = "air"
    PATH_TURN = "coal_block"
    FALSE_TURN = "black_wool"
    WALL = "stone"
    START = ""
    END = "end"

TYPES = {
    0 : None,
    1 : Blocks.PATH,
    2 : Blocks.PATH_TURN,
    3 : Blocks.FALSE_TURN,
    8 : Blocks.START,
    9 : Blocks.END
}

def _generateCommands(maze: Maze, coords: tuple[int], cmdCoords: tuple[int], cmdDirection: tuple[int]) -> list[str]:
    assert len(coords) == 3, "Coords must have x, y, and z values"
    assert len(cmdCoords) == 3, "cmdCoords must have x, y, and z values"
    assert len(cmdDirection) == 2, "cmdDirection must have x and z values"

    x, y, z = coords
    commands = [f"fill {x-1} {y} {z-1} {x+maze.max_x} {y+2} {z+maze.max_y} {Blocks.WALL.value}"]

    for _z in range(maze.max_y):
        for _x in range(maze.max_x):
            block_type = TYPES[maze.get(_x, _z)]
            if block_type is None:
                continue

            commands.append(f"fill {x+_x} {y+1} {z+_z} {x+_x} {y+2} {z+_z} air")
            if block_type == Blocks.PATH_TURN or block_type == Blocks.END:
                commands.append(f"setblock {x+_x} {y} {z+_z} {Blocks.PATH_TURN.value}")
            elif block_type == Blocks.FALSE_TURN:
                commands.append(f"setblock {x+_x} {y} {z+_z} {Blocks.FALSE_TURN.value}")
    
    return commands


def _generateCommandBlocks(maze: Maze, cmdCoords: tuple[int], cmdDirection: tuple[int]) -> list[str]:
    assert maze.isPath(0, maze.max_y-1, DIR.HERE, [8]), "Start of maze must be in lower left hand corner"
    assert maze.isPath(0, maze.max_y-2, DIR.HERE) != maze.isPath(1, maze.max_y-1, DIR.HERE), "Must have only one path from start"
    
    SOUND = "block.note_block.banjo hostile"
    commands = []
    visited = []
    id = 0
    cmdX, cmdY, cmdZ = cmdCoords
    x_, z_ = cmdDirection
    pos = (0, maze.max_y-1)

    if x_ == 0:
        facing = "north" if z_ < 0 else "south"
    else:
        facing = "west" if x_ < 0 else "east"

    while True:
        block_type = TYPES[maze.get(*pos)]
        if block_type == Blocks.START or block_type == Blocks.PATH:
            pass
        elif block_type == Blocks.PATH_TURN:
            dir = _findDirection(maze, *pos, visited)
            commands.append(f"setblock {cmdX + id*x_} {cmdY} {cmdZ + id*z_} chain_command_block[facing={facing}]{{Command: 'execute as @a[tag=darkRoomTemp, scores={{darkRoom={id+1}}}] at @s run playsound {SOUND} @s ~{dir[0]} ~ ~{dir[1]}', auto: 1b}} destroy")
            id += 1
        elif block_type == Blocks.END:
            break

        neighbours = [i for i in maze.getNeighbours(*pos) if maze.isPath(*i, DIR.HERE, [1, 2, 9]) and i not in visited]
        assert len(neighbours) > 0, f"No neighbours {pos} {maze.get(*pos)} \n{maze}"
        assert len(neighbours) == 1, f"Too many neighbours {pos} {maze.get(*pos)} \n{maze}"
        pos = neighbours[0]
        visited.append(pos)

    return commands


def _findDirection(maze: Maze, x: int, z: int, visited: list[int]) -> tuple[int]:
    neighbours = maze.getNeighbours(x, z)
    for n in neighbours:
        if n not in visited and TYPES[maze.get(*n)] in [Blocks.PATH, Blocks.PATH_TURN]:
            turns = maze.getNeighbours(*n)
            for t in turns:
                if t not in visited and t != (x,z) and TYPES[maze.get(*t)] in [Blocks.PATH, Blocks.PATH_TURN, Blocks.END]:
                    if (t[0] == n[0]): return Direction.UP.value if t[1] < n[1] else Direction.DOWN.value
                    return Direction.LEFT.value if t[0] < n[0] else Direction.RIGHT.value

def generate(maze: Maze, coords: tuple[int], cmdCoords: tuple[int], cmdDirection: tuple[int], filename: str) -> None:
    """
    Generates the commands required to create the given maze and prints them to a file.
    Start of maze must be in lower left hand corner of maze (as seen in 2D)

    params:
        maze :: Maze object, only the base path should be marked (with '1') - turn, false path, start, and end markers will be generated
        coords :: tuple(x, y, z) North-Western corner of maze (an extra ring of wall will be constructed around the maze)
        cmdCoords :: tuple(x, y, z) Position of first block in command block chain
        cmdDirection :: tuple(x, z) Direction of command block chain from first block
        filename :: str filename to print commands to
    """
    
    maze = transform(maze)
    commands = _generateCommandBlocks(maze, cmdCoords, cmdDirection)
    maze = generateFalsePaths(maze)
    commands += _generateCommands(maze, coords, cmdCoords, cmdDirection)
    with open(filename, "w") as f:
        f.write("\n".join(commands))