# Code copied from TA-led mini lecture "Graph Algorithms"
class Graph(object):
    
    def __init__(self, d):
        self.table = d
    
    # Add an edge between two nodes in a graph 
    def addEdge(self, nodeA, nodeB):
        if nodeA not in self.table:
            self.table[nodeA] = set()
        if nodeB not in self.table:
            self.table[nodeB] = set()

    # Return a list of all nodes in the graph 
    def getNodes(self):
        return list(self.table)
    
    # Return a set of all neighbor nodes of a given node
    def getNeighbors(self, node):
        return set(self.table[node])

    def __repr__(self):
        return f'{self.table}'