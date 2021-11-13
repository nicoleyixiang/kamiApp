# Name: Nicole Xiang
# Date: November 11th 2021
# 112 TERM PROJECT: KAMI!

from cmu_112_graphics import * 
    
def appStarted(app):
    app.rows = 25
    app.cols = 20
    app.margin = 10
    app.triangleSize = 0
    app.colors = {0: "maroon",
                  1: "white",
                  2: "darkBlue",
                  3: "blue",
                  4: "yellow"}
    app.board = []
    app.currColor = 0
    app.seen = set()
    app.drawMode = False

    app.moves = []

    app.win = False
    createBoard(app)

def mouseDragged(app, event):
    if app.drawMode:
        (row, col) = getRowCol(app, event.x, event.y)
        changeColor(app, row, col, app.currColor)
    
def storeMove(app, tiles, color):
    app.moves.append(tiles, color)
    print(app.moves)

def mousePressed(app, event):
    app.seen.clear()
    x = event.x
    y = event.y
    (row, col) = getRowCol(app, x, y)
    if not app.drawMode:
        clickedColor = app.board[row][col]
        flood(app, row, col, clickedColor, app.currColor)
        storeMove(app, app.seen, clickedColor)
    else:
        changeColor(app, row, col, app.currColor)
    checkIfWin(app)

def checkIfWin(app):
    for row in app.board:
        boardSet = set(row)
        if len(boardSet) != 1: return
    app.win = True

def keyPressed(app, event):
    if event.key == "r": app.currColor = 0
    elif event.key == "w": app.currColor = 1
    elif event.key == "b": app.currColor = 2
    elif event.key == "Space": app.drawMode = not app.drawMode
    elif event.key == "u": undoMove(app)

# TODO need to fix, right now it floods more than necessary 
def undoMove(app):
    if len(app.moves) > 0: 
        (tiles, color) = app.moves[-1]
        for (row, col) in app.seen:
            changeColor(app, row, col, color)
        app.moves.pop()

def changeColor(app, row, col, color):
    if row <= app.rows and col <= app.cols:
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
    if row % 2 == col % 2:
        if ydiff > xdiff: row = row + 1
    elif row % 2 != col % 2: 
        if xdiff > app.triangleSize or ydiff > app.triangleSize: row = row + 1
    return (row, col)

def createBoard(app):
    app.board = [([0] * app.cols) for _ in range(app.rows)]

def printInfo(app, canvas):
    canvas.create_text(200, 550, text = app.colors[app.currColor]) 
    if app.drawMode: text = "draw mode"
    else: text = "play mode"
    canvas.create_text(300, 550, text = text)
    if app.win: 
        canvas.create_text(350,550, text = "won!", fill = "red")

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
    color = app.colors.get(app.board[row][col])
    # color = rgbString(240, 100, 200)
    canvas.create_polygon(x1, midY, x2, topY, x2, endY, fill = color, width = 1,
                        outline = "black")

def drawRightTriangle(app, canvas, row, col):
    x1 = getColCoordinate(app, col)
    x2 = getColCoordinate(app, col + 1)
    topY = getRowCoordinate(app, row - 1)
    midY = getRowCoordinate(app, row)
    endY = getRowCoordinate(app, row + 1)
    color = app.colors.get(app.board[row][col])
    # color = 'white'
    canvas.create_polygon(x1, topY, x1, endY, x2, midY, fill = color, width = 1,
                        outline = "black")

def flood(app, row, col, clickedColor, color):
    changeColor(app, row, col, color) # Change the color of the tile the user clicked 
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
    if (row, col) in app.seen: return False # If the tile already changed
    # If out of bounds 
    if row < 0 or row >= app.rows or col < 0 or col >= app.cols: return False
    # If we've reached an edge 
    if app.board[row][col] != clickedColor: return False
    return True

def kamiApp():
    runApp(width=500, height=600)

kamiApp()