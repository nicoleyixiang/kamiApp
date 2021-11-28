from main import *
import copy 

# This calculates, for each region on the board, the region with the connection
# that covers the most space on the screen 
def calculateRegionAreas(app):
    temp = dict()
    for region in app.regionList:
        (bestConnection, bestNumber) = findConnectionWthMostArea(region)
        temp[region.color] = (bestConnection, bestNumber)
    best = 0
    bestKey = None
    colorToClick = None
    for key in temp:
        if best < temp[key][1]:
            best = temp[key][1]
            bestKey = key
            colorToClick = temp[key][0]
    print(bestKey, best, colorToClick)


def merge(self, color):
    newColor = color 
    newTiles = copy.copy(self.tiles)
    newNeighbors = list()
    for neighbor in self.getNeighbors():
        if neighbor.color == color: 
            newTiles.extend(neighbor.tiles)
            for neighborsOfNeighbor in neighbor.getNeighbors():
                if neighborsOfNeighbor != self and neighborsOfNeighbor not in newNeighbors: 
                    newNeighbors.append(neighborsOfNeighbor)
    return Region(self.name, newTiles, newColor, newNeighbors)

# This searches through each of the connecting neighbors of a given region and  
# returns the neighbor with the greatest amount of tiles (i.e. area)
def findConnectionWthMostArea(region):
    connectingAreas = dict() 
    for neighbor in region.getNeighbors():
        color = neighbor.color 
        area = len(neighbor.tiles)
        connectingAreas[color] = connectingAreas.get(color, 0) + area 
    bestNumber = 0
    bestConnection = None
    for key in connectingAreas:
        if bestNumber < connectingAreas[key]:
            bestNumber = connectingAreas[key]
            bestConnection = key
    return (bestConnection, bestNumber)

def newChildCreation(boardD):
    children = list()
    for key in boardD:
        neighbors = boardD[key]
        for neighbor in neighbors:
            childBoard = newTestMerge(key, neighbor.color, boardD)
            children.append(childBoard)
    return children

# Thoughts: maybe instead of storing as objects, I store them as tuples instead? 
# all I need to know really is the color, name and the connections
def newTestMerge(regionName, color, d):
    newGraph = copy.deepcopy(d)
    regionToChange = d[regionName]
    for neighbor in regionToChange:
        # Need to somehow actually GET the regionToChange instead of just the key/name
        if neighbor.color == color: 
            # newTiles = regionToChange.tiles + neighbor.tiles
            newTiles = []
            newRegion = Region(regionName, color, newTiles)
            newRegion.connectingRegions = regionToChange.connectingRegions + neighbor.connectingRegions 
            for key in d: 
                if neighbor in d[key]: d[key].remove(neighbor)
            newGraph[regionName] = newRegion.connectingRegions
    return newGraph

def createChildsForBoardUsingRegionList(regionList):
    children = list()
    for region in regionList:
        for color in region.getNeighborColors():
            child = creatingChildRegionLists(region, color, regionList)
            children.append(child)
    return children 

def creatingChildRegionLists(regionToChange, color, regionList):
    newRegionList = copy.deepcopy(regionList) 
    newRegionList.remove(regionToChange)
    newConnectingRegions = list()
    newConnectingRegions.extend(regionToChange.connectingRegions)
    newRegion = Region(regionToChange.name, color)
    for neighbor in regionToChange.getNeighbors():
        if neighbor.color == color:
            for connection in neighbor.connectingRegions:
                if connection not in newConnectingRegions:
                    newConnectingRegions.append(connection)
            for region in newRegionList:
                if neighbor in region.connectingRegions:
                    region.connectingRegions.remove(neighbor)
                    region.connectingRegions.append(newRegion)
            if neighbor in newRegionList: newRegionList.remove(neighbor)
    newRegion.connectingRegions = newConnectingRegions
    newRegionList.append(newRegion)
    return newRegionList

# TODO test out using tuples instead to make BFS faster 
def createAdjacencyList(regionList):
    adjacency = dict() 
    for region in regionList:
        adjacency[(region.name, region.color)] = set()
        for neighbor in region.connectingRegions:
            adjacency[region.name].add(neighbor.name)
    return adjacency

def createChildsForBoard(boardD):
    children = list()
    for key in boardD:
        # colors = boardD[key].getNeighborColors()
        neighbors = boardD[key]
        for neighbor in neighbors:
            childBoard = makeChildRegionList(key, neighbor.color, boardD)
            children.append(childBoard)
    return children

def makeChildRegions(regionChange, color, boardD):
    newGraph = copy.deepcopy(boardD)
    neighbors = boardD[regionChange]
    for neighbor in neighbors:
        if neighbor.color == color:
            for key in newGraph:
                if neighbor in newGraph[key]:
                    newGraph[key].remove(neighbor)
                    newGraph[key].append(regionChange) # This might be a problem, because it's not actually appending an object
            del newGraph[neighbor.name] # Delete the neighbor from the graph 
            for neighbor2 in neighbor.getNeighbors(): # 
                if neighbor2 not in boardD[regionChange]:
                    newGraph[regionChange].append(neighbor2)
    print(newGraph)
    newBoard = Board()
    newBoard.graph = newGraph
    return newGraph

# This function uses adjaceny matrices instead to create children 
# TODO using this method instead of the lists to make it more efficient? 
def makeChildRegionList(regionChange, color, board):
    board.createGraph()
    newGraph = copy.deepcopy(board.graph) # This copies over the adjacency
    print(newGraph)
    # newBoard.createGraph()
    # regionList = board.regionList
    neighbors = regionChange.getNeighbors() # This gets all the neighbors of the changing region 
    for neighbor in neighbors: 
        if neighbor.color == color: # If we come across one that is the color we're changing
            del newGraph[neighbor.name] # Delete the neighbor from the graph 
            for neighbor2 in neighbor.getNeighbors(): # 
                if neighbor2 not in newGraph[regionChange.name]:
                    newGraph[regionChange.name].append(neighbor2)
            for key in newGraph:
                if neighbor in newGraph[key]:
                    newGraph[key].remove(neighbor)
    print(newGraph)
    newBoard = Board()
    newBoard.graph = newGraph
    # return newGraph
    # newBoard.graph = graph 
    return newBoard
    
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
