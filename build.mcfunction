fill -3 -52 -3 29 -42 27 air
gamerule doDaylightCycle false
gamerule commandBlockOutput false
gamerule doWeatherCycle false
gamerule doTraderSpawning false
scoreboard objectives add darkRoom dummy
setblock 20 -49 16 repeating_command_block[facing=north] destroy
setblock 20 -49 15 chain_command_block[facing=north]{Command: 'execute as @a[tag=darkRoomTemp, scores={darkRoom=1}] at @s run playsound block.note_block.banjo hostile @s ~5 ~ ~0', auto: 1b} destroy
setblock 20 -49 14 chain_command_block[facing=north]{Command: 'execute as @a[tag=darkRoomTemp, scores={darkRoom=2}] at @s run playsound block.note_block.banjo hostile @s ~0 ~ ~-5', auto: 1b} destroy
setblock 20 -49 13 chain_command_block[facing=north]{Command: 'execute as @a[tag=darkRoomTemp, scores={darkRoom=3}] at @s run playsound block.note_block.banjo hostile @s ~5 ~ ~0', auto: 1b} destroy
setblock 20 -49 12 chain_command_block[facing=north]{Command: 'execute as @a[tag=darkRoomTemp, scores={darkRoom=4}] at @s run playsound block.note_block.banjo hostile @s ~0 ~ ~-5', auto: 1b} destroy
setblock 20 -49 11 chain_command_block[facing=north]{Command: 'execute as @a[tag=darkRoomTemp, scores={darkRoom=5}] at @s run playsound block.note_block.banjo hostile @s ~5 ~ ~0', auto: 1b} destroy
setblock 20 -49 18 repeating_command_block[facing=south] destroy
setblock 20 -49 19 chain_command_block[facing=south]{Command: 'execute as @a[tag=!darkRoomTemp] at @s if block ~ ~-1 ~ diorite run scoreboard players add @s darkRoom 1', auto: 1b} destroy
setblock 20 -49 20 chain_command_block[facing=south]{Command: 'execute as @a[tag=!darkRoomTemp] at @s if block ~ ~-1 ~ diorite run tag @s add darkRoomTemp', auto: 1b} destroy
setblock 20 -49 21 chain_command_block[facing=south]{Command: 'execute as @a[tag=darkRoomTemp] at @s unless block ~ ~-1 ~ diorite run tag @s remove darkRoomTemp', auto: 1b} destroy
setblock 20 -49 22 chain_command_block[facing=south]{Command: 'execute as @a[tag=darkRoomTemp] at @s run setblock ~ ~-1 ~ white_concrete', auto: 1b} destroy
setblock 20 -49 25 chain_command_block[facing=south]{Command: 'execute as @a[tag=!falsePath,tag=!admin,tag=darkRoom] at @s if block ~ ~-1 ~ black_wool run tag @s add falsePath', auto: 1b} destroy
setblock 20 -49 26 chain_command_block[facing=south]{Command: 'execute as @a[tag=falsePath] at @s unless block ~ ~-1 ~ black_wool run tag @s remove falsePath', auto: 1b} destroy
setblock 22 -49 18 command_block[facing=north] destroy
setblock 22 -49 17 chain_command_block[facing=north]{Command: 'setblock ~0 ~ ~2 air', auto: 1b} destroy
setblock 22 -49 16 chain_command_block[facing=north]{Command: 'tp @a[tag=darkRoom,tag=!admin] 0 -49 14 -180 0', auto: 1b} destroy
setblock 22 -49 15 chain_command_block[facing=north]{Command: 'setblock 20 -49 17 redstone_block', auto: 1b} destroy
setblock 22 -49 14 chain_command_block[facing=north]{Command: 'scoreboard objectives setdisplay sidebar darkRoom', auto: 1b} destroy
setblock 22 -49 13 chain_command_block[facing=north]{Command: 'execute as @a[tag=darkRoom] at @s run effect give @s night_vision 9999 99', auto: 1b} destroy
setblock 24 -49 18 command_block[facing=north] destroy
setblock 24 -49 17 chain_command_block[facing=north]{Command: 'setblock ~0 ~ ~2 air', auto: 1b} destroy
setblock 24 -49 16 chain_command_block[facing=north]{Command: 'setblock 20 -49 17 air', auto: 1b} destroy
setblock 24 -49 15 chain_command_block[facing=north]{Command: 'tp @p[tag=darkRoom] 0 -49 18', auto: 1b} destroy
setblock 24 -49 14 chain_command_block[facing=north]{Command: 'scoreboard players reset @a darkRoom', auto: 1b} destroy
setblock 24 -49 13 chain_command_block[facing=north]{Command: 'effect clear @a[tag=darkRoom]', auto: 1b} destroy
setblock 24 -49 12 chain_command_block[facing=north]{Command: 'execute as @a[tag=darkRoom] at @s run tag @s remove darkRoom', auto: 1b} destroy
setblock 26 -49 18 command_block[facing=north] destroy
setblock 26 -49 17 chain_command_block[facing=north]{Command: 'setblock ~0 ~ ~2 air', auto: 1b} destroy
setblock 26 -49 16 chain_command_block[facing=north]{Command: 'clone -1 -46 -1 15 -43 15 -1 -50 -1 replace', auto: 1b} destroy
setblock 28 -49 18 command_block[facing=north] destroy
setblock 28 -49 17 chain_command_block[facing=north]{Command: 'setblock ~0 ~ ~2 air', auto: 1b} destroy
setblock 28 -49 16 chain_command_block[facing=north]{Command: 'execute as @a[tag=darkRoom] at @s run playsound block.note_block.cow_bell hostile @s ~ ~ ~', auto: 1b} destroy
setblock 28 -49 15 chain_command_block[facing=north]{Command: 'setblock 26 -49 19 redstone_block', auto: 1b} destroy
setblock 28 -49 14 chain_command_block[facing=north]{Command: 'setblock 22 -49 19 redstone_block', auto: 1b} destroy
setblock 28 -49 13 chain_command_block[facing=north]{Command: 'scoreboard players reset @a darkRoom', auto:1b} destroy
setblock 24 -49 11 chain_command_block[facing=north]{Command: 'setblock 26 -49 19 redstone_block', auto: 1b} destroy
setblock 20 -49 23 chain_command_block[facing=south]{Command: 'execute as @a[tag=darkRoom,tag=!admin,scores={darkRoom=6}] run setblock 24 -49 19 redstone_block', auto: 1b} destroy
setblock 20 -49 24 chain_command_block[facing=south]{Command: 'execute as @a[tag=!falsePath,tag=!admin,tag=darkRoom] at @s if block ~ ~-1 ~ black_wool run setblock 28 -49 19 redstone_block', auto: 1b} destroy
fill -1 -50 -1 15 -47 15 white_concrete
fill 0 -49 0 0 -48 0 air
fill 1 -49 0 1 -48 0 air
fill 2 -49 0 2 -48 0 air
fill 4 -49 0 4 -48 0 air
setblock 4 -50 0 black_wool
fill 5 -49 0 5 -48 0 air
fill 6 -49 0 6 -48 0 air
setblock 6 -50 0 black_wool
fill 12 -49 0 12 -48 0 air
setblock 12 -50 0 black_wool
fill 13 -49 0 13 -48 0 air
fill 14 -49 0 14 -48 0 air
setblock 14 -50 0 black_wool
fill 0 -49 1 0 -48 1 air
setblock 0 -50 1 black_wool
fill 2 -49 1 2 -48 1 air
fill 3 -49 1 3 -48 1 air
setblock 3 -50 1 black_wool
fill 5 -49 1 5 -48 1 air
fill 7 -49 1 7 -48 1 air
setblock 7 -50 1 black_wool
fill 11 -49 1 11 -48 1 air
setblock 11 -50 1 black_wool
fill 13 -49 1 13 -48 1 air
fill 1 -49 2 1 -48 2 air
setblock 1 -50 2 black_wool
fill 2 -49 2 2 -48 2 air
fill 4 -49 2 4 -48 2 air
setblock 4 -50 2 black_wool
fill 5 -49 2 5 -48 2 air
fill 6 -49 2 6 -48 2 air
fill 7 -49 2 7 -48 2 air
fill 8 -49 2 8 -48 2 air
setblock 8 -50 2 black_wool
fill 10 -49 2 10 -48 2 air
setblock 10 -50 2 black_wool
fill 11 -49 2 11 -48 2 air
fill 12 -49 2 12 -48 2 air
fill 13 -49 2 13 -48 2 air
fill 14 -49 2 14 -48 2 air
setblock 14 -50 2 black_wool
fill 0 -49 3 0 -48 3 air
setblock 0 -50 3 black_wool
fill 2 -49 3 2 -48 3 air
fill 3 -49 3 3 -48 3 air
setblock 3 -50 3 black_wool
fill 5 -49 3 5 -48 3 air
fill 7 -49 3 7 -48 3 air
setblock 7 -50 3 black_wool
fill 9 -49 3 9 -48 3 air
setblock 9 -50 3 black_wool
fill 11 -49 3 11 -48 3 air
setblock 11 -50 3 black_wool
fill 13 -49 3 13 -48 3 air
fill 0 -49 4 0 -48 4 air
fill 1 -49 4 1 -48 4 air
fill 2 -49 4 2 -48 4 air
fill 4 -49 4 4 -48 4 air
setblock 4 -50 4 black_wool
fill 5 -49 4 5 -48 4 air
fill 6 -49 4 6 -48 4 air
setblock 6 -50 4 black_wool
fill 8 -49 4 8 -48 4 air
setblock 8 -50 4 black_wool
fill 9 -49 4 9 -48 4 air
fill 10 -49 4 10 -48 4 air
setblock 10 -50 4 black_wool
fill 12 -49 4 12 -48 4 air
setblock 12 -50 4 black_wool
fill 13 -49 4 13 -48 4 air
fill 14 -49 4 14 -48 4 air
setblock 14 -50 4 black_wool
fill 0 -49 5 0 -48 5 air
setblock 0 -50 5 black_wool
fill 2 -49 5 2 -48 5 air
fill 3 -49 5 3 -48 5 air
setblock 3 -50 5 black_wool
fill 5 -49 5 5 -48 5 air
fill 7 -49 5 7 -48 5 air
setblock 7 -50 5 black_wool
fill 9 -49 5 9 -48 5 air
fill 11 -49 5 11 -48 5 air
setblock 11 -50 5 black_wool
fill 13 -49 5 13 -48 5 air
fill 1 -49 6 1 -48 6 air
setblock 1 -50 6 black_wool
fill 2 -49 6 2 -48 6 air
fill 4 -49 6 4 -48 6 air
setblock 4 -50 6 black_wool
fill 5 -49 6 5 -48 6 air
fill 6 -49 6 6 -48 6 air
fill 7 -49 6 7 -48 6 air
fill 8 -49 6 8 -48 6 air
fill 9 -49 6 9 -48 6 air
fill 10 -49 6 10 -48 6 air
fill 11 -49 6 11 -48 6 air
fill 12 -49 6 12 -48 6 air
fill 13 -49 6 13 -48 6 air
fill 14 -49 6 14 -48 6 air
setblock 14 -50 6 black_wool
fill 0 -49 7 0 -48 7 air
setblock 0 -50 7 black_wool
fill 2 -49 7 2 -48 7 air
fill 3 -49 7 3 -48 7 air
setblock 3 -50 7 black_wool
fill 5 -49 7 5 -48 7 air
fill 7 -49 7 7 -48 7 air
setblock 7 -50 7 black_wool
fill 11 -49 7 11 -48 7 air
setblock 11 -50 7 black_wool
fill 0 -49 8 0 -48 8 air
fill 1 -49 8 1 -48 8 air
fill 2 -49 8 2 -48 8 air
fill 4 -49 8 4 -48 8 air
setblock 4 -50 8 black_wool
fill 5 -49 8 5 -48 8 air
fill 6 -49 8 6 -48 8 air
setblock 6 -50 8 diorite
fill 8 -49 8 8 -48 8 air
setblock 8 -50 8 black_wool
fill 9 -49 8 9 -48 8 air
fill 10 -49 8 10 -48 8 air
setblock 10 -50 8 black_wool
fill 12 -49 8 12 -48 8 air
setblock 12 -50 8 black_wool
fill 13 -49 8 13 -48 8 air
fill 14 -49 8 14 -48 8 air
setblock 14 -50 8 black_wool
fill 0 -49 9 0 -48 9 air
setblock 0 -50 9 black_wool
fill 2 -49 9 2 -48 9 air
fill 5 -49 9 5 -48 9 air
setblock 5 -50 9 diorite
fill 7 -49 9 7 -48 9 air
setblock 7 -50 9 black_wool
fill 9 -49 9 9 -48 9 air
fill 11 -49 9 11 -48 9 air
setblock 11 -50 9 black_wool
fill 13 -49 9 13 -48 9 air
fill 1 -49 10 1 -48 10 air
setblock 1 -50 10 black_wool
fill 2 -49 10 2 -48 10 air
fill 3 -49 10 3 -48 10 air
fill 4 -49 10 4 -48 10 air
setblock 4 -50 10 diorite
fill 5 -49 10 5 -48 10 air
fill 6 -49 10 6 -48 10 air
fill 7 -49 10 7 -48 10 air
fill 8 -49 10 8 -48 10 air
fill 9 -49 10 9 -48 10 air
fill 10 -49 10 10 -48 10 air
fill 11 -49 10 11 -48 10 air
fill 12 -49 10 12 -48 10 air
fill 13 -49 10 13 -48 10 air
fill 14 -49 10 14 -48 10 air
fill 0 -49 11 0 -48 11 air
setblock 0 -50 11 black_wool
fill 2 -49 11 2 -48 11 air
setblock 2 -50 11 diorite
fill 4 -49 11 4 -48 11 air
setblock 4 -50 11 black_wool
fill 6 -49 11 6 -48 11 air
fill 8 -49 11 8 -48 11 air
setblock 8 -50 11 black_wool
fill 10 -49 11 10 -48 11 air
fill 12 -49 11 12 -48 11 air
setblock 12 -50 11 black_wool
fill 14 -49 11 14 -48 11 air
fill 0 -49 12 0 -48 12 air
fill 1 -49 12 1 -48 12 air
setblock 1 -50 12 diorite
fill 2 -49 12 2 -48 12 air
fill 3 -49 12 3 -48 12 air
setblock 3 -50 12 black_wool
fill 5 -49 12 5 -48 12 air
setblock 5 -50 12 black_wool
fill 6 -49 12 6 -48 12 air
fill 7 -49 12 7 -48 12 air
setblock 7 -50 12 black_wool
fill 9 -49 12 9 -48 12 air
setblock 9 -50 12 black_wool
fill 10 -49 12 10 -48 12 air
fill 11 -49 12 11 -48 12 air
setblock 11 -50 12 black_wool
fill 13 -49 12 13 -48 12 air
setblock 13 -50 12 black_wool
fill 14 -49 12 14 -48 12 air
fill 0 -49 13 0 -48 13 air
setblock 0 -50 13 diorite
fill 2 -49 13 2 -48 13 air
fill 4 -49 13 4 -48 13 air
setblock 4 -50 13 black_wool
fill 6 -49 13 6 -48 13 air
setblock 6 -50 13 black_wool
fill 8 -49 13 8 -48 13 air
setblock 8 -50 13 black_wool
fill 10 -49 13 10 -48 13 air
fill 12 -49 13 12 -48 13 air
setblock 12 -50 13 black_wool
fill 14 -49 13 14 -48 13 air
setblock 14 -50 13 black_wool
fill 0 -49 14 0 -48 14 air
fill 2 -49 14 2 -48 14 air
fill 3 -49 14 3 -48 14 air
fill 4 -49 14 4 -48 14 air
fill 5 -49 14 5 -48 14 air
setblock 5 -50 14 black_wool
fill 7 -49 14 7 -48 14 air
setblock 7 -50 14 black_wool
fill 8 -49 14 8 -48 14 air
fill 9 -49 14 9 -48 14 air
fill 10 -49 14 10 -48 14 air
fill 11 -49 14 11 -48 14 air
fill 12 -49 14 12 -48 14 air
fill 13 -49 14 13 -48 14 air
setblock 13 -50 14 black_wool
fill -1 -50 16 1 -50 18 stone
setblock 0 -49 16 stone
setblock 0 -49 17 oak_button[facing=south] destroy
setblock 0 -50 16 command_block[facing=down]{Command: 'execute as @p if entity @p[tag=!admin] at @s run tag @s add darkRoom'} destroy
setblock 0 -51 16 chain_command_block[facing=down]{Command: 'execute as @p[tag=darkRoom] at @s run setblock 22 -49 19 redstone_block', auto:1b} destroy
kill @e[type=item]
clone -1 -50 -1 15 -47 15 -1 -46 -1