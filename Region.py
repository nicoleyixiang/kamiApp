# This represents each "region" on the board by storing the tiles that make 
# up that region, the region's color, its edges, and also its neighboring regions

class Region(object):
    def __init__(self, name, color, tileList, edges):
        self.name = name
        self.tiles = tileList
        self.color = color 
        self.edges = edges
        self.neighbors = set()
        self.neighborColors = list()
    
    def __repr__(self):
        returnString = f'{self.name}'
        return returnString
    
    def addNeighbor(self, neighbor):
        self.neighbors.add(neighbor)
    
    def getNeighborColors(self):
        for neighbor in self.neighbors:
            self.neighborColors.append(neighbor.color)
        return self.neighborColors
    
    def __eq__(self, other):
        if not isinstance(other, Region): return False
        else: 
            if self.tiles == other.tiles and self.color == other.color:
                return True
            else: return False