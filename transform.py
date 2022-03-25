# updated 25 March 2022
# transform plain maze into correct protocol and generate false paths

from Maze import Maze, DIR

def transform(maze: Maze) -> Maze:
    assert maze.isPath(0, maze.max_y-1, path_codes = [1]), "Maze must start in bottom left corner"
    maze.set(0, maze.max_y-1, 8)
    pos = (0, maze.max_y-1)
    visited = [pos]

    while True:
        neighbours = [n for n in maze.getNeighbours(*pos) if maze.isPath(*n, DIR.HERE, [1]) and n not in visited]
        if len(neighbours) == 0:
            # no path neighbours means we've reached the end
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
    assert maze.isPath(0, maze.max_y-1, path_codes = [8]), "Maze must start in bottom left corner"
    pos = (0, maze.max_y-1)
    visited = [pos]

    while not maze.isPath(*pos, path_codes=[9]):
        pos = [i for i in maze.getNeighbours(*pos) if maze.isPath(*i, path_codes=[1, 2, 3, 9]) and i not in visited][0]
        visited.append(pos)
    visited.append(pos)

    for pos in visited:
        if maze.get(*pos) in [8, 9]:
            continue
        neighbours = [n for n in maze.getNeighbours(*pos) if n not in visited]
        bad = []
        for n in neighbours:
            ns = maze.getNeighbours(*n)
            for i in ns:
                if i != pos and maze.isPath(*i, path_codes=[1, 2, 3, 8, 9]):
                    bad.append(n)
                    break

        for n in bad:
            neighbours.remove(n)

        for n in neighbours:
            maze.set(*n, 3)
            if maze.get(*pos) == 3:
                maze.set(*pos, 1)
            visited.append(n)

    return maze