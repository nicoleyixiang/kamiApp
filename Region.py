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