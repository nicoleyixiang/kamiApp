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
    app.currColor = 1
    app.seen = set()
    app.drawMode = False
    createBoard(app)

def mousePressed(app, event):
    x = event.x
    y = event.y
    if not app.drawMode:
        (row, col) = getRowCol(app, x, y)
        clickedColor = app.board[row][col]
        # changeColor(app, row, col)
        flood(app, row, col, app.currColor, clickedColor)
        app.seen.clear()
    else:
        return

def keyPressed(app, event):
    if event.key == "r": app.currColor = 0
    elif event.key == "w": app.currColor = 1
    elif event.key == "b": app.currColor = 2
    elif event.key == "Space": app.drawMode = not app.drawMode

def changeColor(app, row, col):
    if row <= app.rows and col <= app.cols:
        app.board[row][col] = app.currColor

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
    print("first", row, col)
    if row % 2 == col % 2:
        print("1!")
        if ydiff > xdiff: row = row + 1
    elif row % 2 != col % 2: 
        print("2!")
        if xdiff > app.triangleSize or ydiff > app.triangleSize: row = row + 1
    print(row, col)
    return (row, col)

def createBoard(app):
    app.board = [([0] * app.cols) for _ in range(app.rows)]
    app.board[4][2] = 2
    app.board[3][2] = 2
    app.board[4][1] = 2
    for i in range(app.rows):
        app.board[i][2] = 2
    for i in range(app.rows):
        app.board[i][8] = 1
    for i in range(app.rows):
        for j in range(app.cols):
            if i == j:
                app.board[i][j] = 1
        
def printInfo(app, canvas):
    canvas.create_text(200,550, text = app.colors[app.currColor]) 
    canvas.create_text(250,550, text = app.drawMode)

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
    canvas.create_polygon(x1, midY, x2, topY, x2, endY, fill = color, width = 1,
                        outline = "black")

def drawRightTriangle(app, canvas, row, col):
    x1 = getColCoordinate(app, col)
    x2 = getColCoordinate(app, col + 1)
    topY = getRowCoordinate(app, row - 1)
    midY = getRowCoordinate(app, row)
    endY = getRowCoordinate(app, row + 1)
    color = app.colors.get(app.board[row][col])
    canvas.create_polygon(x1, topY, x1, endY, x2, midY, fill = color, width = 1,
                        outline = "black")

def flood(app, row, col, color, clickedColor):
    changeColor(app, row, col)
    app.seen.add((row,col))
    if row % 2 != col % 2:
        for (drow, dcol) in [(-1, 0), (+1, 0), (0, -1)]:
            if isLegal(app, row + drow, col + dcol, clickedColor):
                flood(app, row + drow, col+dcol, color, clickedColor)
    elif row % 2 == col % 2: 
        for (drow, dcol) in [(-1, 0), (+1, 0), (0, +1)]:
            if isLegal(app, row + drow, col + dcol, clickedColor):
                flood(app, row+drow, col+dcol, color, clickedColor) 

def isLegal(app, row, col, clickedColor):
    if (row, col) in app.seen: return False
    if row < 0 or row >= app.rows or col < 0 or col >= app.cols: return False
    if app.board[row][col] != clickedColor: return False
    return True

def kamiApp():
    runApp(width=500, height=600)

kamiApp()