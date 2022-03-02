# updated 22 February 2022
# takes a 2d matrix representing the desired maze and the (x,y,z) coordinates of the lower north-west corner of the location
# commands will be generated assuming the top left-hand corner is the north-west corner
# matrix should use:
# 0 as the default 
# 1 to represent path
# 2 for left turn blocks
# 3 for right turn blocks
# 4 for false turn blocks
# 8 for start
# 9 for end
#
# it is assumed that the maze matrix is square
# eg:
# [
#    [0,0,0,0,0,0,3,0,0,9],
#    [0,0,0,3,0,0,1,0,0,1],
#    [0,0,1,1,1,1,2,1,0,1],
#    [0,0,2,0,0,0,0,1,0,1],
#    [0,3,1,2,1,1,0,1,0,1],
#    [0,0,3,0,0,2,0,2,0,1],
#    [1,1,2,1,0,1,0,1,2,1],
#    [2,0,0,2,0,1,0,0,0,0],
#    [1,0,0,1,2,1,0,0,0,0],
#    [8,0,0,0,0,0,0,0,0,0],
#]

PATH = "air"
PATH_TURN = "coal_block"
FALSE_TURN = "black_wool"
WALL = "stone"
START = ""
END = "end"

TYPES = {
    0 : None,
    1 : PATH,
    2 : PATH_TURN,
    3 : FALSE_TURN,
    8 : START,
    9 : END
}

UP = (0, -5)
RIGHT = (5, 0)
DOWN = (0, 5)
LEFT = (-5, 0)

commands = []

def getNeighbours(x : int, y : int, max_x : int, max_y : int) -> list[tuple[int]]:
    out = []
    if (x > 0): out.append((x-1, y))
    if (x < max_x-1): out.append((x+1, y))
    if (y > 0): out.append((x, y-1))
    if (y < max_y-1): out.append((x, y+1))
    out.append(None)
    return out

def generateCommands(maze, coords, cmdCoords, cmdDirection) -> None:
    assert len(coords) == 3, "Must include x, y, and z coordinates"

    x, y, z = coords
    global commands
    commands.append(f"fill {x-1} {y} {z-1} {x+len(maze)} {y+2} {z+len(maze)} {WALL}")

    for _z in range(len(maze)):
        for _x in range(len(maze)):
            block_type = TYPES[maze[_z][_x]]
            if block_type is None:
                continue

            commands.append(f"fill {x+_x} {y+1} {z+_z} {x+_x} {y+2} {z+_z} air")
            if block_type == PATH_TURN or block_type == END:
                commands.append(f"setblock {x+_x} {y} {z+_z} {PATH_TURN}")
            elif block_type == FALSE_TURN:
                commands.append(f"setblock {x+_x} {y} {z+_z} {FALSE_TURN}")
            elif block_type == START:
                generateCommandBlocks(maze, _x, _z, cmdCoords, cmdDirection)

def generateCommandBlocks(maze, mazeX, mazeZ, cmdCoords, cmdDirection):
    cmdX, cmdY, cmdZ = cmdCoords
    x_, z_ = cmdDirection
    pos = (mazeX, mazeZ)
    visited = []
    id = 0
    sound = "block.note_block.banjo hostile"
    global commands

    if x_ == 0:
        facing = "north" if z_ < 0 else "south"
    else:
        facing = "west" if x_ < 0 else "east"

    while True:
        block_type = TYPES[maze[pos[1]][pos[0]]]
        if block_type == START or block_type == PATH:
            pass
        elif block_type == PATH_TURN:
            dir = findDirection(maze, *pos, visited)
            commands.append(f"setblock {cmdX + id*x_} {cmdY} {cmdZ + id*z_} chain_command_block[facing={facing}]{{Command: 'execute as @a[tag=darkRoomTemp, scores={{darkRoom={id+1}}}] at @s run playsound {sound} @s ~{dir[0]} ~ ~{dir[1]}', auto: 1b}} destroy")
            id += 1
        elif block_type == END:
            break

        # change pos
        neighbours = getNeighbours(*pos, len(maze), len(maze))
        for n in neighbours:
            if n not in visited and TYPES[maze[n[1]][n[0]]] in [PATH, PATH_TURN]:
                pos = n
                break
            elif TYPES[maze[n[1]][n[0]]] == END:
                return
        visited.append(pos)


# doesnt work correctly
def findDirection(maze, x, z, visited):
    neighbours = getNeighbours(x, z, len(maze), len(maze))
    for n in neighbours:
        if n not in visited and TYPES[maze[n[1]][n[0]]] == PATH:
            turns = getNeighbours(n[0], n[1], len(maze), len(maze))
            for t in turns:
                if t not in visited and t != (x,z) and TYPES[maze[t[1]][t[0]]] in [PATH, PATH_TURN]:
                    if (t[0] == n[0]): return UP if t[1] < n[1] else DOWN
                    return LEFT if t[0] < n[0] else RIGHT


def writeCommands(filename):
    with open(filename, "w") as f:
        f.write("\n".join(commands))


def main(maze, coords, cmdCoords, cmdDirection, filename):
    generateCommands(maze, coords, cmdCoords, cmdDirection)
    writeCommands(filename)