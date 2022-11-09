# sound puzzle generation
# Author: Sam Hansen

from collections import namedtuple

SOUNDNAMES = ["block.note_block.bass","block.note_block.banjo","block.note_block.guitar","block.note_block.pling","block.note_block.harp","block.note_block.bit","block.note_block.xylophone","block.note_block.iron_xylophone","block.note_block.chime","block.note_block.bell","block.note_block.didgeridoo","block.note_block.flute","block.note_block.cow_bell","block.note_block.snare","block.note_block.hat"]
MAX_PITCH = 2.0

Sound = namedtuple('Sound', ['soundname', 'pitch'])

class SoundPuzzle:
    def __init__(self,num: list[list[int]],arrays: list[list[list[int]]]):
        self.num = self.getNum(num)
        self.arrays = arrays
        self.sounds = self.getSounds()
        #self.printSounds()

    def getNum(self,array):
        for i in range(0,len(array)):
            for j in range(0,len(array[i])):
                if array[i][j] == 1:
                    return 15-i
    
    def printSounds(self):
        for x in self.sounds:
            print(x.soundname, x.pitch)
    
    def getRowCol(self,arr: list[list[int]]):
        for i in range(0,len(arr)):
            for j in range(0,len(arr[i])):
                if arr[i][j] == 1:
                    return (14-i, j)
                else:
                    continue
        return (0,0)
    
    def getPitch(self,pitch: int):
        pitch_interval = MAX_PITCH / 15
        return pitch_interval * pitch

    def getSounds(self):
        arr = []
        for x in self.arrays:
            row, col = self.getRowCol(x)
            s = Sound(SOUNDNAMES[col],self.getPitch(row))
            arr.append(s)
        return arr

def generateSP(puzzle: SoundPuzzle, coords: tuple[int]):
    #print("SoundPuzzle Generation")
    #print("Number of sounds: ", puzzle.num)
    #print("Sounds:")
    #puzzle.printSounds()
    assert len(coords) == 3, "Coords must have x, y, z values"

    x, y, z = coords
    commands = []
