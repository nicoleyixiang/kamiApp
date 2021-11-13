class Graph(object):
    
    def __init__(self):
        self.table = {}
    
    # Add an edge between two nodes in a graph 
    def addEdge(self, nodeA, nodeB, weight=1):
        if nodeA not in self.table:
            self.table[nodeA] = {}
        if nodeB not in self.table:
            self.table[nodeB] = {}
        self.table[nodeA][nodeB] = weight
        self.table[nodeB][nodeA] = weight

    # Return a list of all nodes in the graph 
    def getNodes(self):
        return list(self.table)
    
    # Return a set of all neighbor nodes of a given node
    def getNeighbors(self, node):
        return set(self.table[node])