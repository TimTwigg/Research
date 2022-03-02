from mazeGenerator import main
from Maze import Maze
from transform import transform
from generate import generate
import shutil

if __name__ == "__main__":
    maze = [
        [0,0,0,0,0,0,3,0,0,9],
        [0,0,0,3,0,0,1,0,0,1],
        [0,0,1,1,1,1,2,1,0,1],
        [0,0,2,0,0,0,0,1,0,1],
        [0,3,1,2,1,1,0,1,0,1],
        [0,0,3,0,0,2,0,2,0,1],
        [1,1,2,1,0,1,0,1,2,1],
        [2,0,0,2,0,1,0,0,0,0],
        [1,0,0,1,2,1,0,0,0,0],
        [8,0,0,0,0,0,0,0,0,0],
    ]
    #main(maze, (0, 100, 0), (20, 101, 10), (0, -1), "test.mcfunction")
    #shutil.move("G:\\My Drive\\UCI\\Research\\Code\\test.mcfunction", "D:\\.minecraft\\saves\\functions\\datapacks\\test\\data\\test\\functions\\test.mcfunction")
    
    m = Maze(maze)
    m = transform(m)
    generate(m)
    print(m)
    print("Complete")
