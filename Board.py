from Region import *

class Board(object):

    def __init__(self, listOfRegions, completeList = None):
        self.regionList = listOfRegions
        self.graph = dict()
        if completeList == None:
            completeList = list()
        else:
            self.completeList = completeList
        self.children = list()

    def createGraph(self):
        for region in self.regionList:
            self.graph[region.name] = region.getNeighbors()
        return self.graph

    def mergeRegions(self, regionToChange, color):
        newListOfRegions = list()
        for region in self.regionList:
            if region == regionToChange:
                return

        # return newListOfRegions

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