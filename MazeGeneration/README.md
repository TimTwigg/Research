# Maze Generator

## Usage

The recommended way to use this module is to not use it. The ./../PuzzleGenerator
class is set up to use this and is the recommended way to access Maze generation.

## The Files

- `generate.py` is the access point. It is responsible for generating the MC commands
to create a maze. The `generate()` function defined inside is the only function which
should be called from outside this module. The function docstring describes usage.
- `transform.py` defines transformation functions to transform the 2D grid with defined
path into the form required by `generate()`.
- `Maze.py` defines the Maze object used to wrap the grid and some functionality associated
with it.