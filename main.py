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
    canvas.create_image(200, 300, image=ImageTk.PhotoImage(app.image2))
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.image4))
    canvas.create_text(app.width/2, app.height/2 + 80, text="Press any key to begin!", 
                font = "Hiragino 12 bold", fill = "#D57E7E")

def splashScreenMode_keyPressed(app, event):
    app.mode = "homeScreenMode"

def splashScreenMode_mousePressed(app, event):
    app.mode = "homeScreenMode"

# def spalshScreenMode_timerFired(app, event):
#     app.timeRan += app.timerDelay
#     if app.timeRan > 5000:
#         app.timeRan = 0
#         app.mode = "homeScreenMode"        

################################
# Home Screen Mode 
################################

def homeScreenMode_redrawAll(app, canvas):
    canvas.create_image(200, 300, image=ImageTk.PhotoImage(app.image2))
    canvas.create_rectangle(app.width/3, app.height/4, 2*app.width/3, 
                    1.5*app.height/4, fill = "#D57E7E", width = 0)
    canvas.create_text(1.5*app.width/3, 1.25*app.height/4, text = "DRAW",
                    font = "Hiragino 24 bold", fill = "#8F1E20")
    canvas.create_rectangle(app.width/3, 2*app.height/4, 2*app.width/3, 
                    2.5*app.height/4, fill = "#D57E7E", width = 0)
    canvas.create_text(1.5*app.width/3, 2.25*app.height/4, text = "PLAY",
                    font = "Hiragino 24 bold", fill = "#8F1E20")

def homeScreenMode_mousePressed(app, event):
    x = event.x
    y = event.y
    if app.width/3 < x < 2*app.width/3 and app.height/4 < y < 1.5*app.height/4:
        app.mode = "drawMode"
        app.drawMode = True
    elif app.width/3 < x < 2*app.width/3 and 2*app.height/4 < y < 2.5*app.height/4:
        app.mode = "gameMode"
        createFirstBoard(app)

#################################
# Draw Mode 
#################################

def drawMode_redrawAll(app, canvas):
    drawBoard(app, canvas) 
    cellHeight = (app.height - app.margin) / app.rows
    canvas.create_rectangle(0, app.height-app.margin-cellHeight, app.width, 
                app.height, fill = "white", outline = "black")
    yCoor = app.height-app.margin//2
    for i in range(app.numberOfColors):
        xCoor = app.colorSelectionWidth * i 
        (r,g,b) = app.colors[i]
        color = rgbString(r,g,b)
        canvas.create_rectangle(xCoor, yCoor, xCoor + app.colorSelectionWidth, 
                        app.height, fill = color)
    canvas.create_rectangle(app.xCoor, yCoor, app.xCoor-10, yCoor+10, 
                        fill = "beige")
    printInfo(app, canvas)

def drawMode_mousePressed(app, event):
    if event.y >= (app.height - (app.margin // 2)): 
        boxNumber = findBoxNumber(app, event.x)
        app.currColor = boxNumber
        app.xCoor = app.colorSelectionWidth * (boxNumber+1)
    (row, col) = getRowCol(app, event.x, event.y)
    changeColor(app, row, col, app.currColor)

def drawMode_keyPressed(app, event):
    if event.key == "Space":
        app.drawMode = False
        app.mode = "gameMode"
    elif event.key == "0":
        BFSHelper(app)

def drawMode_mouseDragged(app, event):
    (row, col) = getRowCol(app, event.x, event.y)
    changeColor(app, row, col, app.currColor)

#################################
# Main App
#################################

# From the CMU 112 website (Graphics Week)
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def appStarted(app):
    app.image1 = app.loadImage('splash.jpg')
    app.image2 = app.scaleImage(app.image1, 1.8)
    app.image3 = app.loadImage('font2.png')
    app.image4 = app.scaleImage(app.image3, 1)
    app.image5 = app.loadImage('arrow.webp')
    app.image6 = app.scaleImage(app.image5, 0.1)

    app.mode = "splashScreenMode"
    app.rows = 25
    app.cols = 15

    app.timerDelay = 1000
    app.timeRan = 0
    app.buttonsList = []

    app.margin = 100
    app.triangleSize = 0
    app.colors = {0: (247, 246, 242),
                  1: (170, 216, 211),
                  2: (56,  62,  86),
                  3: (251, 116, 62)}
    app.board = []
    app.currColor = 0
    app.seen = set()
    app.drawMode = False
    app.displayHint = False

    app.numberOfColors = len(app.colors)
    app.colorSelectionWidth = app.width // app.numberOfColors
    app.xCoor = app.colorSelectionWidth

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

def storeMove(app, tiles, color):
    app.moveCounter += 1
    app.moves.append((tiles, color))

def findBoxNumber(app, x):
    number = len(app.colors)
    width = app.width // number 
    return x // width

def checkIfWin(app):
    for row in app.board:
        boardSet = set(row)
        if len(boardSet) != 1: 
            app.win = False 
            return
    app.win = True

def undoMove(app):
    if app.moveCounter > 0: 
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
    if app.drawMode: 
        text = "Draw mode"
    else: 
        text = "Play mode"
        canvas.create_text(app.width-30, app.height-app.margin+10, 
                            text = f'Number of moves: {app.moveCounter}', anchor = "e")
    canvas.create_text(app.width/2, app.height-app.margin+10, text = text, fill = "blue")
    if app.win: 
        canvas.create_text(250, 530, text = "Won!", fill = "red")
        
    if app.displayHint:
        row, col = app.hintCoordinate
        color = app.colors[app.hintColor]
        xcoordinate = getColCoordinate(app, col)
        ycoordinate = getRowCoordinate(app, row)
        canvas.create_text(xcoordinate, ycoordinate, text = color, 
                            fill = color, anchor = 'nw')

############################
# Game Mode
############################
    
def gameMode_mousePressed(app, event):
    cellHeight = (app.height - app.margin) / app.rows
    if event.y >= (app.height - (app.margin // 2)): 
        boxNumber = findBoxNumber(app, event.x)
        app.currColor = boxNumber
        app.xCoor = app.colorSelectionWidth * (boxNumber + 1)
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
            storeMove(app, copy.copy(app.seen), clickedColor)
            checkIfWin(app)

def gameMode_redrawAll(app, canvas):
    drawBoard(app, canvas) 
    cellHeight = (app.height - app.margin) / app.rows
    canvas.create_rectangle(0, app.height-app.margin-cellHeight, app.width, 
                app.height, fill = "white", outline = "black")
    yCoor = app.height-app.margin//2
    colorWidth = app.width // app.numberOfColors
    for i in range(app.numberOfColors):
        xCoor = colorWidth * i 
        (r,g,b) = app.colors[i]
        color = rgbString(r,g,b)
        canvas.create_rectangle(xCoor, yCoor, xCoor + colorWidth, 
                            app.height, fill = color)
    canvas.create_rectangle(app.xCoor, yCoor, app.xCoor-10, yCoor+10, 
                            fill = "beige")
    # canvas.create_image(50, app.height-app.margin+10, image=ImageTk.PhotoImage(app.image6))
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

def getRandomFactor(row, col):
    factor = ((col / (row + 1))) / 100
    return factor 

def drawLeftTriangle(app, canvas, row, col):
    x1 = getColCoordinate(app, col)
    x2 = getColCoordinate(app, col + 1)
    topY = getRowCoordinate(app, row - 1)
    midY = getRowCoordinate(app, row)
    endY = getRowCoordinate(app, row + 1)
    (r, g, b) = app.colors.get(app.board[row][col], 0)
    # factor = getRandomFactor(row, col)
    # factor = 1
    color = rgbString(r,g,b)
    canvas.create_polygon(x1, midY, x2, topY, x2, endY, 
                    fill = color, width = 1, outline = "black")

def drawRightTriangle(app, canvas, row, col):
    x1 = getColCoordinate(app, col)
    x2 = getColCoordinate(app, col + 1)
    topY = getRowCoordinate(app, row - 1)
    midY = getRowCoordinate(app, row)
    endY = getRowCoordinate(app, row + 1)
    (r, g, b) = app.colors.get(app.board[row][col], 0)
    color = rgbString(r, g, b)
    canvas.create_polygon(x1, topY, x1, endY, x2, midY, fill = color, width = 1,
                        outline = "black")

# Learned graph algorithm concepts during TA led mini lecture "Graph Algorithms"
# and applied notes from lecture below:
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
    app.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3], [0, 0, 2, 2, 0, 0, 0, 0, 0, 3, 3, 0, 1, 1, 3], [0, 0, 2, 2, 0, 0, 0, 0, 3, 3, 3, 3, 1, 1, 3], [0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 0, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 3, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 0, 1, 1, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 3, 3, 1, 1, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 1, 1, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 1, 1, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def createSecondBoard(app):
    app.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0], [1, 0, 0, 1, 1, 1, 1, 0, 0, 3, 3, 0, 0, 0, 0], [1, 1, 0, 0, 1, 1, 1, 1, 0, 3, 3, 0, 0, 0, 0], [1, 1, 1, 0, 0, 1, 1, 1, 1, 3, 3, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 1, 1, 1, 2, 3, 0, 0, 0, 0], [0, 1, 1, 1, 1, 0, 0, 1, 1, 2, 2, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 0, 0, 1, 2, 2, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 2, 2, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1, 0, 2, 2, 1, 1, 1, 0], [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def createThirdBoard(app):
    app.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 2, 2, 2, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0], [3, 3, 3, 3, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 3, 3, 3, 3, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 3, 3, 1, 1, 1, 2, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 1, 1, 1, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 1, 1, 1, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 3, 1, 1, 1, 2, 2, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 3, 2, 2, 2, 2, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 3, 3, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0, 1, 1, 1, 3, 3, 3, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 3, 3, 3, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 3, 3, 3, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def createFourthBoard(app):
    app.board = [[2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0], [2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0], [2, 2, 3, 3, 2, 2, 3, 3, 3, 3, 0, 0, 0, 0, 0], [2, 3, 3, 3, 2, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0], [3, 3, 3, 3, 2, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0], [3, 2, 2, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0], [3, 2, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 2, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0], [3, 3, 3, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0], [3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3], [3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 3, 3, 3], [0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3], [0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 2, 2, 3], [0, 0, 3, 3, 0, 0, 0, 0, 0, 3, 3, 3, 2, 2, 3], [0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 2, 2, 3], [0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 2, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 3, 3, 3, 2, 2, 3, 3, 3, 3], [0, 0, 0, 0, 0, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3], [0, 0, 0, 0, 3, 3, 2, 2, 3, 3, 3, 3, 3, 3, 2], [0, 0, 0, 3, 3, 3, 2, 2, 3, 3, 3, 3, 3, 2, 2], [0, 0, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3, 2, 2, 2], [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2]]

####### Autosolver #########

def getNextPosition(rows, cols, seen):
    for row in range(rows):
        for col in range(cols):
            if (row, col) not in seen: 
                return (row, col)
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
            if checkIsLegal(row + drow, col + dcol, rows, cols, color, 
                                boardList, edges, seen):
                searchForTiles(row + drow, col+dcol, rows, cols, color, 
                                boardList, seen, edges, region)
    elif row % 2 == col % 2: # For all left facing triangles 
        for (drow, dcol) in [(-1, 0), (+1, 0), (0, +1)]:
            if checkIsLegal(row + drow, col + dcol, rows, cols, color, 
                                boardList, edges, seen):
                searchForTiles(row + drow, col+dcol, rows, cols, color, 
                                boardList, seen, edges, region)

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
            searchForTiles(checkX, checkY, rows, cols, color, boardList, seen, 
                                            currRegionEdges, currRegion)
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

# For the starting board, loop through each region and try each color
def createChildrenBoardsForBoard(board):
    for region in board.regionList:
        colors = region.getNeighborColors()
        for color in colors:
            child = createChildForRegion(region, color, board)
            childRegionList = createRegionList(child)
            # childBoard = makeChildRegionList(region, color, board)
            childBoard = Board(childRegionList, child)
            board.addChild(childBoard)
    return board.children
    
import copy 

# Attempting to make it faster
def createChildsForBoard(boardD):
    children = list()
    for key in boardD:
        # colors = boardD[key].getNeighborColors()
        neighbors = boardD[key]
        for neighbor in neighbors:
            # TODO cannot pass in boardD, need to pass in the region name instead 
            childBoard = makeChildRegionList(key, neighbor.color, boardD)
            # childBoard = makeChildRegions(key, neighbor.color, boardD)
            children.append(childBoard)
    return children

def makeChildRegions(regionChange, color, boardD):
    newGraph = copy.deepcopy(boardD)
    neighbors = boardD[regionChange]
    # print(neighbors)
    for neighbor in neighbors:
        if neighbor.color == color:
            for key in newGraph:
                if neighbor in newGraph[key]:
                    newGraph[key].remove(neighbor)
                    newGraph[key].append(regionChange) # This might be a problem, because it's not actually appending an object
            del newGraph[neighbor.name] # Delete the neighbor from the graph 
            for neighbor2 in neighbor.getNeighbors(): # 
                if neighbor2 not in boardD[regionChange]:
                    newGraph[regionChange].append(neighbor2)
    print(newGraph)
    newBoard = Board()
    newBoard.graph = newGraph
    return newGraph

# This function uses adjaceny matrices instead to create children 
# TODO using this method instead of the lists to make it more efficient? 
def makeChildRegionList(regionChange, color, board):
    board.createGraph()
    newGraph = copy.deepcopy(board.graph) # This copies over the adjacency
    print(newGraph)
    # newBoard.createGraph()
    # regionList = board.regionList
    neighbors = regionChange.getNeighbors() # This gets all the neighbors of the changing region 
    for neighbor in neighbors: 
        if neighbor.color == color: # If we come across one that is the color we're changing
            del newGraph[neighbor.name] # Delete the neighbor from the graph 
            for neighbor2 in neighbor.getNeighbors(): # 
                if neighbor2 not in newGraph[regionChange.name]:
                    newGraph[regionChange.name].append(neighbor2)
            for key in newGraph:
                if neighbor in newGraph[key]:
                    newGraph[key].remove(neighbor)
    print(newGraph)
    newBoard = Board()
    newBoard.graph = newGraph
    # return newGraph
    # newBoard.graph = graph 
    return newBoard

# I think this needs to be more efficient
def createChildForRegion(regionChange, color, board):
    newList = copy.deepcopy(board.completeList)
    for (row, col) in regionChange.tiles:
        newList[row][col] = color
    return newList
    
def BFSHelper(app):
    regionList = createRegionList(app.board)
    currBoard = Board(regionList, app.board)
    # createChildrenBoardsForBoard(currBoard)
    # currBoard.createGraph()
    print(BFS(currBoard))
    
# Referenced https://www.educative.io/edpresso/how-to-implement-a-breadth-first-search-in-python
def BFS(startingBoard):
    queue = list()
    visited = set()
    level = 1
    queue.append((startingBoard, 0))
    visited.add(level)

    while queue != []:
        (currState, currLevel) = queue.pop(0) 
        children = createChildrenBoardsForBoard(currState)
        # children = currState.getChildren()
        numberOfChildren = len(children)
        if currLevel > level: level += 1
        for index in range(numberOfChildren):
            # if len(children[index]) == 1:
            # TODO change to len(children[index].graph) == 1
            if len(children[index].regionList) == 1:
                solution = "Number of moves needed: " + str(level)
                # print("Number of moves needed:", len(visited))
                return solution
            else:
                # visited.append(children[index])
                visited.add(level+1)
                queue.append((children[index], level + 1))
        # level += 1

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
    position = random.sample(region.tiles, 1)
    app.hintColor = color
    app.hintCoordinate = position[0]
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

# def giveHint(app):
#     app.displayHint = True
#     app.seen.clear()
#     app.regionList = createRegionList(app.board)
#     giveInstructions(app) 

def gameMode_keyPressed(app, event):
    if event.key == "Space": 
        app.drawMode = not app.drawMode
        app.win = False
        app.moveCounter = 0
        app.mode = "drawMode"
        createBoard(app)
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
    elif event.key == "0":
        BFSHelper(app)

def kamiApp():
    runApp(width=500, height=600)

kamiApp()