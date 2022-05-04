# code for testing the soundpuzzle generation, this is not part of the main program

import json

class Tester:
    def __init__(self, path):
        self.grid = 0
        self.path = path
        with(open(path)) as f:
            self.data = json.load(f)
    
    def getGrid(self):
        if (self.grid == 0):
            return self.data["setup"]
        else:
            return self.data[str(self.grid)]
        self.grid += 1