###################################
# Name: Nicole Xiang
# Date: November 11th 2021
# 112 TERM PROJECT: KAMI!
###################################

from cmu_112_graphics import * 
    
# TODO use .get for app.colors as a failsafe ?? 
def appStarted(app):
    app.rows = 25
    app.cols = 20
    app.margin = 10
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

    app.win = False
    createBoard(app)

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

def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

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
    if (row, col) in app.seen: 
        return False # If the tile already changed
    # If out of bounds 
    if row < 0 or row >= app.rows or col < 0 or col >= app.cols: 
        return False
    # If we've reached an edge 
    if app.board[row][col] != clickedColor: 
        return False
    return True

def kamiApp():
    runApp(width=500, height=600)

kamiApp()

####### Autosolver (Planning) #########

def getPieces(app):
    # start from the 0,0 index, check the color (i.e. the number stored) 
    # and figure out where the piece stores (i.e. where the number changes)
        # probably a similar algo to the flood filling 
    # store the indices in a set to represent the piece 
    # store each color as keys in dict and values being the chunks (sets)
    return 

def createGraph(app):
    # Adjacency list vs. adjacency matrix 
    return   