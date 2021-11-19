class Board(object):

    def __init__(self, listOfRegions, completeList):
        self.regionList = listOfRegions
        self.completeList = completeList
        # self.d = adjacencyD
        self.children = list()

    def __repr__(self):
        return f'{self.regionList}'
        # return "\n".join("{}\t{}".format(k, v) for k, v in 
                    # self.d.items())

    def removeNode(self, node):
        del self.d[node]
    
    def addNode(self, key, value):
        self.d[key] = value
    
    def addChild(self, child):
        self.children.append(child)