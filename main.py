###################################
# Name: Nicole Xiang
# Date: November 11th 2021
# 112 TERM PROJECT: KAMI!
###################################

from cmu_112_graphics import * 
from Region import * 
from Graph import *
from Board import *
from Button import *

################################
# Spalsh Screen Mode
################################

def splashScreenMode_redrawAll(app, canvas):
    canvas.create_text(app.width/2, 150, text='Welcome to Kami!', fill = 'black')

def splashScreenMode_keyPressed(app, event):
    app.mode = "gameMode"

#################################
# Main App
#################################

# colorname.com , use Hex values 
def appStarted(app):
    app.mode = "splashScreenMode"
    app.rows = 25
    app.cols = 15
    # app.rows = 5
    # app.cols = 5
    app.margin = 100
    app.triangleSize = 0
    app.colors = {0: "maroon",
                  1: "white",
                  2: "blue",
                  3: "yellow"}
    app.board = [[0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0]]
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
    
    app.childrenList = list()
    app.num = 0 

    # detectRegions(app)

def gameMode_mouseDragged(app, event):
    if app.drawMode:
        (row, col) = getRowCol(app, event.x, event.y)
        changeColor(app, row, col, app.currColor)
    
def storeMove(app, tiles, color):
    app.moveCounter += 1
    app.moves.append((tiles, color))

def findBoxNumber(app, x):
    number = len(app.colors)
    width = app.width // number 
    return x // width

def gameMode_mousePressed(app, event):
    cellHeight = (app.height - app.margin) / app.rows
    if event.y >= (app.height - (app.margin // 2)): 
        boxNumber = findBoxNumber(app, event.x)
        app.currColor = boxNumber
    elif event.y < app.height-app.margin:
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
            checkIfWin(app)
        else:
            changeColor(app, row, col, app.currColor)

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
    canvas.create_text(100, 500, text = 
                f'Current Color: {app.colors[app.currColor]}') 
    if app.drawMode: 
        text = "Draw mode"
    else: 
        text = "Play mode"
        canvas.create_text(400, 500, 
                            text = f'Number of moves: {app.moveCounter}')
    canvas.create_text(250, 500, text = text, fill = "blue")
    if app.win: 
        canvas.create_text(250, 530, text = "Won!", fill = "red")
        
    if app.displayHint:
        row, col = app.hintCoordinate
        color = app.colors[app.hintColor]
        xcoordinate = getColCoordinate(app, col)
        ycoordinate = getRowCoordinate(app, row)
        canvas.create_text(xcoordinate, ycoordinate, text = color, 
                            fill = color, anchor = 'nw')

    # canvas.create_text(50, 520, text = "Press w for white.", anchor = "nw")
    # canvas.create_text(50, 535, text = "Press b for blue.", anchor = "nw")
    # canvas.create_text(50, 550, text = "Press r for maroon.", anchor = "nw")
    # canvas.create_text(50, 565, text = "Press y for yellow.", anchor = "nw")

    # canvas.create_text(450, 520, text = "Press h for a hint!", anchor = "ne")

    # canvas.create_text(450, 540, text = "Press 1 for level 1.", anchor = "ne")
    # canvas.create_text(450, 555, text = "Press 2 for level 2.", anchor = "ne")
    # canvas.create_text(450, 570, text = "Press 3 for level 3.", anchor = "ne")
    # canvas.create_text(450, 585, text = "Press 4 for level 4.", anchor = "ne")

def gameMode_redrawAll(app, canvas):
    drawBoard(app, canvas) 
    cellHeight = (app.height - app.margin) / app.rows
    canvas.create_rectangle(0, app.height-app.margin-cellHeight, app.width, 
                app.height, fill = "white", outline = "black")
    numberOfColors = len(app.colors)
    colorSelectionWidth = app.width / numberOfColors
    for i in range(numberOfColors):
        xCoor = colorSelectionWidth * i 
        yCoor = app.height-app.margin//2
        canvas.create_rectangle(xCoor, yCoor, xCoor + colorSelectionWidth, app.height, fill = app.colors[i])
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

def getColCoordinate(app, col):
    coordinate = (app.width // app.cols) * col
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

# Hardcoding some boards for testing 
def createFirstBoard(app):
    app.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 3, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 2, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 3, 3, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 3, 3, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def createSecondBoard(app):
    app.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0], [1, 0, 0, 1, 1, 1, 1, 0, 0, 3, 3, 0, 0, 0, 0], [1, 1, 0, 0, 1, 1, 1, 1, 0, 3, 3, 0, 0, 0, 0], [1, 1, 1, 0, 0, 1, 1, 1, 1, 3, 3, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 1, 1, 1, 2, 3, 0, 0, 0, 0], [0, 1, 1, 1, 1, 0, 0, 1, 1, 2, 2, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 0, 0, 1, 2, 2, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 2, 2, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1, 0, 2, 2, 1, 1, 1, 0], [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def createThirdBoard(app):
    app.board = [[3, 3, 3, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 3, 3, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 3, 2, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 2, 2, 0, 0, 0, 0, 0, 2, 2, 3, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 2, 2, 3, 3, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 3, 2, 3, 3, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 3, 3, 2, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 3, 2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 2, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 0, 0, 0], [0, 0, 0, 0, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 2, 0, 0], [0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 2, 2, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 1, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 1, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 1, 1, 1]]

def createFourthBoard(app):
    app.board = [[0, 0, 3, 3, 2, 0, 0, 0, 0, 3, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0], [1, 0, 2, 3, 2, 0, 0, 0, 0, 3, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0], [1, 1, 2, 2, 2, 0, 0, 0, 0, 2, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 2, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 1, 1, 0, 0, 0, 0, 2, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 1, 1, 0, 0, 0, 2, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0], [1, 0, 3, 3, 2, 1, 1, 0, 0, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0], [1, 1, 3, 3, 2, 0, 1, 1, 0, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0], [3, 1, 1, 3, 2, 0, 0, 1, 1, 2, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0], [3, 3, 1, 2, 2, 0, 0, 0, 1, 3, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0], [3, 3, 2, 2, 2, 0, 0, 0, 0, 3, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0], [3, 3, 2, 2, 2, 3, 0, 0, 0, 3, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 2, 2, 3, 3, 0, 0, 3, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 2, 3, 3, 1, 0, 2, 3, 3, 2, 1, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 2, 3, 3, 1, 1, 2, 2, 3, 2, 1, 1, 0, 0, 0, 0, 0], [0, 0, 3, 3, 2, 0, 3, 3, 1, 1, 2, 2, 2, 0, 1, 1, 0, 0, 0, 0], [0, 0, 2, 3, 2, 0, 0, 3, 3, 1, 3, 2, 2, 0, 0, 1, 1, 0, 0, 0], [0, 0, 2, 2, 2, 0, 0, 0, 3, 3, 3, 1, 2, 0, 0, 0, 1, 1, 0, 0], [0, 0, 2, 2, 2, 0, 0, 0, 0, 3, 3, 1, 1, 0, 0, 0, 0, 1, 1, 0], [0, 0, 2, 3, 2, 0, 0, 0, 0, 2, 3, 3, 1, 1, 0, 0, 0, 0, 1, 1], [0, 0, 2, 3, 3, 0, 0, 0, 0, 2, 2, 3, 3, 1, 3, 0, 0, 0, 0, 1], [0, 0, 2, 3, 3, 0, 0, 0, 0, 2, 2, 2, 3, 3, 3, 3, 0, 0, 0, 0], [0, 0, 2, 3, 3, 0, 0, 0, 0, 2, 2, 2, 2, 3, 3, 3, 3, 0, 0, 0], [0, 0, 2, 2, 3, 0, 0, 0, 0, 2, 2, 2, 2, 0, 3, 3, 3, 3, 0, 0]]

####### Autosolver (Planning) #########

# def search(app, row, col, color):
#     app.region.add((row,col)) # Add it to set of seen tiles 
#     app.seen.add((row,col))
#     if row % 2 != col % 2: # For all right facing triangles 
#         for (drow, dcol) in [(-1, 0), (+1, 0), (0, -1)]: 
#             if isLegal(app, row + drow, col + dcol, color):
#                 search(app, row + drow, col+dcol, color)
#     elif row % 2 == col % 2: # For all left facing triangles 
#         for (drow, dcol) in [(-1, 0), (+1, 0), (0, +1)]:
#             if isLegal(app, row + drow, col + dcol, color):
#                 search(app, row+drow, col+dcol, color) 

# def getNextRowCol(app):
#     for row in range(app.rows):
#         for col in range(app.cols):
#             if (row, col) not in app.seen: return (row, col)
#     return None

def getNextPosition(rows, cols, seen):
    for row in range(rows):
        for col in range(cols):
            if (row, col) not in seen: return (row, col)
    return None

def checkIsLegal(row, col, rows, cols, color, board, edges, seen):
    if row < 0 or row >= rows or col < 0 or col >= cols: 
        return False
    if board[row][col] != color: 
        edges.add((row,col))
        return False
    if (row, col) in seen: 
        return False 
    return True

def searchForTiles(row, col, rows, cols, color, boardList, seen, edges, region):
    region.add((row,col)) # Add it to set of seen tiles 
    seen.add((row,col))
    if row % 2 != col % 2: # For all right facing triangles 
        for (drow, dcol) in [(-1, 0), (+1, 0), (0, -1)]: 
            if checkIsLegal(row + drow, col + dcol, rows, cols, color, boardList, edges, seen):
                searchForTiles(row + drow, col+dcol, rows, cols, color, boardList, seen, edges, region)
    elif row % 2 == col % 2: # For all left facing triangles 
        for (drow, dcol) in [(-1, 0), (+1, 0), (0, +1)]:
            if checkIsLegal(row + drow, col + dcol, rows, cols, color, boardList, edges, seen):
                searchForTiles(row + drow, col+dcol, rows, cols, color, boardList, seen, edges, region)

def createRegionList(boardList):
    rows, cols = len(boardList), len(boardList[0])
    seen = set()
    regionList = list()
    index = -1
    while len(seen) != rows * cols:
        index += 1
        position = getNextPosition(rows, cols, seen)
        currRegion = set()
        currRegionEdges = set()
        if position == None: return
        else:
            checkX, checkY = position
            color = boardList[checkX][checkY]
            searchForTiles(checkX, checkY, rows, cols, color, boardList, seen, currRegionEdges, currRegion)
            newRegion = Region(index, currRegion, color, currRegionEdges)
            regionList.append(newRegion)
    createConnectionsUsingList(regionList)
    return regionList

def createConnectionsUsingList(regionList):
    for region1 in regionList:
        neighbors = list()
        for (row, col) in region1.edges:
            for region2 in regionList:
                if (row, col) in region2.tiles and region2 not in neighbors:
                   neighbors.append(region2)
        region1.connectingRegions = neighbors

# This function goes through a board at its current state and 
# finds all the regions (as well as their neighboring connections)
# def detectRegions(app):
#     app.seen.clear()
#     app.regionList.clear()
#     index = -1
#     while len(app.seen) != app.rows * app.cols:
#         index += 1
#         position = getNextRowCol(app)
#         app.region.clear()
#         app.edges.clear()
#         if position == None: return 
#         else:
#             checkX, checkY = position 
#             color = app.board[checkX][checkY]
#             search(app, checkX, checkY, color) 
#             tiles = list(app.region.copy())
#             edges = app.edges.copy()
#             newRegion = Region(index, tiles, color, list(), edges)
#             app.regionList.append(newRegion)
#     return createConnections(app)

# This goes through each region on the board and adds connections based on 
# which of the other regions are touching the edge of current region 
# def createConnections(app):
#     for region1 in app.regionList:
#         neighbors = list()
#         for (row, col) in region1.edges:
#             for region2 in app.regionList:
#                 if (row, col) in region2.tiles and region2 not in neighbors:
#                    neighbors.append(region2)
#         region1.connectingRegions = neighbors
#     # graphToBoard(app, app.regionList)
#         # print(region1.connectingRegions)
#     return createAdjacencyList(app.regionList, app.board)

# def regionListToBoard(app, regionList):
#     for region in regionList:
#         tiles = region.tiles
#         color = region.color
#         for (row, col) in tiles:
#             app.board[row][col] = color

# # This creates a Board based on the regions and their neighbors 
# def createAdjacencyList(regionList, boardList):
#     newGraph = Board(regionList, boardList)
#     return newGraph

# For the starting board, loop through each region and try each color
def createChildrenBoardsForBoard(board):
    for region in board.regionList:
        colors = region.getNeighborColors()
        for color in colors:
            child = createChildForRegion(region, color, board)
            childRegionList = createRegionList(child)
            childBoard = Board(childRegionList, child)
            board.addChild(childBoard)
                # childBoard = Board(child)
                # board.addChild(childBoard)
                # board.addChild(child)
    # return board.children 
    
import copy 

def makeChildForRegion(regionChange, color, board):
    return

# I think this needs to be more efficient
def createChildForRegion(regionChange, color, board):
    newList = copy.deepcopy(board.completeList)
    # for region in board.regionList:
    #     for (row, col) in region.tiles:
    #         newList[row][col] = region.color
    for (row, col) in regionChange.tiles:
        newList[row][col] = color
    return newList
    
    # resultListOfRegions = list()
    # mergedRegion = region.newMerge(color)
    # # print(len(mergedRegion.tiles))
    # for (row, col) in mergedRegion.tiles:
    #     app.board[row][col] = mergedRegion.color
    # resultListOfRegions.append(mergedRegion)
    # for otherRegions in mergedRegion.getNeighbors():
    #     resultListOfRegions.append(otherRegions)
    # print(resultListOfRegions)
    # return resultListOfRegions

def BFSHelper(app):
    regionList = createRegionList(app.board)
    currBoard = Board(regionList, app.board)
    BFS(currBoard)

# Planning for BFS structure - 
# referenced https://www.educative.io/edpresso/how-to-implement-a-breadth-first-search-in-python
def BFS(startingBoard):
    queue = list()
    # visited = list()
    level = 1
    queue.append((startingBoard, 0))

    while queue != []:
        (currState, currLevel) = queue.pop(0) 
        createChildrenBoardsForBoard(currState)
        children = currState.getChildren()
        numberOfChildren = len(children)
        if currLevel > level: level += 1
        for index in range(numberOfChildren):
            if len(children[index].regionList) == 1:
                print("Number of moves needed:", level)
                return
            else:
                # visited.append(children[index])
                queue.append((children[index], level + 1))


# This returns the region with the most connections 
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

# This calculates, for each region on the board, the region with the connection
# that covers the most space on the screen 
def calculateRegionAreas(app):
    temp = dict()
    for region in app.regionList:
        (bestConnection, bestNumber) = findConnectionWthMostArea(region)
        temp[region.color] = (bestConnection, bestNumber)
    best = 0
    bestKey = None
    colorToClick = None
    for key in temp:
        if best < temp[key][1]:
            best = temp[key][1]
            bestKey = key
            colorToClick = temp[key][0]
    print(bestKey, best, colorToClick)

# This searches through each of the connecting neighbors of a given region and  
# returns the neighbor with the greatest amount of tiles (i.e. area)
def findConnectionWthMostArea(region):
    connectingAreas = dict() 
    for neighbor in region.getNeighbors():
        color = neighbor.color 
        area = len(neighbor.tiles)
        # print(color, area)
        connectingAreas[color] = connectingAreas.get(color, 0) + area 
    bestNumber = 0
    bestConnection = None
    for key in connectingAreas:
        if bestNumber < connectingAreas[key]:
            bestNumber = connectingAreas[key]
            bestConnection = key
    return (bestConnection, bestNumber)

def giveInstructions(app):
    region = findRegionWithMostConnections(app)
    color = findColorToClick(region)
    position = region.tiles[random.randint(0, len(region.tiles)-1)]
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
    # detectRegions(app)
    giveInstructions(app) 

def gameMode_keyPressed(app, event):
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
    elif event.key == "1":
        app.moveCounter = 0
        createFirstBoard(app)
    elif event.key == "2":
        app.moveCounter = 0 
        createSecondBoard(app)
    elif event.key == "3":
        app.moveCounter = 0
        createThirdBoard(app)
    elif event.key == "4":
        app.moveCounter = 0 
        createFourthBoard(app)
    # elif event.key == "h":
    #     giveHint(app)
    elif event.key == "p":
        print(app.board)
        # currBoard = detectRegions(app)
    #     # print(createRegionList(app.board))
    #     # currBoard = Board(createRegionList(app.board), app.board)
    #     # print(currBoard)
    #     listOfChildBoards = createChildrenBoardsForBoard(app, currBoard)
    #     # print(listOfChildBoards)
    #     # print(type(listOfChildBoards[0].regionList))
    #     app.childrenList = listOfChildBoards
    #     # print(app.childrenList)
    # elif event.key == "i":
    #     if app.num == len(app.childrenList): return
    #     print(len(app.childrenList))
    #     print(app.childrenList)
    #     testList = app.childrenList[app.num].completeList
    #     # childRegions = app.childrenList[app.num].regionList
    #     # print(type(childRegions))
    #     # regionListToBoard(app, testList)
    #     app.board = testList
    #     # app.board = graphToBoard(app, childRegions)
    #     app.num += 1
    elif event.key == "0":
        BFSHelper(app)

def kamiApp():
    runApp(width=500, height=600)

kamiApp()