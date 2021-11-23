from main import *
import copy 

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

def createAdjacencyList(regionList):
    adjacency = dict() 
    for region in regionList:
        adjacency[region.name] = set()
        for neighbor in region.connectingRegions:
            adjacency[region.name].add(neighbor.name)
    return adjacency

# Attempting to make it faster
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