###################################
# Name: Nicole Xiang
# Date: November 11th 2021
# 112 TERM PROJECT: KAMI!
###################################

from cmu_112_graphics import * 

# colorname.com , use Hex values 
# TODO use .get for app.colors as a failsafe ?? 
def appStarted(app):
    app.rows = 25
    app.cols = 20
    app.margin = 100
    app.triangleSize = 0
    app.colors = {0: "maroon",
                  1: "white",
                  2: "darkBlue",
                  3: "yellow"}
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

    app.hintColor = 0
    app.hintCoordinate = (0,0)

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
    cellHeight = (app.height - app.margin) / app.rows
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
    canvas.create_text(100, 550, text = f'Current Color: {app.colors[app.currColor]}') 
    if app.drawMode: 
        text = "Draw mode"
    else: 
        text = "Play mode"
        canvas.create_text(400, 550, 
                            text = f'Number of moves: {app.moveCounter}')
    canvas.create_text(300, 550, text = text, fill = "black")
    if app.win: 
        canvas.create_text(200, 550, text = "Won!", fill = "red")
        
    row, col = app.hintCoordinate
    color = app.colors[app.hintColor]
    xcoordinate = getColCoordinate(app, col)
    ycoordinate = getRowCoordinate(app, row)
    canvas.create_text(xcoordinate, ycoordinate, text = color, fill = color, anchor = 'nw')

def redrawAll(app, canvas):
    drawBoard(app, canvas) 
    cellHeight = (app.height - app.margin) / app.rows
    canvas.create_rectangle(0, app.height-app.margin-cellHeight, app.width, app.height, fill = "white", 
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
    gridHeight = app.height - app.margin
    coordinate = (gridHeight // app.rows) * row
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
            tiles = list(app.region.copy())
            edges = app.edges.copy()
            # TODO this might be very inefficient 
            newRegion = Node(tiles, color, edges)
            app.regionList.append(newRegion)
    # printStuff(app)
    createConnections(app)
    # printMoreStuff(app)
    # print(findRegionWithMostConnections(app))

def printStuff(app):
    for region in app.regionList:
        print("region", region)
        print("its edges:", region.edges)
        print("\n")

def printMoreStuff(app):
    for region in app.regionList:
        print("its connections", region.connectingRegions)

def createConnections(app):
    for region1 in app.regionList:
        for (row, col) in region1.edges:
            for region2 in app.regionList:
                if (row, col) in region2.tiles:
                    region1.addConnection(region2)

def findRegionWithMostConnections(app):
    bestNumber = 0
    bestRegion = None
    for region in app.regionList:
        connections = len(region.connectingRegions)
        if connections > bestNumber: 
            bestNumber = connections 
            bestRegion = region 
    return bestRegion  

def giveInstructions(app):
    region = findRegionWithMostConnections(app)
    # print(region)
    color = findColorToClick(region)
    # print(color)
    centerCoordinate = len(region.tiles) // 2
    position = region.tiles[centerCoordinate]
    app.hintColor = color
    app.hintCoordinate = position
    print(f'Click on {position} with color {app.colors[color]}')

def findColorToClick(region):
    colorDict = dict()
    for neighbor in region.connectingRegions:
        currColor = neighbor.color
        colorDict[currColor] = colorDict.get(currColor, 0) + 1
    bestColor = 0
    bestCount = 0
    for key in colorDict:
        if bestCount < colorDict[key]:
            bestCount = colorDict[key]
            bestColor = key
    return bestColor

def giveHint(app):
    app.seen.clear()
    app.regionList.clear()
    createNode(app)
    giveInstructions(app) 

class Node(object):
    def __init__(self, tileList, color, edges):
        self.tiles = tileList
        self.color = color 
        self.edges = edges
        self.connectingRegions = set()
    
    def __repr__(self):
        return f'{self.tiles}'

    def addConnection(self, region):
        self.connectingRegions.add(region)

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
    elif event.key == 'h':
        giveHint(app)

def kamiApp():
    runApp(width=500, height=600)

kamiApp()