#
# CS 177 - project3.py
# Devin Ersoy, 00305545351 Juliana Peckenpaugh, 0030606114, Emelie Coleman, 0031104038
# Following Coding Standards and Guidelines
# This program creates a control window and a game window. The control window is used to get a payer's
#   name, start a game, or exit a game. The program has a game window where the players name will appear
#   what round they're on, and how many clicks have happened. Also in this window, a 15x15 grid of black
#   circles will appear and when clicked they change colors to their 'hidden' color. When the user finds
#   the gold circle that marks the end of the round, a message is displayed and the user may continue.
#   When the game ends, the players name and score is written to a file called 'scores.txt.' and displayed
#   in controlwin. In addition, this program will also draw a red circle which increases score by 5 once
#   clicked. After the game completes, the golden circle will animate for 5 seconds and remove 2 clicks 
#   based on times it was clicked. Once exit is clicked, the game will close. Otherwise, game will continue
#   running after 5 rounds with a restart. For extra additions, there are sounds for every click on circles 
#   along with respective celebration sounds and bummer sound when redcirc is clicked. In addition, after
#   the 5th round, there is a video with the creators of the project clapping. The last addition is an 
#   easter egg. Once the q button is typed, cheats are activated for the game outlining where goldcirc and
#   redcirc is until the next round.
#

# Import necessary libraries
from graphics import *
from time import time, sleep
from math import sqrt
from random import randint
import platform
import os

# Import winsound if system is windows
if platform.system() == 'Windows':
    import winsound

####################################################################################################################################################################

# Define the game control function
def GameControl():
    # Create control window
    win = GraphWin('Game Control', 250, 200, autoflush=False)

    # Create and display Boiler Gold Hunt! title
    titlebar = Rectangle(Point(0,0), Point(250, 30))
    titlebar.setFill('black')
    titlebar.draw(win)
    title = Text(Point(125, 15), 'BOILER GOLD HUNT!')
    title.setStyle('bold')
    title.setSize(13)
    title.setFill('gold')
    title.draw(win)

    # Create and display player name entry box and title
    name = Text(Point(80,50), 'PLAYER NAME')
    name.setStyle('bold')
    name.setSize(10)
    name.draw(win)
    inputbox = Entry(Point(185,50), 6)
    inputbox.setSize(16)
    inputbox.setFill('white')
    inputbox.draw(win)

    # Create and display the top scores and text title
    topscores = Text(Point(125,80), 'TOP SCORES')
    topscores.setStyle('bold')
    topscores.setSize(13)
    topscores.draw(win)
    # Open the file
    scoresfile = open('scores.txt', 'r')
    # Make the file a list of strings
    scores = scoresfile.readlines()
    top3 = []
    # Get the top 3 names and scores
    i = 0
    while i < 3:
        if len(scores) == i:
            break
        top3.append(scores[i].rstrip('\n').replace(' ', '').split(','))
        place = Text(Point(95,100+i*17), top3[i][0])
        place.setSize(11)
        place.draw(win)
        score = Text(Point(155,100+i*17), top3[i][1])
        score.setSize(11)
        score.draw(win)
        i += 1
    # Close the file
    scoresfile.close()

    # Create and display New Game button
    newgamerect = Rectangle(Point(5, 155), Point(105, 190))
    newgamerect.setFill('gold')
    newgamerect.draw(win)
    newgamelabel = Text(Point(55, 172.5), 'NEW GAME')
    newgamelabel.setStyle('bold')
    newgamelabel.setSize(10)
    newgamelabel.draw(win)

    # Create and display Exit button
    exitrect = Rectangle(Point(180, 155), Point(245,190))
    exitrect.setFill('black')
    exitlabel = Text(Point(212.5, 172.5), 'EXIT')
    exitlabel.setFill('white')
    exitlabel.setStyle('bold')
    exitlabel.setSize(10)
    exitrect.draw(win)
    exitlabel.draw(win)

    # Return the inputbox and graphics window 
    return inputbox, win

####################################################################################################################################################################

# Define the goldhunt funtion
def GoldHunt():
    # Create the window
    win = GraphWin('GoldHunt', 480, 520, autoflush=False)

    # Create and display black recatngle for 
    rclabel = Rectangle(Point(0, 0), Point(480, 40))
    rclabel.setFill('black')
    rclabel.draw(win)

    # Display round label
    rounds = Text(Point(60, 20), 'Round: 0')
    rounds.setFill('gold')
    rounds.setStyle('bold')
    rounds.setSize(11)
    rounds.draw(win)

    # Display clicks title
    clicks = Text(Point(420, 20), 'Clicks: 0')
    clicks.setFill('gold')
    clicks.setStyle('bold')
    clicks.setSize(11)
    clicks.draw(win)

    # Return the round, clicks, and window
    return win, rounds, clicks
    
####################################################################################################################################################################

# Define the MakeCircles function
def MakeCircles(name, win):
    # Display where the players name will appear in the game window
    player = Text(Point(240, 20), 'Player: {0}'.format(name))
    player.setStyle('bold')
    player.setFill('gold')
    player.draw(win)
    
    # Start with an empty list and fill is with 225 black circle in a grid shape
    circles = []
    for i in range(15):
         for j in range(15):
            circle = Circle(Point(30 + i*30, 70 + j*30), 15)
            circle.setFill('black')
            circle.setOutline('black')
            circles.append(circle)

    # Draw these circles in the game window
    for circle in circles:
        circle.draw(win)

    # Make the list of appropriate colors for the circle based on where the gold circle is
    randnum = randint(0,224)

    #   Start with a list of the color white for each circle
    colors = ['white' for i in range(225)]

    #   Whatever index the gold circle is then assign gold, gray, and tan to appropriate circles
    for i in range(225):
        if i == randnum:
            colors[i] = 'gold'
        if i in [randnum-1, randnum+1, randnum+16, randnum+15, randnum+14, randnum-16, randnum-15, randnum-14]:
            colors[i] = 'tan'
        if i in [randnum-32, randnum-31, randnum-30, randnum-29, randnum-28, randnum+28, randnum+29, randnum+30, randnum+31, randnum+32, randnum-2, randnum+2, randnum-17,  randnum-13, randnum+17, randnum+13, randnum-13]:
            colors[i] = 'lightgray'
    
    # Create a random integer for which the red circle will be placed
    randrednum = randint(0,224)

    # Define a while loop to iterate until red circle location is not that of red index
    while randrednum == randnum:
        randrednum = randint(0,224)

    # Color specified circle to red
    colors[randrednum] = 'red'

    # Reset Cheats to normal board
    circles[randnum].setOutline('black')
    circles[randrednum].setOutline('black')

    # Return list of circles and color assignments
    return circles, colors, player, randrednum, randnum

###################################################################################################################################################################

# Define the goldmess function
def goldmess(golddistance, controlwin, ghwin, circles, goldcirc, roundcontinues, click, clickcount, player, roundn, clicks):
    print("goldmess")
    # If the click is in the gold circle, display winning message, moves all circles except gold circle down, and restart round.
    if golddistance < 15: 
        print("yoooo")
        # Play tada sound
        digsound('tada.wav')

        # Displays congratulatory message
        Congrats = Text(Point(240, 280), 'You win!')
        Congrats.setSize(15)
        Congrats.setStyle('bold')

        # Make all circles besides the gold circle fall off the screen
        for i in range(47):
            for circle in circles:
                if circle != goldcirc:
                    update(10 ** 10)
                    circle.move(0, 10)

                    # Undraw circles once passed win to preserve space
                    if circle.getCenter().y > 520:
                        circle.undraw()

                    # Check if exit button is clicked and close program accordingly (cliclose not used to prevent slowing down of program)
                    click = controlwin.checkMouse()
                    if click != None and (165 <= click.x <= 245 and 140 <= click.y <= 190):
                        controlwin.close()
                        ghwin.close()
                        os._exit(0)
        
        # If newgame is clicked, reset game
        if click != None and (5 <= click.x <= 105 and 120 <= click.y <= 190):
            print("wowzers")
            clickcount = 0
            roundn = 0
            player.undraw()
            roundcontinues = False
            print("Reset Game!")
                    
        # Define the previous time
        oldtime = time()

        # Initialize current time
        timepass = time() - oldtime

        # Store a random interval between 5 and 10 as randtime
        randtime = randint(5,10)

        # Initialize circle movement and iterator
        dx,dy = 3,-5
        i = 0

        # Define a while loop to run until 5-10 seconds have passed
        while timepass < randtime:
            # Find amount of time passed
            timepass = time() - oldtime

            # Update frame rate so goldcirc is clickable
            update(60)

            # Undraw goldcirc
            goldcirc.undraw()

            # Find center of goldcirc
            center = goldcirc.getCenter()

            # Check if click is on goldcirc
            gameclick = ghwin.checkMouse()
            if gameclick != None:
                distance = sqrt(((gameclick.x-center.x)**2)+((gameclick.y-center.y)**2))

                # If click is on goldcirc, subtract two from clickcount and play coin sound
                if distance <= goldcirc.getRadius() and clickcount > 1:
                    clickcount -= 2
                    clicks.setText('Clicks: {0}'.format(clickcount))
                    digsound('coin.wav')

            # Redraw goldcirc in new moved location
            goldcirc = Circle(Point(center.x + dx, center.y + dy),15-i)
            goldcirc.setFill('gold')
            goldcirc.draw(ghwin)
            center=goldcirc.getCenter()

            # If border is hit, bounce the goldcirc away
            if center.x not in range(0,480):
                dx *= -1
            if center.y not in range(60,520):
                dy *= -1

            # Make the circle smaller each time loop repeats
            i += .02

            # Check if exit button is clicked and close program accordingly 
            #    (cliclose not used to prevent slowing down of program)
            click = controlwin.checkMouse()
            if click != None and (165 <= click.x <= 245 and 140 <= click.y <= 190):
                controlwin.close()
                ghwin.close()
                os._exit(0)
            
            # Otherwise, if newgame is clicked, reset the game
            elif click != None and (5 <= click.x <= 105 and 120 <= click.y <= 190):
                print("wowzers")
                clickcount = 0
                roundn = 0
                player.undraw()
                roundcontinues = False
                print("Reset Game!")     

            # If circle gets as small as possible in time interval, 
            #    break from loop to prevent it from getting larger
            if 15 - i < 0.1:
                break

        # Undraw the golden circle
        goldcirc.undraw()

        # Displays congratulatory message
        Congrats = Text(Point(240, 280), 'You win!')
        Congrats.setSize(15)
        Congrats.setStyle('bold')
        Congrats.draw(ghwin)

        # Click to start new round
        Continue = Text(Point(240, 300),
                    'Click to continue...')
        Continue.setSize(11)
        Continue.setStyle('italic')
        Continue.draw(ghwin)
        ghwin.getMouse()

        # When click is detected, undraw messages and gold circle in order to prepare for next round
        Congrats.undraw()
        Continue.undraw()

        # Stop current round
        roundcontinues = False

    # Return necessary variables and round stoppage
    return roundcontinues, clickcount, roundn, clicks

###################################################################################################################################################################

# Define the cliclose function
def cliclose(controlwin, ghwin, click):
    # Slow down program to capture clicks better
    sleep(0.03)

    # Check for any clicks on the exitgame control
    click = controlwin.checkMouse()

    # If exit button is clicked, close the program
    if click != None and (165 <= click.x <= 245 and 140 <= click.y <= 190):
        controlwin.close()
        ghwin.close()
        os._exit(0)

###################################################################################################################################################################

# Define the chegclick function
def chegclick(controlwin, ghwin, click, roundn, clickcount, letsago, roundcontinues):
    print("chegclick")

    # Initialize game click
    gameclick = None

    # Define a while loop to check if new game button is clicked and if goldwin is clicked
    while gameclick == None:
        gameclick = ghwin.checkMouse()

        # Call the newgtwist function
        roundn, letsago, roundcontinues, clickcount = newgtwist(click, roundn, letsago, roundcontinues, controlwin, clickcount, ghwin)

        # If new game button is clicked, restart the game
        if roundcontinues == False:
            break
    
    # Return necessary variables to main
    return gameclick, roundn, clickcount, letsago, roundcontinues

###################################################################################################################################################################

# Define the checklick function
def checlick(controlwin, ghwin):
    print("checlick")

    # Initialize click
    click = None

    # Define a while loop to check for click on new game or exit buttons
    while click == None:
        # Wait for a click in controlwin
        click = controlwin.getMouse()

        # If click is in new game button, return the click and start game
        if (5 <= click.x <= 120 and 140 <= click.y <= 190):
            print("Its in")
            letsago = True
            return click, letsago

        # If click is on exit button, close windows and the program        
        elif (180 <= click.x <= 245 and 120 <= click.y <= 190):
            controlwin.close()
            ghwin.close()
            os._exit(0)

        # Otherwise, re-initialize click to repeat loop
        else:
            click = None

###################################################################################################################################################################

# Define the newgtwist function
def newgtwist(click, roundn, letsago, roundcontinues, controlwin, clickcount, ghwin):
    # Slow down program to capture clicks
    sleep(0.03)

    # Check for click in controlwin
    click = controlwin.checkMouse()

    # Call the cliclose function
    cliclose(controlwin, ghwin, click)

    # If there is a click on the new game button, restart game with round and click counter reset
    if click != None:
        if (5 <= click.x <= 105 and 120 <= click.y <= 190):
            print("wowza")
            clickcount = 0
            letsago = True
            roundcontinues = False
            if roundn > 0:
                roundn = 0
            print("Reset Game!")

    # Return necessary variables to main
    return roundn, letsago, roundcontinues, clickcount

###################################################################################################################################################################

# Define the digsound() function
def digsound(track):
    # Play chosen track with compatibility for each operating system
    if platform.system() == 'Windows':
        winsound.PlaySound(track, winsound.SND_ASYNC)
    if platform.system == 'Linux':
        os.system('aplay ' + track + '&')
    if platform.system == 'Darwin':
        os.system('afplay ' + track + '&')

###################################################################################################################################################################

# Define the main() function
def main():
    # Call GoldHunt and GameControl functions and assign appropriate variables
    ghwin, rounds, clicks = GoldHunt()
    playername, controlwin = GameControl()

    # Intialize variables for while loops and round counts
    playing = True
    click = None
    roundn = 0
    clickcount = 0

    # Play background music while user enters name
    digsound('WiiMusic.wav')

    # Initialize variable to count number of loop iterations
    realit = 0
    
    # While loop to continue gameplay
    while playing:
        # Call the checlick function if playing loop is in first iteration
        #    in order to initiate gameplay
        if realit == 0:
            click, letsago = checlick(controlwin, ghwin)
        
        # Increase loop variable iteration by one to avoid calling checlick
        realit += 1
        
        # Get the users name from entry box
        name = playername.getText()
        
        # If name equals nothing, do not start game
        if name == '':
            print(name)
            realit = 0
            letsago = False

        # Update frames to smoothen gameplay
        update(60)

        # If the player has entered their name and clicks new game, 
        #    a grid of circles appears and gameplay begins
        if letsago == True and name != '' or roundn >= 1:
            print("newgame")
            # When round begins, add one to the round count
            roundn += 1

            # Show the round count to user
            rounds.setText('Rounds: {0}'.format(roundn))
            
            # Call the MakeCircles() function to get a new circle set each round
            circles, colors, player, randrednum, randnum = MakeCircles(name, ghwin)

            # Find which circle is the gold circle
            circnum = colors.index('gold')
            goldcirc = circles[circnum]

            # While loop for each individual round that counts clicks, sets circle fill, 
            #    and tells user when they have found the gold circle
            roundcontinues = True
            while roundcontinues:
                print("round continues")
            
                # Check for mouse click in control window here so exit or new game can be clicked whenever
                cliclose(controlwin, ghwin, click)

                # Call the chegclick function
                gameclick, roundn, clickcount, letsago, roundcontinues = chegclick(controlwin, ghwin, click, roundn, clickcount, letsago, roundcontinues)

                # Call the cliclose function
                cliclose(controlwin, ghwin, click)
                
                # If q is pressed, activate cheats by outlining where border of goldcirc and redcirc is
                key = controlwin.checkKey()
                print(key)
                if key == 'q':
                    goldcirc.setOutline('gold')
                    circles[randrednum].setOutline('red')    
                      
                # Get player name from entry box
                name = playername.getText()

                # If entry box is not empty and new game button is pressed, 
                #    reset the board and get out of loop
                if roundcontinues == False and name != '':
                    print("break")
                    print(name)
                    for circle in circles:
                            update(90)
                            circle.undraw()
                    player.setText('')
                    rounds.setText('Rounds: {0}'.format(roundn))
                    clicks.setText('Clicks: {0}'.format(clickcount))
                    break

                # Initialize variable to check if click is in controlwin
                cloak = True

                # Define a while loop to pause program until a name is entered into controlwin
                while name == '':
                    # Update frames to smoothen game
                    update(60)

                    # Set name value to blank
                    player.setText('')

                    # Get player name
                    name = playername.getText()

                    # Repeat the round
                    roundcontinues = True

                    # Call the cliclose function
                    cliclose(controlwin, ghwin, click)

                    # Check for click on goldwin
                    cloak = ghwin.checkMouse

                    # If there is a click on goldwin while name is empty, ignore it 
                    if cloak != None:
                        cloak = None

                # If there is a name in controlwin entry box, continue gameplay
                if cloak != None:

                    # Fill the clicked circles with the assigned color if it has been clicked
                    for j in range(225):
                        center = circles[j].getCenter()
                        distance = sqrt(((gameclick.x - center.x)**2) + ((gameclick.y - center.y)**2))
                        goldcenter = goldcirc.getCenter()
                        golddistance = sqrt(((gameclick.x - goldcenter.x)**2) + ((gameclick.y - goldcenter.y)**2))
        
                        # If the click is detected on within the circle(in radius), fill it with assigned color
                        #    Add one to click counter when the circle is clicked and color is revealed
                        #    If a red circle is clicked, add 5 to current click count
                        #    Update click count only if circle was not previously revealed
                        if distance < 15 and circles[j].config["fill"] == "black":
                            print(abs(distance - golddistance))
                            if abs(distance - golddistance) < 86:
                                circles[j].setFill(colors[j])
                                clickcount += 1
                                digsound('digclick.wav')
                            elif j == randrednum:
                                print('hey')
                                circles[j].setFill('red')
                                clickcount += 5
                                digsound('trombone.wav')
                            else:
                                circles[j].setFill("white")
                                clickcount += 1
                                if circles[j].config["fill"] != "red":
                                    digsound('digclick.wav')
                                    
                            # Update the click count text
                            clicks.setText('Clicks: {0}'.format(clickcount))
                            
                            # Call the goldmess function
                            roundcontinues, clickcount, roundn, clicks = goldmess(golddistance, controlwin, ghwin, circles, goldcirc, roundcontinues, click, clickcount, player, roundn, clicks)
                            
            # Get out of playing loop to stop game after 5th round
            if roundn == 5:
                # Open the file to read its data
                scorefile = open('scores.txt', 'r')
                # Save the file as a list
                scoredata = scorefile.readlines()

                # Close the file
                scorefile.close()
                
                # Create an updated version without extra characters
                NameScoreL = []
                # Append the recently made score in the correct format
                NameScoreL.append([name, clickcount])
                # If the data from the scores file is not empty retrive it, reformat it and append it into the formatted list of names and scores.
                if scoredata != []:
                    for item in scoredata:
                        NameScoreL.append(item.rstrip('\n').replace(' ', '').split(','))
                    for item in NameScoreL:
                        item[1] = int(item[1])
                        
                    # Sort the list according to the score (second item in each list)
                    NameScoreL = sorted(NameScoreL, key=lambda x: x[1])

                    # Open the file again in order to manipulate it
                    scorefile = open('scores.txt', 'w')
                    
                    # Write this updated list to the file
                    for item in NameScoreL:
                        scorefile.write(('{0}, {1}\n').format(item[0], item[1]))
                    scorefile.close()

                # If the scores file is empty then just write the newly made score to it.
                elif scoredata == []:
                    # Open the file again in order to manipulate it
                    scorefile = open('scores.txt', 'w')
                    # Write the new name and score into file
                    scorefile.write(('{0}, {1}\n').format(name, clickcount))
                    # Close the file
                    scorefile.close()
                
                # Update the top 3 display and give user a chance to exit game for good or start new
                controlwin.close()
                ghwin.close()
                # Call functions and assign appropriate variables
                ghwin, rounds, clicks = GoldHunt()
                playername, NEWGAME, EXIT, controlwin = GameControl()
                
    # Close all windows to stop program and stop background music
    ghwin.close()
    controlwin.close()

    # Play sound at end of the game
    digsound('endgame.wav')
    sleep(2.5)
main()
