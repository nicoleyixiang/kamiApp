from Region import *

# Referenced the Graph class from TA-led mini lecture on Graph Algorithms
# This object stores a board by keeping track of the regions that make up 
# the given board and the 2D list of tiles (if necessary)

class Board(object):

    def __init__(self, listOfRegions = None, completeList = None):
        self.regionList = listOfRegions
        self.graph = dict()
        if completeList == None:
            completeList = list()
        else:
            self.completeList = completeList
        self.children = list()
        self.parent = None

    def createGraph(self):
        for region in self.regionList:
            self.graph[region.name] = region.getNeighbors()
        return self.graph

    def mergeRegions(self, regionToChange, color):
        self.createGraph()
        neighbors = regionToChange.getNeighbors()
        for neighbor in neighbors: 
            if neighbor.color == color:
                return

    def createChildren(self):
        for region in self.regionList:
            colors = region.getNeighborColors()
            for color in colors:
                listOfRegions = self.mergeRegions(region, color)
                child = Board(listOfRegions)
                self.addChild(child)

    def __repr__(self):
        return f'{self.regionList}'

    def removeNode(self, node):
        del self.d[node]
    
    def addNode(self, key, value):
        self.d[key] = value
    
    def addChild(self, child):
        self.children.append(child)
    
    def getChildren(self):
        return self.children
    
    def setParent(self, parent):
        self.parent = parent