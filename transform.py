# updated 5 March 2022
# transform plain maze into correct protocol and generate false paths

from Maze import Maze

def transform(maze: Maze) -> Maze:
    m = Maze([
        [0,0,0,0,0,0,0,0,0,9],
        [0,0,0,3,0,0,3,0,0,1],
        [0,0,1,1,1,1,2,1,0,1],
        [0,0,2,0,0,0,0,1,0,1],
        [0,3,1,2,1,1,0,1,0,1],
        [0,0,3,0,0,2,0,2,0,1],
        [1,1,2,1,0,1,0,1,2,1],
        [2,0,0,2,0,1,0,0,0,0],
        [1,0,0,1,2,1,0,0,0,0],
        [8,0,0,0,0,0,0,0,0,0],
    ])
    return m