Author: Nicole Xiang 
AndrewID: yinicolx
Date Created: November 11th 2021


NOTES 

# TODO: Instead, would it be faster to use an adjacency list that stores the names 
# computing how to change this list, but not actually creating new objects  

# Loop through each region on the board and attempt to change it to each of the 
# neighbor's colors 
    # Check each of the region's neighbors and if they are the same color as the 
    # color we're changing to, then merge it with the region we're changing 
        # we want to combine all of the neighbor's neighbors, combine all of their
        # tiles, and name it the name of the region we "pressed" 
        # To merge, we want to first delete the neighbor from each of the key's neighbors (that region no longer exists) 
        # Add this region to the list and also replace each of the occurences of the old piece with this new region.

'''
BFS 
1. Check if any of the neighbors is the target node 
    - if it isn't then you step again 
    - looking at everything that is first one level away, then two levels, etc. 
2. NOT a recursive algorithm, don't write using recursion 

How to reconstruct paths from BFS/DFS? 
1. Have a dict mapping each node to a previous node (initially all None)
2. Whenever the search visits node V from node U, have V point to U in the dict
3. At the end of the search, start at the target node and follow the pointers back
to the start node, building the list up as we go 

What is BFS/DFS useful for? 
- Identifying connecting components 
    - How is this implemented in my case? 
    - Remove all connected nodes of the same color and also to find 
    and remove all bubbles that are no longer connected to the ceiling
- Floodfill 
'''

### NOTES ###
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
Need a way to extract the 2D list of colors and understand how each piece is 
represented as a region. 
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


# def newBFS(startingListOfRegions):
#     queue = list()
#     # visited = set()
#     level = 1
#     queue.append((startingListOfRegions, 0))
#     # visited.add(level)

#     while queue != []:
#         (currState, currLevel) = queue.pop(0) 
#         # children = createChildrenBoardsForBoard(currState)
#         children = createChildsForBoardUsingRegionList(currState)
#         # children = currState.getChildren()
#         numberOfChildren = len(children)
#         if currLevel > level: level += 1
#         for index in range(numberOfChildren):
#             # if len(children[index]) == 1:
#             # TODO change to len(children[index].graph) == 1
#             if len(children[index]) == 1:
#                 solution = "Number of moves needed: " + str(level)
#                 # print("Number of moves needed:", len(visited))
#                 return solution
#             else:
#                 # visited.append(children[index])
#                 # visited.add(level+1)
#                 queue.append((children[index], level + 1))
