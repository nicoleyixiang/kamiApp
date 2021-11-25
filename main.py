###################################
# Name: Nicole Xiang
# Date: November 11th 2021
# 112 TERM PROJECT: KAMI!
###################################

from cmu_112_graphics import * 
from Region import * 
from Graph import *
from Board import *

##################################
# Spalsh Screen Mode
##################################

def splashScreenMode_redrawAll(app, canvas):
    canvas.create_image(200, 300, image=ImageTk.PhotoImage(app.image2))
    canvas.create_image(app.width/2, app.height/2, 
            image=ImageTk.PhotoImage(app.image4))
    canvas.create_text(app.width/2, app.height/2 + 80, 
            text="Press any key to begin!", font = "Hiragino 12 bold", 
            fill = "#D57E7E")

def splashScreenMode_keyPressed(app, event):
    app.mode = "homeScreenMode"

def splashScreenMode_mousePressed(app, event):
    app.mode = "homeScreenMode"

# def spalshScreenMode_timerFired(app, event):
#     app.timeRan += app.timerDelay
#     if app.timeRan > 5000:
#         app.timeRan = 0
#         app.mode = "homeScreenMode"        

##################################
# Instructions Mode
##################################

def instructionsMode_redrawAll(app):
    return 

################################
# Home Screen Mode 
################################

def homeScreenMode_redrawAll(app, canvas):
    canvas.create_image(200, 300, image=ImageTk.PhotoImage(app.image2))
    # canvas.create_image(app.width/4, app.height/5, 
    #               image=ImageTk.PhotoImage(app.image4))
    canvas.create_rectangle(app.width/3, app.height/4, 2*app.width/3, 
                    1.5*app.height/4, fill = "#ACE3E8", width = 0)
    canvas.create_text(1.5*app.width/3, 1.25*app.height/4, text = "DRAW",
                    font = "Hiragino 24 bold", fill = "black")
    canvas.create_rectangle(app.width/3, 2*app.height/4, 2*app.width/3, 
                    2.5*app.height/4, fill = "#D57E7E", width = 0)
    canvas.create_text(1.5*app.width/3, 2.25*app.height/4, text = "PLAY",
                    font = "Hiragino 24 bold", fill = "black")

def homeScreenMode_mousePressed(app, event):
    app.displayMoves = False
    app.win = False
    x = event.x
    y = event.y
    if app.width/3 < x < 2*app.width/3 and app.height/4 < y < 1.5*app.height/4:
        createBoard(app)
        app.level = None
        app.mode = "drawMode"
        app.drawMode = True
    elif (app.width/3 < x < 2*app.width/3 and 
                        2*app.height/4 < y < 2.5*app.height/4):
        app.level = 1
        app.mode = "gameMode"
        app.drawMode = False
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
    canvas.create_rectangle(10, app.height-app.margin, 100, 
                app.height-app.margin+30, fill = "white", width = 0.5)
    canvas.create_text(55, app.height-app.margin+15, text = "Back", 
                fill = "#D57E7E", font = "Hiragino")
    canvas.create_rectangle(400, app.height-app.margin, 490, 
                app.height-app.margin+30, fill = "white", width = 0.5)
    canvas.create_text(445, app.height-app.margin+15, text = "Play!", 
                fill = "#D57E7E", font = "Hiragino")
    printInfo(app, canvas)

def drawMode_mousePressed(app, event):
    if event.y >= (app.height - (app.margin // 2)): 
        boxNumber = findBoxNumber(app, event.x)
        app.currColor = boxNumber
        app.xCoor = app.colorSelectionWidth * (boxNumber+1)
    elif (10 < event.x < 100 and 
            app.height-app.margin < event.y < app.height-app.margin+15):
        app.mode = "homeScreenMode"
        app.level = None
    elif (400 < event.x < 490 and 
            app.height-app.margin < event.y < app.height-app.margin+15):
        app.mode = "gameMode"
        app.drawMode = False
    else:
        (row, col) = getRowCol(app, event.x, event.y)
        changeColor(app, row, col, app.currColor)

def drawMode_keyPressed(app, event):
    if event.key == "Space":
        app.drawMode = False
        app.mode = "gameMode"

def drawMode_mouseDragged(app, event):
    (row, col) = getRowCol(app, event.x, event.y)
    changeColor(app, row, col, app.currColor)

############################
# Game Over 
############################

def gameOver_redrawAll(app, canvas):
    canvas.create_image(200, 300, image=ImageTk.PhotoImage(app.image2))
    canvas.create_text(app.width/2, app.height/2, 
    text = "Congrats! Levels completed. Press r to go back to the home screen.")

def gameOver_keyPressed(app, event):
    if event.key == "r":
        app.mode = "homeScreenMode"

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
    elif (10 < event.x < 100 and 
                app.height-app.margin < event.y < app.height-app.margin+15):
        app.mode = "homeScreenMode"   
        app.moveCounter = 0 
        app.movesNeededForBoard = None
    else: return

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
    canvas.create_rectangle(10, app.height-app.margin, 100, 
                app.height-app.margin+30, fill = "white", width = 0.5)
    canvas.create_text(55, app.height-app.margin+15, text = "Back", 
                fill = "#D57E7E", font = "Hiragino")
    if app.displayMoves:
        canvas.create_text(app.width/2, app.height-app.margin+30, 
        text = f'Number of moves needed: {app.movesNeededForBoard}', fill = "red")
    if app.win: 
        canvas.create_rectangle(0, app.height/2-15, 
            app.width, app.height/2+30, fill = "white")
        canvas.create_text(app.width/2, app.height/2, 
            text = "WON!", fill = "red")
        if app.level == None: 
            canvas.create_text(app.width/2, app.height/2 + 15, 
            text = "Press back to return to home screen.")
        else:
            canvas.create_text(app.width/2, app.height/2 + 15, 
            text = "Press any key for the next level.")
    if (app.movesNeededForBoard != None and 
                        app.moveCounter > app.movesNeededForBoard):
        canvas.create_text(app.width/2, app.height - app.margin, 
        text = "Too many moves used!")
        # TODO need to restart the counter if the user 
        # presses 0 in the middle of solving 
    printInfo(app, canvas)

#################################
# Main App
#################################

# From the CMU 112 website (Graphics Week)
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def appStarted(app):
    # Initializing images 
    # https://www.istockphoto.com/vector/vector-abstract-blurry-pastel-colored-soft-gradient-background-gm959093634-261892056
    app.image1 = app.loadImage('images/splash.jpg')
    app.image2 = app.scaleImage(app.image1, 1.8)
    # https://www.fontspace.com/aroly-font-f21303
    app.image3 = app.loadImage('images/font2.png')
    app.image4 = app.scaleImage(app.image3, 1)
    
    # Initializing main variables for starting game
    app.mode = "splashScreenMode"
    app.rows = 25
    app.cols = 15
    app.margin = 100

    app.level = 1

    app.timerDelay = 1000
    app.timeRan = 0
    app.buttonsList = []

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

    app.displayMoves = False
    app.movesNeededForBoard = None
    # app.totalMovesAvailable = None 

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

# This function takes in the position of a mouse click and detects which 
# triangle it i (i.e. which row, col index triangular tile did the user select). 
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
        canvas.create_text(app.width-10, app.height-app.margin+30, 
                    text = f'Number of moves: {app.moveCounter}', anchor = "e")
    canvas.create_text(app.width/2, app.height-app.margin+15, 
                    text = text, fill = "blue")
    if app.displayHint:
        row, col = app.hintCoordinate
        (r,g,b) = app.colors[app.hintColor]
        color = rgbString(r, g, b)
        xcoordinate = getColCoordinate(app, col)
        ycoordinate = getRowCoordinate(app, row)
        canvas.create_text(xcoordinate, ycoordinate, text = "HERE!", 
                            fill = color, anchor = 'nw')

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

# This draws a triangle that points to the left. 
# This is achieved by essentially "triangulating" the points by taking the 
# left point of the triangle to be the middle "row" index, and then retrieving 
# the row index of the row above and the row below in order to form the other
# two points of the triangle.
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
                    fill = color, width = 0.1, outline = "white")

# This draws a triangle that points to the right. 
# This is achieved by essentially "triangulating" the points by taking the 
# right point of the triangle to be the middle "row" index, and then retrieving 
# the row index of the row above and the row below in order to form the other
# two points of the triangle.
def drawRightTriangle(app, canvas, row, col):
    x1 = getColCoordinate(app, col)
    x2 = getColCoordinate(app, col + 1)
    topY = getRowCoordinate(app, row - 1)
    midY = getRowCoordinate(app, row)
    endY = getRowCoordinate(app, row + 1)
    (r, g, b) = app.colors.get(app.board[row][col], 0)
    color = rgbString(r, g, b)
    canvas.create_polygon(x1, topY, x1, endY, x2, midY, fill = color, width = 0.1,
                        outline = "white")

# Learned graph concepts during TA led mini lecture "Graph Algorithms"
# and applied notes I took during that lecture below to write this DFS function:
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

############################
# Autosolver 
###########################

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

# This takes in a 2D list of a board of tiles and detects the regions that 
# make up that board.
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
            newRegion = Region(index, color, currRegion, currRegionEdges)
            regionList.append(newRegion)
    createConnectionsUsingList(regionList)
    return regionList

# This sets up the "connecting regions" for each region on the board
def createConnectionsUsingList(regionList):
    for region1 in regionList:
        neighbors = list()
        for (row, col) in region1.edges:
            for region2 in regionList:
                if (row, col) in region2.tiles and region2 not in neighbors:
                   neighbors.append(region2)
        region1.connectingRegions = neighbors

# For the starting board, loop through each region and try each color 
# (i.e. attempt every possible move for the given board)
def createChildrenBoardsForBoard(board):
    for region in board.regionList:
        colors = region.getNeighborColors()
        for color in colors:
            child = createChildForRegion(region, color, board)
            childRegionList = createRegionList(child)
            childBoard = Board(childRegionList, child)
            childBoard.parent = board
            board.addChild(childBoard)
    return board.children

# For a given region, create the resulting board after implementing the move 
def createChildForRegion(regionChange, color, board):
    newList = copy.deepcopy(board.completeList)
    for (row, col) in regionChange.tiles:
        newList[row][col] = color
    return newList
    
# This function initializes the starting node and calls BFS to find the solution
def BFSHelper(app):
    regionList = createRegionList(app.board)
    currBoard = Board(regionList, app.board)
    currBoard.createGraph()
    (app.movesNeededForBoard, resultingBoard) = BFS(currBoard)
    solution = getPath(app, resultingBoard, currBoard)
    print([currBoard] + solution)

# Using recursion to get the path from the resulting board back to the parent
def getPath(app, halfwayBoard, currBoard):
    if halfwayBoard == currBoard:
        return []
    else: 
        return getPath(app, halfwayBoard.parent, currBoard) + [halfwayBoard]

def printSolutionToSolveBoard(app):
    return 

# Learned the overall concept of BFS via https://en.wikipedia.org/wiki/Breadth-first_search 
# Referenced https://www.educative.io/edpresso/how-to-implement-a-breadth-first-search-in-python
# for the structure of a general BFS algorithm. Applied those concepts below 
# for my program. 
def BFS(startingBoard):
    queue = list()
    visited = set()
    level = 0
    queue.append(1)
    visited.add(startingBoard)
    queue.append(startingBoard)

    while queue != []:
        currState = queue.pop(0) 
        # This tracks the depth of the BFS in order to determine how many 
        # moves we've applied to get to the solution. Referenced some posts
        # from https://stackoverflow.com/questions/31247634/how-to-keep-track-of-depth-in-breadth-first-search
        # to get a sense of how this can be done but did NOT copy code directly. 
        if isinstance(currState, int):
            if currState > level: level = currState
        else:
            children = createChildrenBoardsForBoard(currState)
            numberOfChildren = len(children)
            for index in range(numberOfChildren):
                if children[index] not in visited:
                    if len(children[index].regionList) == 1: 
                        return (level, children[index])
                    else:
                        visited.add(children[index])
                        queue.append(level + 1)
                        queue.append(children[index])

########################
# Hint system
########################

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

# This function prints out instructions for what a possible "next best move"
# could be for the current board. 
def giveInstructions(app):
    region = findRegionWithMostConnections(app)
    color = findColorToClick(region)
    position = random.sample(region.tiles, 1)
    app.hintColor = color
    app.hintCoordinate = position[0]
    print(f'Click on {position} with color {app.colors[color]}')

# This function finds the best color to click based on the algorhtms above.
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

# This function gives the user a hint based on the current board.
def giveHint(app):
    app.displayHint = True
    app.seen.clear()
    app.regionList = createRegionList(app.board)
    giveInstructions(app) 

#############################
# Main key pressed functions
#############################

def gameMode_keyPressed(app, event):
    if app.win:
        if app.level != None: 
            app.level = app.level + 1
        if app.level == 2: createSecondBoard(app)
        elif app.level == 3: createThirdBoard(app)
        elif app.level == 4: createFourthBoard(app)  
        elif app.level > 4: app.mode = "gameOver"
        app.moveCounter = 0
        app.win = False
        app.displayMoves = False
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
    elif event.key == "h":
        giveHint(app)
    elif event.key == "p":
        print(app.board)
    elif event.key == "0":
        BFSHelper(app)
        app.displayMoves = True

def kamiApp():
    runApp(width=500, height=600)

kamiApp()