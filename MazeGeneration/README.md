# Maze Generator

## Using the App

The easiest way to generate a maze is to run App by creating an instance of the
App object from ../App.py. This will start a basic user interface. All fields are
required.

NOTE: the App currently requires a data.json file containing a 2d matrix.

## Generating a Maze File Directly (Not Recommended)

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

## mccontroller

This is an old project which is no longer used.