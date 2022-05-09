# Maze Generator

## Using the App

The easiest way to generate a maze is to run App by creating an instance of the
App object from App.py. This will start a basic user interface. All fields are
required, though the value of function name is unimportant.

NOTE: the App requires two json files: data.json containing a the matrix, and
config.json containing the default/previous values.

## Generating a Maze File Directly

Create a Maze object (described in Maze.py) with a 2d matrix. Pass the Maze to
the generate function from generate.py. The generate function also requires
(x, y, z) coordinates of the north-western corner for the desired maze location,
(x, y, z) coordinates for the command block circuitry, (x, z) direction values
for the command block chain, and a string filename. Optional parameters: bool
light specifies light mode or dark mode (default False -> dark);
bool falsePaths specifies whether or not to generate false paths (default True).
Using the maze coordinates (x, y, z) for a maze of size (n x m), values for the
circuitry location can be calculated as (x + n + 5, y + 1, z + m). The direction
values will almost always be (0, -1).

## Understanding App

The MC function requires a fairly specific directory path to work. App has
methods which create these paths:
_functionPath is the basic directory path. \n
_metaPath is the location of the mcmeta file which describes the datapack.
_sourcePath evaluates the location of the file running the program, which is
where the mcfunction file will initially be created.
_make_path creates the function path and meta pack file if they do not exist.

Meta pack file is required by minecraft for the datapack. A single file is
required, and no editing should be done to add more functions to the pack.

## Expansion

The App will be expanded to generate other puzzles, such as the sound puzzle.
