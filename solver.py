from . import *

''' 
Autosolver given a board of tiles and colors 
- Are there multiple solutions possible or only one "best solution"? 
    - If there are multiple solutions possible, then maybe the program should
    be able to dynamically solve from the given state (i.e. recalibrate)
    - If there is only one best solution, then the program should be 
    able to inform the user of the next best move 
- Will there ever be a case where the board is unsolvable? Probably not... 
- Should the user be able to undo moves? Need a way to store the prev state(s)
    - Clearing the board and starting fresh is probably a lot easier, less
    memory needed to store that info 
'''

''' 
Another possible version would be to do the flood filling one 
- Start from a given node and expand it outwards 
'''

''' 
Possible extensions to the game...?
1. Leaderboard, other input factors, etc.
2. Different shaped tiles... will that change anything?
'''

''' Intuitively, which shape is touching the color with most areas to 
flood as much as possible '''

''' for every move, change as many tiles as possible OR make bigger groups '''

''' do my edges need to have weights? weight being a color, so the 
program will check for each block of colors (node) how many edges with the 
same weight exist. the node with the most edges of same weight is the 
best next move '''