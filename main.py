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
    app.displayHint = False

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
    app.displayHint = False
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
    canvas.create_text(100, 500, text = f'Current Color: {app.colors[app.currColor]}') 
    if app.drawMode: 
        text = "Draw mode"
    else: 
        text = "Play mode"
        canvas.create_text(400, 500, 
                            text = f'Number of moves: {app.moveCounter}')
    canvas.create_text(250, 500, text = text, fill = "blue")
    if app.win: 
        canvas.create_text(250, 550, text = "Won!", fill = "red")
        
    if app.displayHint:
        row, col = app.hintCoordinate
        color = app.colors[app.hintColor]
        xcoordinate = getColCoordinate(app, col)
        ycoordinate = getRowCoordinate(app, row)
        canvas.create_text(xcoordinate, ycoordinate, text = color, fill = color, anchor = 'nw')

    canvas.create_text(50, 520, text = "Press w for white.", anchor = "nw")
    canvas.create_text(50, 535, text = "Press b for blue.", anchor = "nw")
    canvas.create_text(50, 550, text = "Press r for maroon.", anchor = "nw")
    canvas.create_text(50, 565, text = "Press y for yellow.", anchor = "nw")

    canvas.create_text(450, 520, text = "Press h for a hint!", anchor = "ne")

    canvas.create_text(450, 540, text = "Press 1 for level 1.", anchor = "ne")
    canvas.create_text(450, 555, text = "Press 2 for level 2.", anchor = "ne")
    canvas.create_text(450, 570, text = "Press 3 for level 3.", anchor = "ne")

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

import random 

def giveInstructions(app):
    region = findRegionWithMostConnections(app)
    color = findColorToClick(region)
    position = region.tiles[random.randint(0, len(region.tiles))]
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
    app.displayHint = True
    app.seen.clear()
    app.regionList.clear()
    createNode(app)
    giveInstructions(app) 

# Hardcoding some boards for testing 
def createFirstBoard(app):
    app.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2, 2], [0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 0], [0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def createSecondBoard(app):
    app.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 1, 1, 1, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 1, 1, 1, 1, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 1, 1, 1, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 1, 1, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 0, 0, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1, 0, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 0, 1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 0, 0, 1, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 0, 0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 1, 1, 1, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 1, 1, 1, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 1, 1, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]]

def createThirdBoard(app):
    app.board = [[3, 3, 3, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 3, 3, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 3, 2, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 2, 2, 0, 0, 0, 0, 0, 2, 2, 3, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 2, 2, 3, 3, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 3, 2, 3, 3, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 3, 3, 2, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 3, 2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 2, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 0, 0, 0], [0, 0, 0, 0, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 2, 0, 0], [0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 2, 2, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 1, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 1, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 1, 1, 1]]

def createFourthBoard(app):
    app.board = [[0, 0, 3, 3, 2, 0, 0, 0, 0, 3, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0], [1, 0, 2, 3, 2, 0, 0, 0, 0, 3, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0], [1, 1, 2, 2, 2, 0, 0, 0, 0, 2, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 2, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 1, 1, 0, 0, 0, 0, 2, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 1, 1, 0, 0, 0, 2, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0], [1, 0, 3, 3, 2, 1, 1, 0, 0, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0], [1, 1, 3, 3, 2, 0, 1, 1, 0, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0], [3, 1, 1, 3, 2, 0, 0, 1, 1, 2, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0], [3, 3, 1, 2, 2, 0, 0, 0, 1, 3, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0], [3, 3, 2, 2, 2, 0, 0, 0, 0, 3, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0], [3, 3, 2, 2, 2, 3, 0, 0, 0, 3, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 2, 2, 3, 3, 0, 0, 3, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 2, 3, 3, 1, 0, 2, 3, 3, 2, 1, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 2, 3, 3, 1, 1, 2, 2, 3, 2, 1, 1, 0, 0, 0, 0, 0], [0, 0, 3, 3, 2, 0, 3, 3, 1, 1, 2, 2, 2, 0, 1, 1, 0, 0, 0, 0], [0, 0, 2, 3, 2, 0, 0, 3, 3, 1, 3, 2, 2, 0, 0, 1, 1, 0, 0, 0], [0, 0, 2, 2, 2, 0, 0, 0, 3, 3, 3, 1, 2, 0, 0, 0, 1, 1, 0, 0], [0, 0, 2, 2, 2, 0, 0, 0, 0, 3, 3, 1, 1, 0, 0, 0, 0, 1, 1, 0], [0, 0, 2, 3, 2, 0, 0, 0, 0, 2, 3, 3, 1, 1, 0, 0, 0, 0, 1, 1], [0, 0, 2, 3, 3, 0, 0, 0, 0, 2, 2, 3, 3, 1, 3, 0, 0, 0, 0, 1], [0, 0, 2, 3, 3, 0, 0, 0, 0, 2, 2, 2, 3, 3, 3, 3, 0, 0, 0, 0], [0, 0, 2, 3, 3, 0, 0, 0, 0, 2, 2, 2, 2, 3, 3, 3, 3, 0, 0, 0], [0, 0, 2, 2, 3, 0, 0, 0, 0, 2, 2, 2, 2, 0, 3, 3, 3, 3, 0, 0]]

def createAdjacencyList(app):
    for index in range(len(app.regionList)):
        node = app.regionList[index]
        app.graphDict[index] = node.connectingRegions

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
    elif event.key == "s":
        createNode(app)
    elif event.key == "h":
        giveHint(app)
    elif event.key == "1":
        createFirstBoard(app)
    elif event.key == "p":
        print(app.board)
    elif event.key == "2":
        createSecondBoard(app)
    elif event.key == "3":
        createThirdBoard(app)
    elif event.key == "4":
        createFourthBoard(app)
    elif event.key == "g":
        createAdjacencyList(app)

# Planning for BFS structure - 
# referenced https://www.educative.io/edpresso/how-to-implement-a-breadth-first-search-in-python
def BFS(app, graph, initialNode):
    # Create a queue (i.e. a list)
    # Add the initialNode to the front of the queue (index 0)

    # while the queue is not empty:
        # remove the first element in the queue (pop index 0)
        # loop through all the neighbors of the first element we just removed 
            # If we haven't visited the neighbor yet, then visit it and 
            # add it to the queue
    return 

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

def kamiApp():
    runApp(width=500, height=600)

kamiApp()