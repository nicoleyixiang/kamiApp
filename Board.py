from Region import *

# Referenced the Graph class from TA-led mini lecture on Graph Algorithms

# This object stores a board by keeping track of the regions that make up 
# the given board and the 2D list of tiles (if necessary)

class Board(object):

    def __init__(self, listOfRegions, completeList):
        self.regionList = listOfRegions
        self.graph = dict()
        self.completeList = completeList
        self.children = list()
        self.parent = None

    def createGraph(self):
        for region in self.regionList:
            self.graph[region.name] = region.neighbors
        return self.graph

    def __repr__(self):
        return f'{self.regionList}'
    
    def addChild(self, child):
        self.children.append(child)
    
    def getChildren(self):
        return self.children
    
    def setParent(self, parent):
        self.parent = parent