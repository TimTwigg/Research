# Sound Generation

This script takes in multiple grids to construct a sound-based combination puzzle.
Grids are 15x15 2d arrays (see testdata.json for examples).
First, it takes in a setup grid, and then takes in 1 grid for each combo thing.

## Setup Grid

Setup grid tells the program how many combos there will be. Minimum 1 and max 15 (limited by grid size).
Place a piece in the row for the number of combos (bottom is 1, top is 15) in the first column.

## Combo Grid

Combo grids are pretty easy. Instrument is x-axis and Pitch is y-axis. Place ONE block on the graph corresponding to the pitch and instrument you want.

| Column | Instrument | Java Name |
|--------|------------|-----------|
| 1 | String Bass | block.note_block.bass |
| 2 | Banjo | block.note_block.banjo |
| 3 | Guitar | block.note_block.guitar |
| 4 | Electric Piano | block.note_block.pling |
| 5 | Normal Piano | block.note_block.harp |
| 6 | Square | block.note_block.bit |
| 7 | Xylo | block.note_block.xylophone | 
| 8 | Iron Xylo | block.note_block.iron_xylophone | 
| 9 | Chimes | block.note_block.chime |
| 10 | Bells | block.note_block.bell |
| 11 | Didgeridoo | block.note_block.didgeridoo | 
| 12 | Flute | block.note_block.flute |
| 13 | Cowbell | block.note_block.cow_bell | 
| 14 | Snare | block.note_block.snare |
| 15 | Hihat | block.note_block.hat |
