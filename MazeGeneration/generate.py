# updated 13 May 2022
# generate mc commands from Maze

from MazeGeneration.Maze import Maze, DIR
from enum import Enum
from MazeGeneration.transform import transform, generateFalsePaths

def _generateCommands(maze: Maze, coords: tuple[int], cmdCoords: tuple[int], cmdDirection: tuple[int]) -> list[str]:
    assert len(coords) == 3, "Coords must have x, y, and z values"
    assert len(cmdCoords) == 3, "cmdCoords must have x, y, and z values"
    assert len(cmdDirection) == 2, "cmdDirection must have x and z values"

    x, y, z = coords
    commands = [f"fill {x-1} {y} {z-1} {x+maze.max_x} {y+3} {z+maze.max_y} {Blocks.WALL.value}"]

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

    # platform outside start with button
    commands.append(f"fill {x-1} {y} {z + maze.max_y + 1} {x+1} {y} {z + maze.max_y + 3} stone")
    commands.append(f"setblock {x} {y + 1} {z + maze.max_y + 1} stone")
    commands.append(f"setblock {x} {y + 1} {z + maze.max_y + 2} oak_button[facing=south] destroy")
    commands.append(f"setblock {x} {y} {z + maze.max_y + 1} command_block[facing=down]{{Command: 'execute as @p if entity @p[tag=!admin] at @s run tag @s add darkRoom'}} destroy")
    commands.append(f"setblock {x} {y - 1} {z + maze.max_y + 1} chain_command_block[facing=down]{{Command: 'execute as @p[tag=darkRoom] at @s run setblock {START_SWITCH[0]} {START_SWITCH[1]} {START_SWITCH[2]} redstone_block', auto:1b}} destroy")
    commands.append("kill @e[type=item]")

    # clone maze to above for use in reset chain
    commands.append(f"clone {x-1} {y} {z-1} {x+maze.max_x} {y+3} {z+maze.max_y} {x-1} {y+4} {z-1}")

    return commands


def _generateCommandBlocks(maze: Maze, coords: tuple[int], cmdCoords: tuple[int], cmdDirection: tuple[int]) -> list[str]:
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
    
    commands.append("scoreboard objectives add darkRoom dummy")
    commands.append(f"setblock {cmdX - 1*x_} {cmdY} {cmdZ - 1*z_} repeating_command_block[facing={facing}] destroy")
    SOUND_SWITCH = (cmdX - 2*x_, cmdY, cmdZ - 2*z_)

    # sound command blocks
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
    
    ########################################################################
    # command chain blocks

    x, y, z = coords

    # reverse facing direction
    if x_ == 0:
        facing = "south" if z_ < 0 else "north"
    else:
        facing = "east" if x_ < 0 else "west"
    
    # change cmd coords
    cmdX = cmdX - 3*x_
    cmdZ = cmdZ - 3*z_
    x_, z_ = -x_, -z_
    step = (2 if x_ == 0 else 0, 2 if z_ == 0 else 0)

    switchCommands = []

    # game management chain
    commands.append(f"setblock {cmdX} {cmdY} {cmdZ} repeating_command_block[facing={facing}] destroy")
    commands.append(f"setblock {cmdX + 1*x_} {cmdY} {cmdZ + 1*z_} chain_command_block[facing={facing}]{{Command: 'execute as @a[tag=!darkRoomTemp] at @s if block ~ ~-1 ~ {Blocks.PATH_TURN.value} run scoreboard players add @s darkRoom 1', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 2*x_} {cmdY} {cmdZ + 2*z_} chain_command_block[facing={facing}]{{Command: 'execute as @a[tag=!darkRoomTemp] at @s if block ~ ~-1 ~ {Blocks.PATH_TURN.value} run tag @s add darkRoomTemp', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 3*x_} {cmdY} {cmdZ + 3*z_} chain_command_block[facing={facing}]{{Command: 'execute as @a[tag=darkRoomTemp] at @s unless block ~ ~-1 ~ {Blocks.PATH_TURN.value} run tag @s remove darkRoomTemp', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 4*x_} {cmdY} {cmdZ + 4*z_} chain_command_block[facing={facing}]{{Command: 'execute as @a[tag=darkRoomTemp] at @s run setblock ~ ~-1 ~ {Blocks.WALL.value}', auto: 1b}} destroy")
    switchCommands.append((cmdX + 5*x_, cmdY, cmdZ + 5*z_))
    switchCommands.append((cmdX + 6*x_, cmdY, cmdZ + 6*z_))
    commands.append(f"setblock {cmdX + 7*x_} {cmdY} {cmdZ + 7*z_} chain_command_block[facing={facing}]{{Command: 'execute as @a[tag=!falsePath,tag=!admin,tag=darkRoom] at @s if block ~ ~-1 ~ {Blocks.FALSE_TURN.value} run tag @s add falsePath', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 8*x_} {cmdY} {cmdZ + 8*z_} chain_command_block[facing={facing}]{{Command: 'execute as @a[tag=falsePath] at @s unless block ~ ~-1 ~ {Blocks.FALSE_TURN.value} run tag @s remove falsePath', auto: 1b}} destroy")

    cmdX, cmdZ = cmdX + step[0], cmdZ + step[1]
    x_, z_ = -x_, -z_
    if x_ == 0:
        facing = "north" if z_ < 0 else "south"
    else:
        facing = "west" if x_ < 0 else "east"

    # start chain
    commands.append(f"setblock {cmdX} {cmdY} {cmdZ} command_block[facing={facing}] destroy")
    global START_SWITCH
    START_SWITCH = (cmdX - 1*x_, cmdY, cmdZ - 1*z_)
    commands.append(f"setblock {cmdX + 1*x_} {cmdY} {cmdZ + 1*z_} chain_command_block[facing={facing}]{{Command: 'setblock ~{-2*x_} ~ ~{-2*z_} air', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 2*x_} {cmdY} {cmdZ + 2*z_} chain_command_block[facing={facing}]{{Command: 'tp @a[tag=darkRoom,tag=!admin] {x} {y+1} {z + maze.max_y - 1} -180 0', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 3*x_} {cmdY} {cmdZ + 3*z_} chain_command_block[facing={facing}]{{Command: 'setblock {SOUND_SWITCH[0]} {SOUND_SWITCH[1]} {SOUND_SWITCH[2]} redstone_block', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 4*x_} {cmdY} {cmdZ + 4*z_} chain_command_block[facing={facing}]{{Command: 'scoreboard objectives setdisplay sidebar darkRoom', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 5*x_} {cmdY} {cmdZ + 5*z_} chain_command_block[facing={facing}]{{Command: 'execute as @a[tag=darkRoom] at @s run effect give @s night vision 9999 9999'}} destroy")

    cmdX, cmdZ = cmdX + step[0], cmdZ + step[1]

    # end chain
    commands.append(f"setblock {cmdX} {cmdY} {cmdZ} command_block[facing={facing}] destroy")
    END_SWITCH = (cmdX - 1*x_, cmdY, cmdZ - 1*z_)
    commands.append(f"setblock {cmdX + 1*x_} {cmdY} {cmdZ + 1*z_} chain_command_block[facing={facing}]{{Command: 'setblock ~{-2*x_} ~ ~{-2*z_} air', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 2*x_} {cmdY} {cmdZ + 2*z_} chain_command_block[facing={facing}]{{Command: 'setblock {SOUND_SWITCH[0]} {SOUND_SWITCH[1]} {SOUND_SWITCH[2]} air', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 3*x_} {cmdY} {cmdZ + 3*z_} chain_command_block[facing={facing}]{{Command: 'tp @p[tag=darkRoom] {x} {y + 1} {z + maze.max_y + 3}', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 4*x_} {cmdY} {cmdZ + 4*z_} chain_command_block[facing={facing}]{{Command: 'scoreboard players reset @a darkRoom', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 5*x_} {cmdY} {cmdZ + 5*z_} chain_command_block[facing={facing}]{{Command: 'effect clear @a[tag=darkRoom]', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 6*x_} {cmdY} {cmdZ + 6*z_} chain_command_block[facing={facing}]{{Command: 'execute as @a[tag=darkRoom] at @s run tag @s remove darkRoom', auto: 1b}} destroy")
    switchCommands.append((cmdX + 7*x_, cmdY, cmdZ + 7*z_))

    cmdX, cmdZ = cmdX + step[0], cmdZ + step[1]

    # reset chain
    commands.append(f"setblock {cmdX} {cmdY} {cmdZ} command_block[facing={facing}] destroy")
    RESET_SWITCH = (cmdX - 1*x_, cmdY, cmdZ - 1*z_)
    commands.append(f"setblock {cmdX + 1*x_} {cmdY} {cmdZ + 1*z_} chain_command_block[facing={facing}]{{Command: 'setblock ~{-2*x_} ~ ~{-2*z_} air', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 2*x_} {cmdY} {cmdZ + 2*z_} chain_command_block[facing={facing}]{{Command: 'clone {x-1} {y+4} {z-1} {x+maze.max_x} {y+7} {z+maze.max_y} {x-1} {y} {z-1} replace', auto: 1b}} destroy")

    cmdX, cmdZ = cmdX + step[0], cmdZ + step[1]

    # false path chain
    commands.append(f"setblock {cmdX} {cmdY} {cmdZ} command_block[facing={facing}] destroy")
    FALSE_SWITCH = (cmdX - 1*x_, cmdY, cmdZ - 1*z_)
    commands.append(f"setblock {cmdX + 1*x_} {cmdY} {cmdZ + 1*z_} chain_command_block[facing={facing}]{{Command: 'setblock ~{-2*x_} ~ ~{-2*z_} air', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 2*x_} {cmdY} {cmdZ + 2*z_} chain_command_block[facing={facing}]{{Command: 'execute as @a[tag=darkRoom] at @s run playsound block.note_block.cow_bell hostile @s ~ ~ ~', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 3*x_} {cmdY} {cmdZ + 3*z_} chain_command_block[facing={facing}]{{Command: 'setblock {RESET_SWITCH[0]} {RESET_SWITCH[1]} {RESET_SWITCH[2]} redstone_block', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 4*x_} {cmdY} {cmdZ + 4*z_} chain_command_block[facing={facing}]{{Command: 'setblock {START_SWITCH[0]} {START_SWITCH[1]} {START_SWITCH[2]} redstone_block', auto: 1b}} destroy")
    commands.append(f"setblock {cmdX + 5*x_} {cmdY} {cmdZ + 5*z_} chain_command_block[facing={facing}]{{Command: 'scoreboard players reset @a darkRoom', auto:1b}} destroy")

    # commands referencing switches
    # couldn't be set earlier since referenced switch did not exist yet
    a,b,c = switchCommands[2]
    commands.append(f"setblock {a} {b} {c} chain_command_block[facing={facing}]{{Command: 'setblock {RESET_SWITCH[0]} {RESET_SWITCH[1]} {RESET_SWITCH[2]} redstone_block', auto: 1b}} destroy")
    # reverse facing direction
    if x_ == 0:
        facing = "south" if z_ < 0 else "north"
    else:
        facing = "east" if x_ < 0 else "west"
    a,b,c = switchCommands[0]
    commands.append(f"setblock {a} {b} {c} chain_command_block[facing={facing}]{{Command: 'execute as @a[tag=darkRoom,tag=!admin,scores={{darkRoom={id+1}}}] run setblock {END_SWITCH[0]} {END_SWITCH[1]} {END_SWITCH[2]} redstone_block', auto: 1b}} destroy")
    a,b,c = switchCommands[1]
    commands.append(f"setblock {a} {b} {c} chain_command_block[facing={facing}]{{Command: 'execute as @a[tag=!falsePath,tag=!admin,tag=darkRoom] at @s if block ~ ~-1 ~ {Blocks.FALSE_TURN.value} run setblock {FALSE_SWITCH[0]} {FALSE_SWITCH[1]} {FALSE_SWITCH[2]} redstone_block', auto: 1b}} destroy")

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

def generate(maze: Maze, coords: tuple[int], cmdCoords: tuple[int], cmdDirection: tuple[int], filename: str,
        light: bool = False, falsePaths: bool = True) -> None:
    """
    Generates the commands required to create the given maze and prints them to a file.
    Start of maze must be in lower left hand corner of maze (as seen in 2D)
    \n
    params:\n
        maze :: Maze object, only the base path should be marked (with '1') - turn, false path, start, and end markers will be generated\n
        coords :: tuple(x, y, z) North-Western corner of maze (an extra ring of wall will be constructed around the maze)\n
        cmdCoords :: tuple(x, y, z) Position of first block in command block chain\n
        cmdDirection :: tuple(x, z) Direction of command block chain from first block\n
        filename :: str filename to print commands to\n
        light :: bool, change to light mode, default false\n
        falsePaths :: bool, generate false paths, default true
    """
    global Direction, Blocks, TYPES
    class Direction(Enum):
        UP = (0, -5)
        RIGHT = (5, 0)
        DOWN = (0, 5)
        LEFT = (-5, 0)

    class Blocks(Enum):
        PATH = "air"
        PATH_TURN = "coal_block" if not light else "diorite"
        FALSE_TURN = "black_wool"
        WALL = "black_concrete" if not light else "white_concrete"
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

    maze = transform(maze)
    commands = []
    x, y, z = coords
    commands.append(f"fill {x-3} {y-2} {z-3} {x + maze.max_x + 14} {y+8} {z+ maze.max_y + 12} air")
    commands.append("gamerule doDaylightCycle false")   
    commands += _generateCommandBlocks(maze, coords, cmdCoords, cmdDirection)
    if falsePaths:
        maze = generateFalsePaths(maze)
    commands += _generateCommands(maze, coords, cmdCoords, cmdDirection)
    with open(filename, "w") as f:
        f.write("\n".join(commands))