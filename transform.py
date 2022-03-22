# updated 22 March 2022
# transform plain maze into correct protocol and generate false paths

#maze = [
#    [0,0,0,0,0,0,0,0,0,1],
#    [0,0,0,0,0,0,0,0,0,1],
#    [0,0,1,1,1,1,1,1,0,1],
#    [0,0,1,0,0,0,0,1,0,1],
#    [0,0,1,1,1,1,0,1,0,1],
#    [0,0,0,0,0,1,0,1,0,1],
#    [1,1,1,1,0,1,0,1,1,1],
#    [1,0,0,1,0,1,0,0,0,0],
#    [1,0,0,1,1,1,0,0,0,0],
#    [1,0,0,0,0,0,0,0,0,0],
#]

from Maze import Maze, DIR

def transform(maze: Maze) -> Maze:
    assert maze.isPath(0, maze.max_y-1, path_codes = [1]), "Maze must start in bottom left corner"
    maze.set(0, maze.max_y-1, 8)
    pos = (0, maze.max_y-1)
    visited = [pos]

    while True:
        neighbours = [n for n in maze.getNeighbours(*pos) if maze.isPath(*n, DIR.HERE, [1]) and n not in visited]
        if len(neighbours) == 0:
            maze.set(*pos, 9)
            break

        elif len(neighbours) > 1:
            print("ERROR", neighbours)
            break

        n = neighbours[0]
        d = None
        if n[0] == pos[0]:
            d = DIR.UP if n[1] < pos[1] else DIR.DOWN
        elif n[1] == pos[1]:
            d = DIR.LEFT if n[0] < pos[0] else DIR.RIGHT
        
        if not maze.isPath(*n, d, [1]):
            maze.set(*pos, 2)
        
        pos = n
        visited.append(pos)

    for n in [i for i in maze.getNeighbours(*pos) if maze.isPath(*i, DIR.HERE, [2])]:
        maze.set(*n, 1)

    return maze

def generateFalsePaths(maze: Maze) -> Maze:
    m = Maze([
        [3,1,1,1,1,3,0,0,0,9],
        [0,1,0,1,0,0,3,0,0,1],
        [0,3,1,1,1,1,2,1,3,1],
        [0,0,2,0,0,0,0,1,0,1],
        [3,1,1,2,1,1,0,1,0,1],
        [0,0,3,0,0,2,0,2,0,1],
        [1,1,2,1,0,1,0,1,2,1],
        [2,0,0,2,0,1,0,0,1,0],
        [1,0,0,1,2,1,0,0,1,0],
        [8,0,0,0,0,3,1,1,1,0],
    ])
    return m