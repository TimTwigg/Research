from Maze import Maze
from generate import generate
import shutil

if __name__ == "__main__":
    maze = [
        [0,0,0,0,0,0,0,0,0,1],
        [0,0,0,0,0,0,0,0,0,1],
        [0,0,1,1,1,1,1,1,0,1],
        [0,0,1,0,0,0,0,1,0,1],
        [0,0,1,1,1,1,0,1,0,1],
        [0,0,0,0,0,1,0,1,0,1],
        [1,1,1,1,0,1,0,1,1,1],
        [1,0,0,1,0,1,0,0,0,0],
        [1,0,0,1,1,1,0,0,0,0],
        [1,0,0,0,0,0,0,0,0,0],
    ]
    
    m = Maze(maze)
    generate(m, (0, 100, 0), (20, 101, 10), (0, -1), "test.mcfunction")
    shutil.move("G:\\My Drive\\UCI\\Research\\Code\\test.mcfunction", "D:\\.minecraft\\saves\\functions\\datapacks\\test\\data\\test\\functions\\test.mcfunction")
    print("Complete")
