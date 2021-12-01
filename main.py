###################################
# Name: Nicole Xiang
# Date: November 11th 2021
# 112 TERM PROJECT: KAMI!
###################################

from cmu_112_graphics import * 
from Region import * 
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

################################
# Home Screen Mode 
################################

def homeScreenMode_redrawAll(app, canvas):
    canvas.create_image(200, 300, image=ImageTk.PhotoImage(app.image2))
    canvas.create_rectangle(app.width / 3, app.height / 4, 2 * app.width / 3, 
                    1.5 * app.height / 4, fill = "#ACE3E8", width = 1)
    canvas.create_text(1.5 * app.width / 3, 1.25 * app.height / 4, 
                    text = "DRAW",
                    font = "Hiragino 24 bold", fill = "black")
    canvas.create_rectangle(app.width / 3, 2 * app.height / 4, 
                    2 * app.width / 3, 2.5 * app.height / 4, fill = "#D57E7E", 
                    width = 1)
    canvas.create_text(1.5 * app.width / 3, 2.25 * app.height / 4, 
                    text = "PLAY",
                    font = "Hiragino 24 bold", fill = "black")

def homeScreenMode_mousePressed(app, event):
    app.displayMoves = False
    app.win = False
    x = event.x
    y = event.y
    if (app.width / 3 < x < 2 * app.width / 3 and 
        app.height / 4 < y < 1.5 * app.height / 4):
        createEmptyBoard(app)
        app.level = None
        app.mode = "drawMode"
        app.drawMode = True
    elif (app.width / 3 < x < 2 * app.width / 3 and 
        2 * app.height / 4 < y < 2.5 * app.height / 4):
        app.level = 1
        app.mode = "gameMode"
        app.drawMode = False
        createFirstBoard(app)

#################################
# Draw Mode 
#################################

def drawMode_redrawAll(app, canvas):
    drawBoard(app, canvas) 
    canvas.create_rectangle(0, app.height - app.margin - app.cellHeight, 
        app.width, app.height, fill = "white", outline = "black")
    yCoor = app.height - app.margin//2
    for i in range(app.numberOfColors):
        xCoor = app.colorSelectionWidth * i 
        (r,g,b) = app.colors[i]
        color = rgbString(r,g,b)
        canvas.create_rectangle(xCoor, yCoor, xCoor + app.colorSelectionWidth, 
                        app.height, fill = color)
    canvas.create_rectangle(app.xCoor, yCoor, app.xCoor - 10, yCoor + 10, 
                        fill = "beige")
    canvas.create_rectangle(10, app.height - app.margin, 100, 
                app.height - app.margin+30, fill = "white", width = 0.5)
    canvas.create_text(55, app.height - app.margin+15, text = "Back", 
                fill = "#D57E7E", font = "Hiragino")
    canvas.create_rectangle(110, app.height - app.margin, 200, 
                app.height - app.margin+30, fill = "white", width = 0.5)
    canvas.create_text(155, app.height - app.margin + 15, text = "Play!", 
                fill = "#D57E7E", font = "Hiragino")
    canvas.create_rectangle(210, app.height - app.margin, 300,
                app.height - app.margin + 30, fill = app.refreshButtonColor, 
                width = 0.5)
    canvas.create_text(255, app.height - app.margin + 15, text = "Refresh!",
                fill = "#D57E7E", font = "Hiragino")
    printInfo(app, canvas)

def drawMode_mousePressed(app, event):
    if event.y >= app.height - app.margin - app.cellHeight:
        if event.y >= (app.height - (app.margin // 2)): 
            boxNumber = findBoxNumber(app, event.x)
            app.currColor = boxNumber
            app.xCoor = app.colorSelectionWidth * (boxNumber + 1)
        elif app.height - app.margin <= event.y <= app.height - app.margin + 30:
            if (10 <= event.x <= 100 and 
                app.height - app.margin < event.y < 
                app.height - app.margin + 15):
                app.mode = "homeScreenMode"
                app.level = None
            elif (110 <= event.x <= 200 and 
                app.height - app.margin < event.y < 
                app.height - app.margin + 15):
                app.mode = "gameMode"
                app.drawMode = False
            elif (210 <= event.x <= 300):
                app.timePassed = 0
                app.refreshButtonColor = "lightGrey"
                createEmptyBoard(app)
    else:
        (row, col) = getRowCol(app, event.x, event.y)
        clickedColor = app.board[row][col]
        if app.currColor == clickedColor: 
            app.isErase = True
            changeColor(app, row, col, 0)
        else:
            app.isErase = False
            changeColor(app, row, col, app.currColor)

def drawMode_mouseDragged(app, event):
    # Ignore any mouse drags over the navigation bar 
    if event.y >= app.height - app.margin - app.cellHeight: return 
    (row, col) = getRowCol(app, event.x, event.y)
    clickedColor = app.board[row][col]
    if app.isErase: # If user is in erase mode 
        if app.currColor == clickedColor: 
            # Then change the tile back to white when user drags over a tile  
            # of the same color as they've selected 
            changeColor(app, row, col, 0)
    else: # Otherwise, user is not erasing 
        # Change the color of the tile into whatever the user has selected
        changeColor(app, row, col, app.currColor) 

def drawMode_timerFired(app):
    if app.timePassed != None:
        app.timePassed += app.timerDelay
    if app.timePassed == 200:
        app.refreshButtonColor = "white"
        app.timePassed = None

############################
# Levels 
############################

def createFirstBoard(app):
    app.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                 [0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3], 
                 [0, 0, 2, 2, 0, 0, 0, 0, 0, 3, 3, 0, 1, 1, 3], 
                 [0, 0, 2, 2, 0, 0, 0, 0, 3, 3, 3, 3, 1, 1, 3], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 3, 3, 3, 3], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 0, 3, 3, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 1, 1, 3, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 3, 3, 0, 1, 1, 3, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 3, 3, 3, 3, 1, 1, 3, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 3, 1, 1, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 3, 1, 1, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0], 
                 [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0], 
                 [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0], 
                 [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def createSecondBoard(app):
    app.board = [[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 1, 1, 1, 1, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 1, 1, 1, 1, 0, 3, 3, 0, 0, 0, 0, 0, 0], 
                 [1, 0, 0, 1, 1, 1, 1, 3, 3, 0, 0, 0, 0, 0, 0], 
                 [1, 1, 0, 0, 1, 1, 1, 2, 3, 0, 0, 0, 0, 0, 0], 
                 [1, 1, 1, 0, 0, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0], 
                 [1, 1, 1, 1, 0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0], 
                 [0, 1, 1, 1, 1, 0, 0, 2, 2, 1, 1, 0, 0, 0, 0], 
                 [0, 0, 1, 1, 1, 1, 0, 2, 2, 1, 1, 1, 0, 0, 0], 
                 [0, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 0, 0], 
                 [0, 0, 0, 0, 1, 1, 1, 2, 2, 0, 1, 1, 1, 1, 0], 
                 [0, 0, 0, 0, 0, 1, 1, 2, 2, 0, 0, 1, 1, 1, 1], 
                 [0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 0, 0, 1, 1, 1], 
                 [0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 0, 0, 1, 1], 
                 [0, 0, 0, 0, 0, 0, 0, 3, 2, 1, 1, 1, 0, 0, 1], 
                 [0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 1, 1, 1, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 1, 1, 1, 1, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 1, 1, 1, 1], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 1, 1], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def createThirdBoard(app):
    app.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [3, 2, 2, 2, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [3, 3, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0], 
                 [3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0], 
                 [3, 3, 3, 3, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0], 
                 [0, 3, 3, 3, 3, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 3, 3, 3, 3, 1, 1, 1, 2, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 3, 3, 3, 1, 1, 1, 2, 2, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 3, 3, 1, 1, 1, 2, 2, 2, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 3, 1, 1, 1, 2, 2, 2, 2, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 1, 1, 1, 3, 2, 2, 2, 2, 0], 
                 [0, 0, 0, 0, 0, 0, 1, 1, 1, 3, 3, 2, 2, 2, 2], 
                 [0, 0, 0, 0, 0, 0, 1, 1, 1, 3, 3, 3, 2, 2, 2], 
                 [0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 3, 3, 3, 2, 2], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 3, 3, 3, 2], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def createFourthBoard(app):
    app.board = [[2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0], 
                 [2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0], 
                 [2, 2, 3, 3, 2, 2, 3, 3, 3, 3, 0, 0, 0, 0, 0], 
                 [2, 3, 3, 3, 2, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0], 
                 [3, 3, 3, 3, 2, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0], 
                 [3, 2, 2, 3, 3, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0], 
                 [3, 2, 2, 3, 3, 3, 0, 0, 0, 0, 0, 3, 3, 0, 0], 
                 [3, 2, 2, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0], 
                 [3, 3, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0], 
                 [3, 3, 3, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0], 
                 [3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3], 
                 [3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3], 
                 [0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 3, 3, 3], 
                 [0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3], 
                 [0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 2, 2, 3], 
                 [0, 0, 3, 3, 0, 0, 0, 0, 0, 3, 3, 3, 2, 2, 3], 
                 [0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 2, 2, 3], 
                 [0, 0, 0, 0, 0, 0, 0, 3, 3, 2, 2, 3, 3, 3, 3], 
                 [0, 0, 0, 0, 0, 0, 3, 3, 3, 2, 2, 3, 3, 3, 3], 
                 [0, 0, 0, 0, 0, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3], 
                 [0, 0, 0, 0, 3, 3, 2, 2, 3, 3, 3, 3, 3, 3, 2], 
                 [0, 0, 0, 3, 3, 3, 2, 2, 3, 3, 3, 3, 3, 2, 2], 
                 [0, 0, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3, 2, 2, 2], 
                 [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2], 
                 [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2]]

############################
# Game Over 
############################

def gameOver_redrawAll(app, canvas):
    canvas.create_image(200, 300, image=ImageTk.PhotoImage(app.image2))
    canvas.create_text(app.width / 2, app.height / 2, 
    text = "Congrats! Levels completed.",
    font = "Hiragino 20")
    canvas.create_text(app.width / 2, app.height / 2 + 50,
    text = "Press any key to go back to the home screen.",
    font = "Hiragino 20")

def gameOver_keyPressed(app, event):
    app.mode = "homeScreenMode"

def gameOver_mousePressed(app, event):
    app.mode = "homeScreenMode"

############################
# Game Mode
############################

def gameMode_timerFired(app):
    if app.timePassed != None:
        app.timePassed += app.timerDelay
    if app.timePassed == 200:
        app.hintButtonColor = "white"
        app.undoButtonColor = "white"
        app.computeButtonColor = "white"
        app.firstButtonColor = "white"
        app.secondButtonColor = "white"
        app.timePassed = None
    if app.displayMessageTime != None:
        app.displayMessageTime += app.timerDelay
    if app.displayMessageTime == 1000:
        app.displayExceededMoves = False
        app.displayMesssageTime = None

def gameMode_mousePressed(app, event):
    if app.win: return # If the board has been won already, ignore all clicks
    if event.y >= app.height - app.margin - app.cellHeight:
        if event.y >= (app.height - (app.margin // 2)): 
            boxNumber = findBoxNumber(app, event.x)
            app.currColor = boxNumber
            app.xCoor = app.colorSelectionWidth * (boxNumber + 1)
        elif (app.height - app.margin <= event.y <= 
                app.height - app.margin + 30):
            app.displayHint = False
            if (10 <= event.x <= 100 and 
                app.height - app.margin < event.y < 
                app.height - app.margin + 15):
                app.mode = "homeScreenMode"   
                app.moveCounter = 0
                app.movesNeededForBoard = 0
                app.moves.clear()
                app.solverSolution.clear()
                app.hintCounter = 0
                app.win = False
                app.displayMoves = False
            elif (85 <= event.x <= 165):
                app.displayMoves = True
                app.computeButtonColor = "lightGrey"
                app.timePassed = 0
                fasterBFSHelper(app)
            elif (170 <= event.x <= 190):
                app.firstButtonColor = "lightGrey"
                app.timePassed = 0
                giveHint(app)
                calculateConnections(app)
            elif (195 <= event.x <= 215):
                app.secondButtonColor = "lightGrey"
                app.timePassed = 0
                giveHint(app)
                calculateRegionAreas(app)
            elif (220 <= event.x <= 290):
                app.undoButtonColor = "lightGrey"
                app.timePassed = 0
                undoMove(app)
            elif (296 <= event.x <= 365):
                app.hintButtonColor = "lightGrey"
                app.timePassed = 0
                if app.solverSolution == []:
                    BFSHelper(app)  
                fasterBFSHelper(app)
                printSolutionToSolveBoard(app)
                checkIfWin(app)
    else: 
        app.seen.clear()
        x = event.x
        y = event.y
        (row, col) = getRowCol(app, x, y)
        app.displayHint = False
        if not app.drawMode:
            clickedColor = app.board[row][col]
            if app.currColor == clickedColor: return
            flood(app, row, col, clickedColor, app.currColor)
            storeMove(app, copy.copy(app.seen), clickedColor)
            checkIfWin(app)
            checkIfPathDeviated(app)
            if exceededMoves(app):
                app.displayExceededMoves = True
                app.displayMessageTime = 0

# This function checks if the user has applied a move that is different from the
# autosolver's path, so that the solution can be updated if necessary. 
def checkIfPathDeviated(app):
    # If the user didn't call on the autsolver, simply return 
    if app.solverSolution == []: return 
    # If the user's move is different from the autosolver
    elif app.board != app.solverSolution[0].completeList:
        # Clear the solver's solution so it can recompute 
        app.solverSolution.clear()
    # If the user's move is the same from the autosolver
    elif app.board == app.solverSolution[0].completeList:
        # Pop the first move from the autosolver, since the user has applied
        # the move already
        app.solverSolution.pop(0)

# This function draws the board and the buttons for the game mode. 
def gameMode_redrawAll(app, canvas):
    drawBoard(app, canvas) 
    canvas.create_rectangle(0, app.height - app.margin - app.cellHeight, 
            app.width, app.height, fill = "white", outline = "black")
    yCoor = app.height - app.margin // 2
    colorWidth = app.width // app.numberOfColors
    for i in range(app.numberOfColors):
        xCoor = colorWidth * i 
        (r,g,b) = app.colors[i]
        color = rgbString(r,g,b)
        canvas.create_rectangle(xCoor, yCoor, xCoor + colorWidth, 
                                app.height, fill = color)
    canvas.create_rectangle(app.xCoor, yCoor, app.xCoor - 10, yCoor + 10, 
                            fill = "beige")
    canvas.create_rectangle(10, app.height - app.margin, 80, 
                app.height - app.margin+30, fill = "white", width = 0.5)
    canvas.create_text(45, app.height - app.margin + 15, text = "Back", 
                fill = "#D57E7E", font = "Hiragino")       
    canvas.create_rectangle(85, app.height - app.margin, 165, app.height -
                app.margin + 30, fill = app.computeButtonColor, width = 0.5)
    canvas.create_text(125, app.height - app.margin + 15, 
                text = "Compute!", 
                fill = "#D57E7E", font = "Hiragino")
    canvas.create_text(193, app.height - app.margin - 10, text = "low level:")
    canvas.create_rectangle(170, app.height - app.margin, 190, app.height - 
                app.margin + 30, fill = app.firstButtonColor, width = 0.5)
    canvas.create_text(181, app.height - app.margin + 15,
                text = "H1",
                fill = "#D57E7E", font = "Hiragino")
    canvas.create_rectangle(195, app.height - app.margin, 215, app.height - 
                app.margin + 30, fill = app.secondButtonColor, width = 0.5)
    canvas.create_text(206, app.height - app.margin + 15,
                text = "H2",
                fill = "#D57E7E", font = "Hiragino")      
    canvas.create_rectangle(220, app.height - app.margin, 290, app.height -
                app.margin + 30, fill = app.undoButtonColor, width = 0.5)
    canvas.create_text(255, app.height - app.margin + 15, text = "Undo!",
                fill = "#D57E7E", font = "Hiragino")
    canvas.create_text(330, app.height - app.margin - 10, text = "high level:")
    canvas.create_rectangle(295, app.height - app.margin, 365, app.height -
                app.margin + 30, fill = app.hintButtonColor, width = 0.5)
    canvas.create_text(330, app.height - app.margin+15, text = "Hint!", 
                fill = "#D57E7E", font = "Hiragino")
    printInfo(app, canvas)

def gameMode_keyPressed(app, event):
    if app.win: # Only act if the board has been won
        if app.level != None: # If the user is playing the levels 
            if event.key != "r": # Clicking any other key advances to next level
                app.level = app.level + 1
            # Generate the boards based on the level number
            if app.level == 1: createFirstBoard(app)
            elif app.level == 2: createSecondBoard(app)
            elif app.level == 3: createThirdBoard(app)
            elif app.level == 4: createFourthBoard(app) 
            elif app.level > 4: app.mode = "gameOver"
        # If the user was previously in draw mode (i.e. playing their board)
        else: 
            if event.key == "r": 
                createEmptyBoard(app) 
                app.mode = "drawMode"
            else:
                app.mode = "homeScreenMode"
        # Resetting all the values 
        app.moveCounter = 0
        app.movesNeededForBoard = 0
        app.moves.clear()
        app.solverSolution.clear()
        app.hintCounter = 0
        app.win = False
        app.displayMoves = False

# This function checks if a user has used more moves than necessary to solve 
# the board. 
def exceededMoves(app):
    # Using short circuit evaluation. If movesNeeded = 0, it means the user 
    # has not requested to compute the number of moves
    if (app.movesNeededForBoard != 0 and 
        app.moveCounter > app.movesNeededForBoard):
        return True
    return False

#################################
# Main App
#################################

# From the CMU 112 website (Graphics Week): 
# https://www.cs.cmu.edu/~112/notes/notes-graphics.html
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
    app.cellWidth  = app.width / app.cols
    app.cellHeight = (app.height - app.margin) / app.rows
    app.level = 1
    app.isErase = False
    app.colors = {0: (247, 246, 242),
                  1: (170, 216, 211),
                  2: (56,  62,  86),
                  3: (251, 116, 62)}
    app.numberOfColors = len(app.colors)
    app.board = []
    app.currColor = 0
    app.drawMode = False
    app.displayHint = False
    app.colorSelectionWidth = app.width // app.numberOfColors
    app.xCoor = app.colorSelectionWidth
    app.win = False
    createEmptyBoard(app)

    # Initializing variables for the flood filling
    app.seen = set()
    app.region = set()
    app.regionList = list()

    # Initializing variables for the hint system
    app.hintColor = 0
    app.hintCoordinate = (0,0)

    # Initializing variables for the autosolver system
    app.hintCounter = 0 
    app.solverSolution = list()
    app.displayMoves = False
    app.movesNeededForBoard = 0
    
    # Initializing variables for storing the user's moves 
    app.moves = []
    app.moveCounter = 0

    # Initializing the button clicking feature
    app.timerDelay = 100
    app.timePassed = None
    app.undoButtonColor = "white"
    app.hintButtonColor = "white"
    app.refreshButtonColor = "white"
    app.computeButtonColor = "white"
    app.firstButtonColor = "white"
    app.secondButtonColor = "white"

    # Initializing the message for when moves have been exceeded 
    app.displayExceededMoves = False 
    app.displayMessageTime = None

# This function stores the move that the user just made and updates the counter 
def storeMove(app, tiles, color):
    app.moveCounter += 1
    app.moves.append((tiles, color))

# This function finds the box that the user has clicked on to select a color 
def findBoxNumber(app, x):
    number = len(app.colors)
    width = app.width // number 
    return x // width

# This function checks if the user has won the board by checking if any row of 
# tiles has more than one color value. 
def checkIfWin(app):
    for row in app.board:
        boardSet = set(row)
        if len(boardSet) != 1: 
            app.win = False 
            return
    app.win = True

# This function undoes the most recent move made by the user. Will not undo 
# any moves made by the autosolver. 
def undoMove(app):
    if app.moves != []: 
        app.moveCounter -= 1
        (tiles, color) = app.moves.pop()
        for (row, col) in tiles:
            changeColor(app, row, col, color)

# This function changes the color of a tile given its row, col values 
def changeColor(app, row, col, color):
    if 0 <= row < app.rows and 0 <= col < app.cols:
        app.board[row][col] = color

# This function takes in the position of a mouse click and detects which 
# triangle it i (i.e. which row, col index triangular tile did the user select). 
def getRowCol(app, x, y):
    triangleSize = app.cellWidth / 2
    row = int(y / app.cellHeight) 
    col = int(x / app.cellWidth) 
    xcoordinate = getColCoordinate(app, col)
    ycoordinate = getRowCoordinate(app, row)
    # Utilizing some math to adjust the index of the row because triangular 
    # tiles are different from square tiles. This is because each row of square
    # tiles would technically contain two overlapping triangles, so the program
    # needs to be able to determine which triangle the user actually clicked on.
    xdiff = x - xcoordinate
    ydiff = y - ycoordinate
    if row % 2 == col % 2:
        if ydiff > xdiff: 
            row = row + 1
    elif row % 2 != col % 2: 
        if xdiff > triangleSize or ydiff > triangleSize: 
            row = row + 1
    return (row, col)

# This function creates a new empty board 
def createEmptyBoard(app):
    app.board = [([0] * app.cols) for _ in range(app.rows)]

# This function prints out all needed information to the user on the bottom bar 
# of the screen 
def printInfo(app, canvas):
    if app.drawMode:
        text = "Draw mode"
    else: 
        text = "Play mode"
        canvas.create_text(app.width - 15, app.height - app.margin + 15, 
                    text = f'Moves used: {app.moveCounter}', anchor = "e")
    canvas.create_text(app.width - 15, app.height - app.margin, 
                    text = text, fill = "blue", anchor = "e")
    if app.displayExceededMoves:
        canvas.create_rectangle(0, app.height / 2 - 80, 
        app.width, app.height / 2 - 60, fill = "white")
        canvas.create_text(app.width / 2, app.height / 2 - 70, 
        text = "You used more moves than necessary!")
    if app.displayHint:
        row, col = app.hintCoordinate
        (r,g,b) = app.colors[app.hintColor]
        color = rgbString(r, g, b)
        xcoordinate = getColCoordinate(app, col)
        ycoordinate = getRowCoordinate(app, row)
        canvas.create_text(xcoordinate, ycoordinate, text = "HERE!", 
                fill = color, font = "Hiragino 15 bold", anchor = "w")
    if app.displayMoves:
        canvas.create_text(app.width - 15, app.height - app.margin + 30, 
        text = f'Moves needed: {app.movesNeededForBoard}', fill = "red", 
        anchor = "e")
    if app.win: 
        canvas.create_rectangle(0, app.height / 2 - 80, 
            app.width, app.height / 2 - 10, fill = "white")
        canvas.create_text(app.width / 2, app.height / 2 - 65, 
            text = "YOU WON!", fill = "red")
        if app.level == None: 
            canvas.create_text(app.width / 2, app.height / 2 - 45, 
            text = "Press any key to return to home screen. " + 
                    "Press 'r' to draw another board!")
        else:
            canvas.create_text(app.width / 2, app.height / 2 - 45, 
            text = "Press any key for the next level. Press 'r' to retry.")
        if app.movesNeededForBoard == 0:
            canvas.create_text(app.width / 2, app.height / 2 - 25,
            text = ":)")
        elif exceededMoves(app):
            canvas.create_text(app.width / 2, app.height / 2 - 25,
            text = "You used more moves than necessary, but that's ok!", 
            fill = "brown")
        else:
            canvas.create_text(app.width / 2, app.height / 2 - 25,
            text = "You completed the board with the correct number of moves!", 
            fill = "green")

# This function draws the board stored in the app 
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            if (row % 2 == col % 2): 
                drawLeftTriangle(app, canvas, row, col)
            elif (row % 2 != col % 2):
                  drawRightTriangle(app, canvas, row, col)

# This function retrieves the y-coordinate given the index of a row 
def getRowCoordinate(app, row):
    boardHeight = app.height - app.margin
    coordinate = (boardHeight // app.rows) * row
    return coordinate 

# This function retrives the x-coordinate given the index of a column
def getColCoordinate(app, col):
    coordinate = (app.width // app.cols) * col
    return coordinate 

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
    canvas.create_polygon(x1, topY, x1, endY, x2, midY, fill = color, 
        width = 0.1, outline = "white")

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

# This function checks if a color change is legal for a given row, col tile 
def isLegal(app, row, col, clickedColor):
    # If out of bounds, reached another region, or seen this tile, return false 
    if ((row < 0 or row >= app.rows) or (col < 0 or col >= app.cols)
        or (app.board[row][col] != clickedColor) 
        or ((row, col) in app.seen)): 
        return False
    # Otherwise return True
    return True

############################
# Autosolver 
############################

# This function retrieves the next tile that has yet to be assigned to a region 
def getNextPosition(rows, cols, seen):
    # Loops through the entire board of tiles 
    for row in range(rows):
        for col in range(cols):
            # Sees if there are any tiles that haven't been seen yet 
            if (row, col) not in seen: 
                return (row, col)
    # If all tiles are seen, then return None
    return None

# This function checks if a tile being searched is a legal tile belonging to 
# the region we're currently building. Also builds up the "edges" of the region.
def checkIsLegal(row, col, rows, cols, color, board, edges, seen):
    # If out of bounds, return false
    if row < 0 or row >= rows or col < 0 or col >= cols: 
        return False
    # If reached another region, return false and add that row col to edges.
    # The edges will help determine which region is connected to which region
    elif board[row][col] != color: 
        edges.add((row,col))
        return False
    # If we've already looked at this tile, return false
    elif (row, col) in seen: 
        return False 
    # Otherwise, return true
    return True

# This function searches for the tiles that make up a region on the board 
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
    # Keep finding new regions as long as we haven't searched all the tiles yet
    while len(seen) != rows * cols:
        index += 1
        position = getNextPosition(rows, cols, seen)
        currRegion = set()
        currRegionEdges = set()
        if position == None: return # If finished searching the board, stop
        else:
            checkX, checkY = position
            color = boardList[checkX][checkY]
            # Find all the tiles belonging to that region as well as the 
            # edges that define that region. 
            searchForTiles(checkX, checkY, rows, cols, color, boardList, seen, 
                                            currRegionEdges, currRegion)
            # Use the set of tiles and the edges to create a new Region object
            newRegion = Region(index, color, currRegion, currRegionEdges)
            regionList.append(newRegion)
    # After the list of regions has been created, form their connections
    createConnectionsUsingList(regionList)
    return regionList

# This sets up the "connecting regions" for each region on the board
def createConnectionsUsingList(regionList):
    for region1 in regionList:
        neighbors = list()
        # Searches through all the edges and finds the regions that have
        # those edges (i.e. they are neighbors)
        for (row, col) in region1.edges:
            for region2 in regionList:
                if (row, col) in region2.tiles and region2 not in neighbors:
                   neighbors.append(region2)
        region1.neighbors = neighbors

# For the starting board, loop through each region and try each color 
# (i.e. attempt every possible move for the given board)
def createChildrenBoardsForBoard(board):
    for region in board.regionList:
        colors = region.getNeighborColors() 
        # Loop through the colors of the region's neighbors
        # Only apply those colors because any other color wouldn't be 
        # a purposeful move to solve the board 
        for color in colors:
            # Create a new Board based on that move 
            childCompleteList = createChildForRegion(region, color, board)
            childRegionList = createRegionList(childCompleteList)
            childBoard = Board(childRegionList, childCompleteList)
            # Set up the parent-child relations between the two boards
            childBoard.parent = board
            board.addChild(childBoard)
    return board.children

# For a given region, create the resulting board after implementing the move 
def createChildForRegion(regionChange, color, board):
    newList = copy.deepcopy(board.completeList)
    for (row, col) in regionChange.tiles:
        newList[row][col] = color
    return newList
    
# This function creates an adjacency list for a board given its regions. Forms 
# key value pairs (each region is a key and each value is a list of its 
# neighboring regions)
def createAdjacencyList(regionList):
    adjacencyList = dict() 
    # Goes through each region and sets up a key
    for region in regionList: 
        adjacencyList[(region.name, region.color)] = set()
        # Adds each neighboring region to the associated value list 
        for neighbor in region.neighbors: 
            neighborTuple = (neighbor.name, neighbor.color) 
            adjacencyList[(region.name, region.color)].add(neighborTuple)
    return adjacencyList

# This function creates the children boards given an initial adjacency list 
# i.e. applies all the move for a given board to create new boards
def createChildrenUsingAdjacencyList(adjList):
    children = list()
    for region in adjList:
        # Find all the colors of its neighbors
        neighborColors = set()
        for neighbor in adjList[region]:
            neighborColors.add(neighbor[1])
        # Loop through each color and apply the move to create the child
        for color in neighborColors:
            childAdjList = createChildForRegionUsingAdj(region, color, adjList)
            children.append(childAdjList)
    return children

# This function creates a child board by taking in the adjacency list 
# that represents the current board, the region that we wish to change,
# and the color we wish to change it to. It then merges the appropriate 
# regions and creates a new adjacency list representing the resulting board.
def createChildForRegionUsingAdj(regionChange, color, adlist):
    childAdjList = copy.deepcopy(adlist) 
    mergedRegions = {regionChange} 
    oldNeighbors = copy.deepcopy(childAdjList[regionChange]) 
    newRegionTuple = (regionChange[0], color) 
    mergedRegionNeighbors = list()
    newNeighbors = set()
    # Loop through all the neighbors of the region we're about to change
    for (neighborName, neighborColor) in childAdjList[regionChange]: 
        if neighborColor == color: # If the color matches 
            # Add it to the merged regions 
            mergedRegions.add((neighborName, neighborColor)) 
            # Add its neighbors to the merged region's neighbors
            mergedRegionNeighbors.extend(childAdjList[(neighborName, 
                                                        neighborColor)]) 
    # Loop through each of them and add it to the newNeighbors set, 
    # as long as it isn't one of the regions we've merged
    for neighbor in mergedRegionNeighbors: 
        if neighbor not in mergedRegions:
            newNeighbors.add(neighbor)
    # Do the same for the old neighbors
    for neighbor in oldNeighbors: 
        if neighbor not in mergedRegions:
            newNeighbors.add(neighbor)
    # Delete all the merged regions from the dictionary
    for region in mergedRegions:
        del childAdjList[region]
    # Set up the new region in the dictionary
    childAdjList[newRegionTuple] = newNeighbors 
    # Loop through each of the regions in the dictionary
    for key in childAdjList: 
        newNeighbors = set()
        # Create a new list of neighbors containing only 
        # those that haven't been merged during the move 
        for neighbor in childAdjList[key]:
            if neighbor not in mergedRegions: 
                newNeighbors.add(neighbor)
        newNeighbors.add(newRegionTuple)
        childAdjList[key] = newNeighbors 
    return childAdjList

# Using recursion to get the path from the resulting board back to the parent
def getPath(app, halfwayBoard, currBoard):
    # Base case: when we've reached the starting board
    if halfwayBoard == currBoard: 
        return []
    # Recursive case: retrieve the parent of each intermediate board and 
    # form a list of the boards going in order from starting to completed (won)
    else: 
        return getPath(app, halfwayBoard.parent, currBoard) + [halfwayBoard]

# This gives out the hints to solve the board
def printSolutionToSolveBoard(app):
    app.moveCounter += 1
    # If we haven't computed the solution or we've already used up all the hints
    # then return to stop the function 
    if app.solverSolution == []: 
        return
    # Retrieve the next move
    nextMove = app.solverSolution.pop(0)
    # Update the board using the data from the next move to display the hint
    # to the user 
    for region in nextMove.regionList:
        for (row, col) in region.tiles:
            app.board[row][col] = region.color

# This function initializes the starting node and calls the fasterBFS to find 
# the fewest number of moves needed to solve this board
def fasterBFSHelper(app):
    adlist = createAdjacencyList(createRegionList(app.board))
    app.movesNeededForBoard = fasterBFS(adlist)
    app.movesNeededForBoard += app.moveCounter
    app.displayMoves = True

# This function initializes the starting node and calls BFS to find the solution
def BFSHelper(app):
    regionList = createRegionList(app.board)
    # If presented with an empty board, don't try to solve 
    if len(regionList) == 1: 
        app.win = True
        return
    currBoard = Board(regionList, app.board)
    resultingBoard = BFS(currBoard)
    app.solverSolution = getPath(app, resultingBoard, currBoard)

# Learned the overall concept of BFS via 
# https://en.wikipedia.org/wiki/Breadth-first_search 
# and through notes from the TA-led mini lecture "Graph Algorithms". Referenced 
# https://www.educative.io/edpresso/how-to-implement-a-breadth-first-search-in-python
# for the structure of a BFS algorithm in python. Applied those concepts below 
# for my program (for both BFS and fasterBFS)
def BFS(startingBoard):
    queue = list()
    visited = set()
    visited.add(startingBoard)
    queue.append(startingBoard)

    while queue != []:
        currState = queue.pop(0) 
        children = createChildrenBoardsForBoard(currState)
        for child in children:
            if child not in visited:
                if len(child.regionList) == 1: 
                    return child
                else:
                    visited.add(child)
                    queue.append(child)
    return None

# A faster BFS algorithm that uses a simpler representation of the board.
# This only computes the number of moves needed, not the path. 
def fasterBFS(startingd):
    queue = list()
    visited = list()
    level = 0
    queue.append(1)
    visited.append(startingd)
    queue.append(startingd)

    while queue != []:
        currState = queue.pop(0) 
        # This tracks the depth of the BFS in order to determine how many 
        # moves we've applied to get to the solution. Referenced some comments
        # from https://stackoverflow.com/questions/31247634/how-to-keep-track-of-depth-in-breadth-first-search 
        # to get a sense of how this can be done but did not copy code directly. 
        if isinstance(currState, int):
            if currState > level: level = currState
        else:
            children = createChildrenUsingAdjacencyList(currState)
            for child in children:
                if child not in visited:
                    if len(child) == 1: 
                        return level
                    else:
                        visited.append(child)
                        queue.append(level + 1)
                        queue.append(child)
    return 0 

########################
# Low level hint system
########################

# This function prints out instructions for what a possible "next best move"
# could be for the current board using the number of connections of a region
def calculateConnections(app):
    region = findRegionWithMostConnections(app)
    color = findColorToClick(region)
    regionTiles = list(region.tiles)
    position = regionTiles[len(regionTiles)//2]
    app.hintColor = color
    app.hintCoordinate = position

# This returns the region on the board with the most neighbors  
def findRegionWithMostConnections(app):
    bestNumber = 0
    bestRegion = None
    for region in app.regionList:
        connections = len(region.neighbors)
        if connections > bestNumber: 
            bestNumber = connections 
            bestRegion = region 
    return bestRegion  

# This function finds the color to click on based on how many neighbors have the 
# same color. The most "popular" color of a region's neighbors would be the 
# best color to change that region to (so we can merge the largest number of 
# regions together)
def findColorToClick(region):
    colorDict = dict()
    for neighbor in region.neighbors:
        currColor = neighbor.color
        colorDict[currColor] = colorDict.get(currColor, 0) + 1
    bestColor = 0
    bestCount = 0
    for key in colorDict:
        if bestCount < colorDict[key]:
            bestCount = colorDict[key]
            bestColor = key
    return bestColor

# This finds the region with the neighbor that is the largest (i.e. the region 
# that is connected to another color that covers the most space on the screen) 
def calculateRegionAreas(app):
    regionNeighborDict = dict()
    for region in app.regionList:
        (bestColor, bestNumber) = findConnectionWthMostArea(region)
        regionNeighborDict[region.name] = (bestColor, bestNumber)
    bestArea = 0
    bestColor = 0
    bestKey = 0
    for key in regionNeighborDict:
        if bestArea < regionNeighborDict[key][1]:
            bestArea = regionNeighborDict[key][1]
            bestColor = regionNeighborDict[key][0]
            bestKey = key
    regionTiles = list(app.regionList[bestKey].tiles)
    position = regionTiles[len(regionTiles)//2]
    app.hintCoordinate = position
    app.hintColor = bestColor

# This searches through each of the connecting neighbors of a given region and  
# returns the neighboring color with the greatest amount of tiles (i.e. area)
def findConnectionWthMostArea(region):
    connectingAreas = dict() 
    for neighbor in region.neighbors:
        color = neighbor.color 
        area = len(neighbor.tiles)
        connectingAreas[color] = connectingAreas.get(color, 0) + area 
    bestNumber = 0
    bestColor = 0
    for key in connectingAreas:
        if bestNumber < connectingAreas[key]:
            bestNumber = connectingAreas[key]
            bestColor = key
    return (bestColor, bestNumber)

# This function sets up the variables needed to compute a hint.
def giveHint(app):
    app.displayHint = True
    app.seen.clear()
    app.regionList = createRegionList(app.board)

############################
# Run app 
############################ 

def kamiApp():
    runApp(width=500, height=600)

kamiApp()