Author: Nicole Xiang 
AndrewID: yinicolx
Date Created: November 11th 2021


'''
BFS 
1. Check if any of the neibors is the target node 
    - if it isn't then you step again 
    - looking at everything that is first one level away, then two levels, etc. 
2. NOT a recursive algorithm, don't write using recursion 

How to reconstruct paths from BFS/DFS? 
1. Have a dict mapping each node to a previous node (initially all None)
2. Whenever the search visits node V from node U, have V point to U in the dict
3. At the end of the search, start at the target node and follow the pointers back
to the start node, building the list up as we go 

What is BFS/DFS useful for? 
- Identifying connecting components 
    - How is this implemented in my case? 
    - Remove all connected nodes of the same color and also to find 
    and remove all bubbles that are no longer connected to the ceiling
- Floodfill 
'''

### NOTES ###
''' 
Autosolver given a board of tiles and colors 
- Are there multiple solutions possible or only one "best solution"? 
    - If there are multiple solutions possible, then maybe the program should
    be able to dynamically solve from the given state (i.e. recalibrate)
    - If there is only one best solution, then the program should be 
    able to inform the user of the next best move 
- Will there ever be a case where the board is unsolvable? Probably not... 
- Should the user be able to undo moves? Need a way to store the prev state(s)
    - Clearing the board and starting fresh is probably a lot easier, less
    memory needed to store that info 
'''

'''
Need a way to extract the 2D list of colors and understand how each piece is 
represented as a region. 
'''

''' 
Another possible version would be to do the flood filling one 
- Start from a given node and expand it outwards 
'''

''' 
Possible extensions to the game...?
1. Leaderboard, other input factors, etc.
2. Different shaped tiles... will that change anything?
'''

''' Intuitively, which shape is touching the color with most areas to 
flood as much as possible '''

''' for every move, change as many tiles as possible OR make bigger groups '''

''' do my edges need to have weights? weight being a color, so the 
program will check for each block of colors (node) how many edges with the 
same weight exist. the node with the most edges of same weight is the 
best next move '''

'''    
# Code copied from TA-led mini lecture "Graph Algorithms"
class Graph(object):
    
    def __init__(self, d):
        self.table = d
    
    # Add an edge between two nodes in a graph 
    def addEdge(self, nodeA, nodeB, weight=1):
        if nodeA not in self.table:
            self.table[nodeA] = set()
        if nodeB not in self.table:
            self.table[nodeB] = set()
        self.table[nodeA][nodeB] = weight
        self.table[nodeB][nodeA] = weight

    # Return a list of all nodes in the graph 
    def getNodes(self):
        return list(self.table)
    
    # Return a set of all neighbor nodes of a given node
    def getNeighbors(self, node):
        return set(self.table[node])
'''
