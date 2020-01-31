from tkinter import *
from math import *  
from time import *
from random import *

root = Tk()
screen = Canvas(root, width=800, height=800, background="black")
screen.pack()

#To prevent crash if user clicks the "r" key during intro screen 
global difficulty
difficulty = "Medium"

#Default paramater values for game
def setInitialValues():
    global trueThief, insults, randomInsults, won, isFound, gameRunning, winConditionX, winConditionY, xSpeed, ySpeed, x1CHead, y1CHead, x2CHead, y2CHead, x1Coin, y1Coin, x2Coin, y2Coin, direction, randomNum, x1Head, y1Head, x2Head, y2Head, x1Body, y1Body, x2Body, y2Body, cXSpeed, cYSpeed, dangerRadius
    trueThief = False #trueThief must be true for the user to pass through the gate. Therefore, accquring trueThief = True is necessary for victory 
    isFound = False #Variable that detects whether user has been found by clown or has collided with external objects
    won = False #Detects whether user has won or not
    gameRunning = True
    xSpeed = 0
    ySpeed = 0
    x1CHead = randint(400, 600)
    y1CHead = randint(100, 600)
    x2CHead = x1CHead + 40
    y2CHead = y1CHead + 40
    x1Coin = randint(400, 600)
    y1Coin = randint(400, 450)
    x2Coin = x1Coin + 40
    y2Coin = y1Coin + 40
    randomNum = randint(400, 700)
    x1Head = 40
    y1Head = 340
    x2Head = 60
    y2Head = 360
    x1Body = 45
    y1Body = 360
    x2Body = 55
    y2Body = 385
    cXSpeed = 0
    cYSpeed = 0
    winConditionX = ""
    winConditionY = ""
    dangerRadius = 10 #Starting radius for the clowns detection zone 
    insults = ["nerd", "geek", "nimrod", "mouthbreather", "environmental-enemy", "cs-hater", "clown"] #You'll see where this comes to play soon >:D
    randomInsults = choice(insults)
    if y1CHead >= 100 and y1CHead <= 200:
        direction = "top"
    elif y1CHead >= 201 and y1CHead <= 400:
        direction = "right"
    else:
        direction = "bot"

#Intro: "Clowns vs. THIEF!" screen
def intro():
    global introBackground
    introBackground = screen.create_rectangle(0, 0, 800, 800, fill = "blanchedalmond")
    clownText = screen.create_text(400, 300, text = "Clown", font = "fixedsys 80", fill = "red")
    vsText = screen.create_text(400, 400, text = "vs", font = "fixedsys 30", fill = "skyblue")
    thiefText = screen.create_text(400, 500, text = "THIEF!", font = "fixedsys 80", fill = "black")
    screen.update()
    sleep(3)
    screen.delete(clownText, vsText, thiefText)

#Function to load game into Medium difficulty settings 
def medButtonPressed():
    global difficulty
    difficulty = "Medium"
    mediumButton.destroy()
    legendaryButton.destroy()
    runGame()

#Function to load game into Legendary difficulty settings. This mode is not for the beginner and is meant as a challenge for experienced players.
def legendButtonPressed():
    global difficulty
    difficulty = "Legendary"
    mediumButton.destroy()
    legendaryButton.destroy()
    runGame()

#Loads main menu
def mainMenu():
    global mediumButton, legendaryButton
    menuActivated = True
    difficultyText = screen.create_text(400, 300, text = "Choose your difficulty", font = "fixedsys 20", fill = "red")
    mediumButton = Button(root, text = "MEDIUM!", font = "fixedsys 50", foreground="purple", command = medButtonPressed, background="slate grey") #If this button is clicked, the medButtonPressed function is ran and the game initaties on Medium difficulty
    mediumButton.pack()
    mediumButton.place(x = 0, y = 400)
    legendaryButton = Button(root, text = "LEGENDARY!", font = "fixedsys 50", foreground="gold", command = legendButtonPressed, background="slate grey") #If this button is clicked, the legendButtonPressed function is ran and the game initaties on Legendary difficulty
    legendaryButton.pack()
    legendaryButton.place(x = 350, y = 400)
    screen.update()

#Creates colour background for main game
def createBackground():
    global background
    #General-wide background 
    background = screen.create_rectangle(0, 0, 800, 800, fill = "grey", outline = "red", width = 50)

#Draws the character that the user controls 
def drawPlayer():
    
    #Head
    playerHead = screen.create_oval(x1Head, y1Head, x2Head, y2Head, fill = "blanchedalmond")
    #Mask
    playerMask = screen.create_arc(x1Head, y1Head, x2Head, y2Head, start = 180, extent = 180, fill = "black") 
    #Eyes
    playerEyes1 = screen.create_oval(x1Head+5, y1Head+4, x1Head+8, y1Head+7, fill = "black")
    playerEyes2 = screen.create_oval(x1Head+15, y1Head+4, x1Head+12, y1Head+7, fill = "black")
    #Body
    playerBody = screen.create_rectangle(x1Body, y1Body, x2Body, y2Body, fill = "black")
    #Arms
    playerArm1 = screen.create_rectangle(x1Body, y1Body, x1Body-10, y1Body+5, fill = "black")
    playerArm2 = screen.create_rectangle(x2Body, y1Body+5, x2Body+10, y1Body, fill = "black")
    #Hands
    playerHand1 = screen.create_oval(x1Body-10, y1Body+5, x1Body-15, y1Body, fill = "blanchedalmond")
    playerHand2 = screen.create_oval(x2Body+10, y1Body+5, x2Body+15, y1Body, fill = "blanchedalmond")
    #Legs
    playerLeg1 = screen.create_rectangle(x1Body, y2Body, x1Body+2.5, y2Body+10, fill = "pink")
    playerLeg2 = screen.create_rectangle(x2Body-3.5, y2Body, x2Body, y2Body+10, fill = "pink")
    #Hitbox: if this interacts with other objects, it will count as collision. The hitbox is made carefully. It can be observed by changing the colour. 
    playerHitbox = screen.create_rectangle(x1Body-10, y1Head, x2Body+10, y2Body+10, outline = "grey") 

#Draws the clown
def drawClown():
    global x1CHead, y1CHead, x2CHead, y2CHead

    #Head
    clownHead = screen.create_oval(x1CHead, y1CHead, x2CHead, y2CHead, fill = "white")
    #Hair
    clownHair = screen.create_polygon(x1CHead, y1CHead+10, x1CHead, y1CHead-20, x2CHead, y1CHead-20, x2CHead, y1CHead+10, fill = "orange", smooth = True)
    #Eyes
    clownEyes1 = screen.create_oval(x1CHead+10, y1CHead+12, x1CHead+16, y1CHead+18, fill = "green", outline = "red", width = 0.5)
    clownEyes2 = screen.create_oval(x1CHead+30, y1CHead+12, x1CHead+24, y1CHead+18, fill = "green", outline = "red", width = 0.5)
    #Nose
    clownNose = screen.create_oval(x1CHead+16, y1CHead+20, x1CHead+24,y1CHead+28, fill = "red")
    #Mouth
    clownMouth = screen.create_polygon(x1CHead+10, y1CHead+32, x1CHead+20, y1CHead+37, x1CHead+30, y1CHead+32, fill = "blanchedalmond", outline = "red", width = 2)
    #Body
    clownBody = screen.create_oval(x2CHead, y2CHead, x1CHead, y2CHead+80, fill = "green")
    #Arms
    clownArm1 = screen.create_rectangle(x2CHead+25, y2CHead+10, x2CHead-10, y2CHead+15, fill = "green")
    clownArm2 = screen.create_rectangle(x1CHead-25, y2CHead+10, x1CHead+10, y2CHead+15, fill = "green")
    #Hands
    clownHand1 = screen.create_oval(x2CHead+15, y2CHead, x2CHead+40, y2CHead+25, fill = "white")
    clownHand2 = screen.create_oval(x1CHead-15, y2CHead, x1CHead-40, y2CHead+25, fill = "white")
    #Legs
    clownLeg1 = screen.create_rectangle(x1CHead+13, y2CHead+80, x1CHead+18, y2CHead+120, fill = "green")
    clownLeg2 = screen.create_rectangle(x1CHead+22, y2CHead+80, x1CHead+27, y2CHead+120, fill = "green")
    
#Draws the danger radius around the clown
def drawRadius():
    global dangerRadius, x1CHead, y1CHead, x2CHead, y2CHead
    radius = screen.create_oval(x1CHead-dangerRadius, y1CHead-dangerRadius, x2CHead+dangerRadius, y2CHead+dangerRadius, outline = "red") #Draws the radius by using the clowns x1,y1 and x2,y2 head coordinates as the center of it

#Draws the coins
def drawCoin():
    global x1Coin, y1Coin, x2Coin, y2Coin, trueThief
    
    #This boolean statement allows the player to "collect" the coin
    if trueThief == False:
        coin = screen.create_oval(x1Coin, y1Coin, x2Coin, y2Coin, fill = "yellow") 
        coinPattern = screen.create_rectangle(x1Coin+18, y1Coin+5, x1Coin+22, y2Coin-5, outline = "black")

#Draws and updates the text in the top right corner that displays whether the user has collected the coin or not
def hasUserCollectedCoin():
    global trueThief, thiefText
    #If trueThief is on, the user has collected the coin. Otherwise, they have not 
    if trueThief == True:
        thiefText = screen.create_text(650, 50, text = "Have you collected the coin: " + str("Yes"), font = "Arial 10")
    else:
        thiefText = screen.create_text(650, 50, text = "Have you collected the coin: " + str("No"), font = "Arial 10")

#Draws the exit gate that the user uses to win
def drawGate():
    global randomNum, winConditionX, winConditionY, gate, direction
    #The gates are placed differently depending on the random variable, "direction"
    if direction == "top":
        gate = screen.create_rectangle(randomNum, 0, randomNum + 75, 25, fill = "green", outline = "black")
        winConditionX = randomNum+37.5 #The winCondition variables are used later in the code to detect whether the user has won or not
        winConditionY = 25
    elif direction == "right":
        gate = screen.create_rectangle(775, randomNum, 800, randomNum+75, fill = "green", outline = "black")
        winConditionX = 787.5
        winConditionY = randomNum+37.5
    elif direction == "bot":
        gate = screen.create_rectangle(randomNum, 775, randomNum + 75, 800, fill = "green", outline = "black")
        winConditionX = randomNum+37.5
        winConditionY = 787.5

#Updates all positions
def updatePositions():
    global x1Body, y1Body, x2Body, y2Body, x1Head, y1Head, x2Head, y2Head, x1CHead, y1CHead, x2CHead, y2CHead, dangerRadius, clownDirections, randomDirection, cXSpeed, cYSpeed, difficulty

    #Updates players positions 
    x1Body = x1Body + xSpeed
    y1Body = y1Body + ySpeed
    x2Body = x2Body + xSpeed
    y2Body = y2Body + ySpeed
    x1Head = x1Head + xSpeed
    y1Head = y1Head + ySpeed
    x2Head = x2Head + xSpeed
    y2Head = y2Head + ySpeed

    #Updates danger radius
    if dangerRadius == 200:
        dangerRadius = dangerRadius - 100
    else:
        if difficulty == "Medium":
            dangerRadius = dangerRadius + 2
        else:
            dangerRadius = dangerRadius + 5

    clownDirections = ("top", "left", "bot", "right")
    randomDirection = choice(clownDirections)
    #Makes the clown go in random directions
    #The greater and less than signs prevent the clown from going anywhere near the edges of the map to guarantee a fun playthrough experience for all. 
    if randomDirection == "top" and y1CHead > 100:
            cXSpeed = 0
            cYSpeed = -4
            if difficulty == "Legendary":
                cXSpeed = 0
                cYSpeed = -6
            for i in range(4):
                x1CHead = x1CHead + cXSpeed
                y1CHead = y1CHead + cYSpeed
                x2CHead = x2CHead + cXSpeed
                y2CHead = y2CHead + cYSpeed

    if randomDirection == "left" and x1CHead-40 > 100:
            cXSpeed = -4
            cYSpeed = 0
            if difficulty == "Legendary":
                cXSpeed = -6
                cYSpeed = 0
            for i in range(4):
                x1CHead = x1CHead + cXSpeed
                y1CHead = y1CHead + cYSpeed
                x2CHead = x2CHead + cXSpeed
                y2CHead = y2CHead + cYSpeed
                
    if randomDirection == "bot" and y2CHead+120 < 700:
            cXSpeed = 0
            cYSpeed = 4
            if difficulty == "Legendary":
                cXSpeed = 0
                cYSpeed = 6
            for i in range(4):
                x1CHead = x1CHead + cXSpeed
                y1CHead = y1CHead + cYSpeed
                x2CHead = x2CHead + cXSpeed
                y2CHead = y2CHead + cYSpeed

    if randomDirection == "right" and x2CHead+40 < 700:
            cXSpeed = 4
            cYSpeed = 0
            if difficulty == "Legendary":
                cXSpeed = 6
                cYSpeed = 0
            for i in range(4):
                x1CHead = x1CHead + cXSpeed
                y1CHead = y1CHead + cYSpeed
                x2CHead = x2CHead + cXSpeed
                y2CHead = y2CHead + cYSpeed

#Detects collisions between objects
def checkForCollisions():
    global x2Head, y2Head, x1Body, x2Body, y1Body, y2Body, x1CHead, y1CHead, x2CHead, y2CHead, x1Coin, y1Coin, dangerRadius, isFound, won, trueThief, winConditionX, winConditionY

    #Hitbox parameters 
    top_left = (x1Body-10, y1Head)
    top_right = (x2Body+10, y1Head)
    bottom_left = (x1Body-10, y2Body+10)
    bottom_right = (x2Body+10, y2Body+10)
    corners = [top_left, top_right, bottom_left, bottom_right]

#Function to check whether coordinate is in a circle
    def checkCollision(coordinates, centerX, centerY, radius):
        x = coordinates[0]
        y = coordinates[1]
        #This is the math formula to determine whether coordinates are found anywhere in a circle
        if (x - centerX)**2 + (y-centerY)**2 < radius**2:
            return True
        return False

    #For loop to check if any of the 4 hitbox coordinates are in the dangerRadius
    for i in range(0, 4):
        if checkCollision(corners[i], x1CHead + 20, y1CHead + 20, dangerRadius):
            isFound = True
        if checkCollision(corners[i], x1Coin, y1Coin, 20):
            trueThief = True
            
    #Function to check the distance between any two objects
    def getDistance(x1, y1, x2, y2):
        return sqrt((x2-x1)**2+(y2-y1)**2)
    
    #Detects collision between player and gate
    if getDistance(x2Body, y1Body+20, winConditionX-10, winConditionY+10) < 35 and trueThief == True:
        won = True
    #Lava makes the player lose if there head hits it
    elif y2Head < 40:
        isFound = True
    #Lava makes the player lose if there legs hit
    elif y2Body > 760:
        isFound = True
    #Lava make the player lose if there arms hit
    elif x1Body-10 < 20 or x2Body+10 > 770:
        isFound = True

#Screen for when the player loses
def lossScreen():
    global randomInsults
    screen.create_rectangle(0, 0, 800, 800, fill = "black")
    screen.create_text(400, 350, text = "GAME OVER!", font = " fixedsys 40", fill = "white")
    screen.create_text(400, 450, text = "Press r to play again", font = "fixedsys 10",  fill = "white")
    #The user is randomly insulted using the randomInsults variable defined above
    screen.create_text(400, 550, text = "Or press q to quit, you " + str(randomInsults), font = "fixedsys 10",  fill = "white")

#Screen for when the player wins
def victoryScreen():
    screen.create_text(400, 350, text = "YOU WIN!", font = " fixedsys 40", fill = "white")
    screen.create_text(400, 450, text = "Press r to play again", font = "fixedsys 10", fill = "white")
    #The user is randomly insulted using the randomInsults variable defined above
    screen.create_text(400, 550, text = "Or press q to quit, you " + str(randomInsults), font = "fixedsys 10", fill = "white")

#Ends the game - this function also ends the entire program
def endGame():
    root.destroy()

#Loads all pre-game functions. It is added to allow the root.after to not have to run the game immediately
def start():
    intro()
    mainMenu()

#Globals the speed values for the player
def keyUpHandler( event ):
    global xSpeed, ySpeed
    xSpeed = 0
    ySpeed = 0
        
def keyDownHandler( event ):
    global xSpeed, ySpeed
    if event.keysym == "Left":
        xSpeed = -5 
    elif event.keysym == "Right":
        xSpeed = 5 
    elif event.keysym == "Up":
        ySpeed = -5 
    elif event.keysym == "Down":
        ySpeed = 5 
    elif event.keysym == "q":
        endGame()
    elif event.keysym == "r":
        runGame()

#Runs the entire game
def runGame():
    global difficultyText, introBackground, mediumButton, legendaryButton, gameRunning, isFound, won
    mediumButton.destroy()
    legendaryButton.destroy()
    screen.update()
    setInitialValues()
    while gameRunning == True:
        createBackground()
        drawPlayer()
        drawClown()
        drawRadius()
        drawCoin()
        hasUserCollectedCoin()
        drawGate()
        screen.update()
        sleep(0.03)
        screen.delete("all")
        updatePositions()
        checkForCollisions()
        #If the user has won, stop the game and run the victory screen
        if won == True:
            gameRunning = False
            victoryScreen()
        #If the user has lost, stop the game and run the loss screen
        if isFound == True:
            gameRunning = False
            lossScreen()

root.after( 0, start )

screen.bind( "<Key>", keyDownHandler )
screen.bind( "<KeyRelease>", keyUpHandler )

screen.pack()
screen.focus_set()
root.mainloop()









