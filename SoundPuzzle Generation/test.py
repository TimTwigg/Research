# code for testing the soundpuzzle generation, this is not part of the main program

import json
import main

class Tester:
    def __init__(self, path):
        self.grid = 0
        self.path = path
        with(open(path)) as f:
            self.data = json.load(f)
    
    def getArrays(self):
        keys = list(self.data.keys())
        keys.remove("setup")
        keys.sort()
        array = []
        for x in keys:
            array.append(self.data[x])
        return array

    def getSetup(self):
        return self.data["setup"]

if __name__ == "__main__":
    tester = Tester("/home/eleros/Projects/Minecraft/research/SoundPuzzle Generation/testdata.json")
    puzzle = main.SoundPuzzle(tester.getSetup(), tester.getArrays())