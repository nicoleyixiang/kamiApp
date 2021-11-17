###################################
# Name: Nicole Xiang
# Date: November 11th 2021
# 112 TERM PROJECT: KAMI!
###################################

from cmu_112_graphics import * 

# colorname.com , use Hex values 
# TODO use .get for app.colors as a failsafe ?? 
def appStarted(app):
    app.rows = 8
    app.cols = 4
    app.margin = 10
    app.triangleSize = 0
    app.colors = {0: "#CA3435",
                  1: "#F8FFFD",
                  2: "#1B6CA8",
                  3: "#EEDC82"}
    app.board = []
    app.currColor = 0
    app.seen = set()
    app.drawMode = False

    app.moves = []
    app.moveCounter = 0
    app.edges = set()

    app.graphDict = dict()

    app.win = False
    createBoard(app)

    app.region = set()
    app.regionList = list()

def mouseDragged(app, event):
    if app.drawMode:
        (row, col) = getRowCol(app, event.x, event.y)
        changeColor(app, row, col, app.currColor)
    
def storeMove(app, tiles, color):
    app.moveCounter += 1
    app.moves.append((tiles, color))

def mousePressed(app, event):
    app.seen.clear()
    x = event.x
    y = event.y
    (row, col) = getRowCol(app, x, y)
    if not app.drawMode:
        clickedColor = app.board[row][col]
        if app.currColor == clickedColor: return
        flood(app, row, col, clickedColor, app.currColor)
        storeMove(app, app.seen, clickedColor)
    else:
        changeColor(app, row, col, app.currColor)
    checkIfWin(app)

def checkIfWin(app):
    for row in app.board:
        boardSet = set(row)
        if len(boardSet) != 1: 
            app.win = False 
            return
    app.win = True

# Doesn't work fully yet, I want to be able to undo multiple moves in a row 
def undoMove(app):
    if len(app.moves) > 0: 
        app.moveCounter -= 1
        (tiles, color) = app.moves.pop()
        for (row, col) in tiles:
            changeColor(app, row, col, color)

def changeColor(app, row, col, color):
    if 0 <= row < app.rows and 0 <= col < app.cols:
        app.board[row][col] = color

def getRowCol(app, x, y):
    cellWidth  = app.width / app.cols
    cellHeight = app.height / app.rows
    app.triangleSize = cellWidth / 2
    row = int(y / cellHeight) 
    col = int(x / cellWidth) 
    xcoordinate = getColCoordinate(app, col)
    ycoordinate = getRowCoordinate(app, row)
    xdiff = x - xcoordinate
    ydiff = y - ycoordinate
    # TODO check how accurate this is and whether or not it needs to be 
    # recalibrated 
    if row % 2 == col % 2:
        if ydiff > xdiff: 
            row = row + 1
    elif row % 2 != col % 2: 
        if xdiff > app.triangleSize or ydiff > app.triangleSize: 
            row = row + 1
    return (row, col)

def createBoard(app):
    app.board = [([0] * app.cols) for _ in range(app.rows)]

def printInfo(app, canvas):
    # print(app.moves)
    canvas.create_text(200, 550, text = app.colors[app.currColor]) 
    if app.drawMode: 
        text = "draw mode"
    else: 
        text = "play mode"
        canvas.create_text(400, 550, 
                            text = f'Number of moves: {app.moveCounter}')
    canvas.create_text(300, 550, text = text)
    if app.win: 
        canvas.create_text(350, 570, text = "won!", fill = "red")

def redrawAll(app, canvas):
    drawBoard(app, canvas) 
    canvas.create_rectangle(0, 500, app.width, app.height, fill = "white", 
                            outline = "black")
    printInfo(app, canvas)

def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            if (row % 2 == col % 2):
                drawLeftTriangle(app, canvas, row, col)
            elif (row % 2 != col % 2):
                  drawRightTriangle(app, canvas, row, col)

def getRowCoordinate(app, row):
    coordinate = (app.height // app.rows) * row
    return coordinate 

def getColCoordinate(app, row):
    coordinate = (app.width // app.cols) * row
    return coordinate 

def drawLeftTriangle(app, canvas, row, col):
    x1 = getColCoordinate(app, col)
    x2 = getColCoordinate(app, col + 1)
    topY = getRowCoordinate(app, row - 1)
    midY = getRowCoordinate(app, row)
    endY = getRowCoordinate(app, row + 1)
    color = app.colors.get(app.board[row][col], 0)
    # color = rgbString(240, 100, 200)
    canvas.create_polygon(x1, midY, x2, topY, x2, endY, fill = color, width = 1,
                        outline = "black")

def drawRightTriangle(app, canvas, row, col):
    x1 = getColCoordinate(app, col)
    x2 = getColCoordinate(app, col + 1)
    topY = getRowCoordinate(app, row - 1)
    midY = getRowCoordinate(app, row)
    endY = getRowCoordinate(app, row + 1)
    color = app.colors.get(app.board[row][col], 0)
    # color = 'white'
    canvas.create_polygon(x1, topY, x1, endY, x2, midY, fill = color, width = 1,
                        outline = "black")

# Flood filling algorithm I wrote is below. Learned graph algorithm concepts
# during TA led mini lecture "Graph Algorithms"
def flood(app, row, col, clickedColor, color):
    changeColor(app, row, col, color) # Change color of tile the user clicked 
    app.seen.add((row,col)) # Add it to set of seen tiles 
    if row % 2 != col % 2: # For all right facing triangles 
        for (drow, dcol) in [(-1, 0), (+1, 0), (0, -1)]: 
            if isLegal(app, row + drow, col + dcol, clickedColor):
                flood(app, row + drow, col+dcol, clickedColor, color)
    elif row % 2 == col % 2: # For all left facing triangles 
        for (drow, dcol) in [(-1, 0), (+1, 0), (0, +1)]:
            if isLegal(app, row + drow, col + dcol, clickedColor):
                flood(app, row+drow, col+dcol, clickedColor, color) 

def isLegal(app, row, col, clickedColor):
    if row < 0 or row >= app.rows or col < 0 or col >= app.cols: 
        return False
    if app.board[row][col] != clickedColor: 
        app.edges.add((row,col))
        return False
    if (row, col) in app.seen: 
        return False 
    return True

####### Autosolver (Planning) #########

def search(app, row, col, color):
    app.region.add((row,col)) # Add it to set of seen tiles 
    app.seen.add((row,col))
    if row % 2 != col % 2: # For all right facing triangles 
        for (drow, dcol) in [(-1, 0), (+1, 0), (0, -1)]: 
            if isLegal(app, row + drow, col + dcol, color):
                search(app, row + drow, col+dcol, color)
    elif row % 2 == col % 2: # For all left facing triangles 
        for (drow, dcol) in [(-1, 0), (+1, 0), (0, +1)]:
            if isLegal(app, row + drow, col + dcol, color):
                search(app, row+drow, col+dcol, color) 

def getNextRowCol(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if (row, col) not in app.seen: return (row, col)
    return None

def createNode(app):
    while len(app.seen) != app.rows * app.cols:
        position = getNextRowCol(app)
        app.region.clear()
        app.edges.clear()
        if position == None: return 
        else:
            checkX, checkY = position 
            color = app.board[checkX][checkY]
            search(app, checkX, checkY, color) 
            tiles = app.region.copy()
            edges = app.edges.copy()
            # TODO this might be very inefficient lol 
            newRegion = Node(tiles, color, edges)
            app.regionList.append(newRegion)
    printStuff(app)
    createConnections(app)
    printMoreStuff(app)

def printStuff(app):
    for region in app.regionList:
        print("region", region)
        print("its edges:", region.edges)
        print("\n")

def printMoreStuff(app):
    for region in app.regionList:
        print("its connections", region.connectingregions)

def createConnections(app):
    for region1 in app.regionList:
        for (row, col) in region1.edges:
            for region2 in app.regionList:
                if (row, col) in region2.tiles:
                    region1.addConnection(region2)

class Node(object):
    def __init__(self, s, color, edges):
        self.tiles = s
        self.color = color 
        self.edges = edges
        self.connectingregions = set()
    
    def __repr__(self):
        return f'{self.tiles}'

    def addConnection(self, region):
        self.connectingregions.add(region)

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

def keyPressed(app, event):
    if event.key == "r": 
        app.currColor = 0
    elif event.key == "w": 
        app.currColor = 1
    elif event.key == "b": 
        app.currColor = 2
    elif event.key == "y":
        app.currColor = 3
    elif event.key == "Space": 
        app.drawMode = not app.drawMode
    elif event.key == "u": 
        undoMove(app)
    elif event.key == 's':
        createNode(app)

def kamiApp():
    runApp(width=500, height=600)

kamiApp()

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