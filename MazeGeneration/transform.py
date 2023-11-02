# updated 2 November 2023
# transform plain maze into correct protocol and generate false paths

from copy import deepcopy
from MazeGeneration.Maze import Maze, DIR

def transform(maze: Maze) -> Maze:
    """Transform a plain maze with the true path marked by 1's, designating the appropriate start, end, and turn blocks.

    Args:
        maze (Maze): the plain Maze

    Returns:
        Maze: the transformed Maze
    """
    if not maze.isPath(0, maze.max_y-1, path_codes = [1]):
        maze = fillGap(maze)
    assert maze.isPath(0, maze.max_y-1, path_codes = [1]), "Maze must start in bottom left corner"
    maze.set(0, maze.max_y-1, 8) # set start block
    pos: tuple[int, int] = (0, maze.max_y-1) # set start pos
    visited: list[tuple[int, int]] = [pos]

    while True:
        # get unvisited path-block neighbors
        neighbours = [n for n in maze.getNeighbours(*pos) if maze.isPath(*n, DIR.HERE, [1]) and n not in visited]
        if len(neighbours) == 0:
            # no path neighbours means we've reached the end
            maze.set(*pos, 9)
            break

        elif len(neighbours) > 1:
            # more than 1 unvisited neighbor means the path is malformed
            print("ERROR: ", pos, neighbours)
            break

        # get direction of neighbor from current pos
        n = neighbours[0]
        d = None
        if n[0] == pos[0]:
            d = DIR.UP if n[1] < pos[1] else DIR.DOWN
        elif n[1] == pos[1]:
            d = DIR.LEFT if n[0] < pos[0] else DIR.RIGHT
        
        # if the block in direction d from the neighbor is not a path, then this is the block before a turn
        if not maze.isPath(*n, d, [1]):
            maze.set(*pos, 2)
        
        pos = n
        visited.append(pos)

    # don't set the block before the end as a turn block
    for n in [i for i in maze.getNeighbours(*pos) if maze.isPath(*i, DIR.HERE, [2])]:
        maze.set(*n, 1)

    return maze

def fillGap(maze: Maze) -> Maze:
    """Attempt to fill the gap in a maze which was improperly captured from image along the left hand side.

    Args:
        maze (Maze): the broken maze

    Returns:
        Maze: the fixed maze
    """
    x, z = 0, maze.max_y-1
    if maze.get(x, z) == 1:
        # this function was called when not applicable
        return maze
    m = deepcopy(maze)
    
    while z >= 0:
        m.set(x, z, 1)
        cell = m.getCell(x, z)
        up = m.isPath(*cell.up(), path_codes = [0])
        right = m.isPath(*cell.right(), path_codes = [0])
        if up != right:
            # 1 (and only 1) neighbor is a path - we have filled the gap and joined the path
            # return the edited maze
            return m
        if not up and not right:
            # error: filling this gap creates a malformed maze.
            # return the original maze with no changes
            return maze
        z -= 1
    
    # setting the entire left hand side to path did not help
    # return the original maze with no changes
    return maze

def generateFalsePaths(maze: Maze) -> Maze:
    """Generate false paths on a pure-path Maze

    Args:
        maze (Maze): the Maze object with only the transformed path marked

    Returns:
        Maze: the Maze object with false paths added
    """
    assert maze.isPath(0, maze.max_y-1, path_codes = [8]), "Maze must start in bottom left corner"
    pos: tuple[int, int] = (0, maze.max_y-1)
    visited = [pos]

    # add the whole path to visited
    while not maze.isPath(*pos, path_codes=[9]):
        pos = [i for i in maze.getNeighbours(*pos) if maze.isPath(*i, path_codes=[1, 2, 3, 9]) and i not in visited][0]
        visited.append(pos)
    visited.append(pos)

    # for each block in the path in between the start and end:
    #   get the neighbors of that block which are NOT next to a path
    #   set those neighbor blocks to path code 3
    #   add them to the visited list
    for pos in visited:
        if maze.get(*pos) in [8, 9]:
            continue
        neighbours = [n for n in maze.getNeighbours(*pos) if n not in visited] # neighbors of path block
        bad: list[tuple[int, int]] = [] # neighbors of path block which are adjacent to existing path
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
                # if the current pos is  a false path block, set it to normal path block
                maze.set(*pos, 1)
            visited.append(n)

    return maze