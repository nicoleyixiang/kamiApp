# This represents each "region" on the board by storing the tiles that make 
# up that region, the region's color, its edges, and also its neighboring regions
class Region(object):
    def __init__(self, name, tileList, color, edges):
        self.name = name
        self.tiles = tileList
        self.color = color 
        self.edges = edges
        self.connectingRegions = set()
        self.neighborColors = set()
    
    def __repr__(self):
        returnString = f'{self.name}'
        return returnString
    
    def getNeighbors(self):
        return self.connectingRegions
    
    def addNeighbor(self, neighbor):
        self.connectingRegions.add(neighbor)
    
    def getNeighborColors(self):
        for neighbor in self.connectingRegions:
            self.neighborColors.add(neighbor.color)
        return self.neighborColors
    
    def __eq__(self, other):
        if not isinstance(other, Region): return False
        else: 
            if self.tiles == other.tiles and self.color == other.color:
                return True
            else: return False

    # change the color of region1 and add all the tiles of region2 to region1 (new region)
    # this new region is connected to all the same connections as before but 
    # minus regions that are region1 or region2

    def newMerge(self, color):
        newColor = color 
        newTiles = self.tiles
        newConnections = list()
        for neighbor in self.getNeighbors():
            if neighbor.color == color: 
                newTiles.extend(neighbor.tiles)
                for neighborsOfNeighbor in neighbor.getNeighbors():
                    if neighborsOfNeighbor != self: 
                        newConnections.append(neighborsOfNeighbor)
            else:
                newConnections.append(neighbor)
        return Region(self.name, newTiles, newColor, newConnections, set())

'''
Planning:

Each node is a state in the game 
Starting node is the starting board 
    its children is each possible move that you can apply given this board 

Whenever it visits a new node, it will check if it's the completed solution 
    If it is, then we can stop and return 
    If it isn't then we keep visiting unvisited children 

If this layer has all been visited, then move onto the next layer 

Repeat until done
'''
