#
# CS 177 - project2.py
# Emelie Coleman, 0031104038
# Following Coding Standards and Guidelines
# This program creates a control window and a game window. The control window is used to get a payer's
#   name, start a game, or exit a game. The program has a game window where the players name will appear
#   what round they're on, and how many clicks have happened. Also in this window, a 15x15 grid of black
#   circles will appear and when clicked they change colors to their 'hidden' color. When the user finds
#   the gold circle that marks the end of the round, a message is displayed and the user may continue.
#   When the game ends, the players name and score is written to a file called 'scores.txt.'
#

# Import necessary libraries
from graphics import *
from random import randint
from math import sqrt
from time import *
import winsound

####################################################################################################################################################################

# Game control window
def GameControl():

    # Create window
    win = GraphWin('Game Control', 250, 200)

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
    name = Text(Point(75,50), 'PLAYER NAME')
    name.setSize(9)
    name.setStyle('bold')
    name.draw(win)
    inputbox = Entry(Point(175,50), 8)
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
    newgamelabel = Text(Point(55,172.5), 'NEW GAME')
    newgamelabel.setStyle('bold')
    newgamelabel.setSize(10)
    newgamelabel.draw(win)

    # Create and display Exit button
    exitrect = Rectangle(Point(180, 155), Point(245,190))
    exitrect.setFill('black')
    exitlabel = Text(Point(212.5, 172.5), 'EXIT')
    exitlabel.setFill('lightgray')
    exitlabel.setStyle('bold')
    exitlabel.setSize(10)
    exitrect.draw(win)
    exitlabel.draw(win)

    # Return the player's name, new game, exit, and the graphics window
    return  inputbox, newgamerect, exitrect, win

####################################################################################################################################################################

# Define the goldhunt() funtion
def GoldHunt():

    # Create the window
    win = GraphWin('GoldHunt', 480, 520)

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


    # Return the round and clicks
    return win, rounds, clicks
    
####################################################################################################################################################################

# Define the circles() function
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
            circles.append(circle)

    # Draw these circles in the game window
    for circle in circles:
        circle.draw(win)

    # Make the list of appropriate colors for the circle based on where the gold circle is
    # Random number for gold circle
    randnum = randint(0,224)
    # Assign a number for the red circle
    red = randint(0,224)
    while red == randnum:
        red = randint(0,224)

    #   Start with a list of the color white for each circle
    colors = ['white' for i in range(225)]

    #   Whatever index the gold circle is then assign gold, gray, and tan to appropriate circles
    for i in range(225):
        if i == red:
            colors[i] = 'red'
        if i == randnum:
            colors[i] = 'gold'
        if i in [randnum-1, randnum+1, randnum+16, randnum+15, randnum+14, randnum-16, randnum-15, randnum-14]:
            colors[i] = 'tan'
        if i in [randnum-32, randnum-31, randnum-30, randnum-29, randnum-28, randnum+28, randnum+29, randnum+30, randnum+31, randnum+32, randnum-2, randnum+2, randnum-17,  randnum-13, randnum+17, randnum+13, randnum-13]:
            colors[i] = 'gray'
    
    # Return list of circles and color assignments
    return player, circles, colors

###################################################################################################################################################################

# Define the main() function
def main():
    
    # Call funtions and assign appropriate variables
    ghwin, rounds, clicks = GoldHunt()
    playername, NEWGAME, EXIT, controlwin = GameControl()

    # Intialize variables for while loops
    playing = True
    roundcontinues = True
    
    # While loop to continue gameplay
    while playing:

        # Get the users name from entry box
        name = playername.getText()

        # Initiate round counter/while loop parameter
        i = 0

        # Wait for click in appropriate parameter
        click = controlwin.checkMouse()
        
        # Exit the game/while loop if the click is detected on the exit control
        if click != None and 180 <= click.x <= 245 and 155 <= click.y <= 190:
            playing = False

        # If the player has entered their name and clicks new game, a grid of circles should appear
        elif click != None and name != '' and (5 <= click.x <= 105 and 155 <= click.y <= 190):

            # Start background music
            wii = winsound.PlaySound('WiiMusic.wav', winsound.SND_ASYNC)

            # Intiate a counter for the amount of clicks
            clickcount = 0
            
            # 5 rounds, if user clicks circle, set fill to assigned colors
            #for i in range(5):
            while i < 5:

                # If EXIT control is clicked break the for loop to close windows and end program
                if playing == False:
                    break

                # When round begins, add one to the round count
                rounds.setText('Rounds: {0}'.format(i+1))

                # Call the MakeCircles() function to get a new gold circle each round
                playertxt, circles, colors = MakeCircles(name, ghwin)

                # Find which circle is the gold circle
                circnum = colors.index('gold')
                redcircnum = colors.index('red')
                goldcirc = circles[circnum]
                redcirc = circles[redcircnum] 
                    
                # While loop for each individual round that counts clicks, sets circle fill, and tells user when they have found the gold circle
                roundcontinues = True
                while roundcontinues:

                    # If q is pressed, activate cheats by outlining where border of goldcirc and redcirc is
                    key = controlwin.checkKey()
                    if key == 'q':
                        goldcirc.setOutline('gold')
                        redcirc.setOutline('red')
                        
                    # Check for mouse click in either goldhunt window or the control window here so exit or new game can be clicked or game can continue.
                    gameclick = None
                    click = None
                    name = playername.getText()
                    while gameclick == None and click == None:
                        gameclick = ghwin.checkMouse()
                        click = controlwin.checkMouse()

                    # If EXIT button was clicked set playing to False and break out of while loop for round
                    if click != None and (180 <= click.x <= 245 and 155 <= click.y <= 190):
                        playing = False
                        break
                    
                    # If new game button was clicked then break loop and reset counters and name
                    elif click != None and (5 <= click.x <= 105 and 155 <= click.y <= 190):
                        roundcontinues = False
                        # Undraw old circles and player text
                        for circle in circles:
                            circle.undraw()
                        playertxt.undraw()
                        # Reset counters
                        rounds.setText('Rounds: 1')
                        clicks.setText('Clicks: 0')
                        i = 1
                        clickcount = 0
                        # Restart background music
                        winsound.PlaySound(None, winsound.SND_ASYNC)
                        winsound.PlaySound('WiiMusic.wav', winsound.SND_ASYNC)
                        break
                
                    # Fill the clicked circles with the assigned color if it has been clicked
                    # Find which circle the click was detected in
                    for j in range(225):
                        # Get the center and calculate the distance
                        center = circles[j].getCenter()
                        distance = sqrt(((gameclick.x - center.x)**2) + ((gameclick.y - center.y)**2))
                        goldcenter = goldcirc.getCenter()
                        golddistance = sqrt(((gameclick.x - goldcenter.x)**2) + ((gameclick.y - goldcenter.y)**2))
                        
                        # If the click is detected on within the circle(in radius), fill it with assigned color
                        if distance <= 15 and circles[j].config['fill'] == 'black':
                            circles[j].setFill(colors[j])
                            # If the color of the circle click is red, add 5 to the clickcount
                            if colors[j] == 'red':
                                winsound.PlaySound('trombone.wav', winsound.SND_ASYNC)
                                clickcount += 5
                            # Add one to click counter when the circle is clicked and color is revealed
                            else:
                                winsound.PlaySound('digclick.wav', winsound.SND_ASYNC)
                                clickcount += 1
                            # Update the clicks
                            clicks.setText('Clicks: {0}'.format(clickcount))
                        
                    # If the click is in the gold circle, display winning message, moves all circles except gold circle down, and restart round.
                    if golddistance <= 15:

                        # Play sound effect for finding the gold circle
                        winsound.PlaySound('tada.wav', winsound.SND_ASYNC)
                        
                        # Make all circles besides the gold circle fall off the screen
                        for k in range(32):
                            # Check for mouseclick in case user wants to change action during animation
                            click = controlwin.checkMouse()
                            # If any controls were clicked then break
                            if playing == False or roundcontinues == False:
                                break
                            for circle in circles:
                                # Check for mouseclick in case user wants to change action during animation
                                click = controlwin.checkMouse()
                                # If circle is not the gold circle then move it
                                if circle != goldcirc:
                                    circle.move(0, 40)
                                    #sleep(.00001**10)
                                # If EXIT button was clicked set playing to False and break out of animation loops
                                if click != None and (180 <= click.x <= 245 and 155 <= click.y <= 190):
                                    playing = False
                                    break
                                # If new game button was clicked then break animation loops and reset counters and name
                                elif click != None and (5 <= click.x <= 105 and 155 <= click.y <= 190):
                                    roundcontinues = False
                                    # Undraw old circles and player text
                                    for circle in circles:
                                        circle.undraw()
                                    playertxt.undraw()
                                    # Reset counters
                                    rounds.setText('Rounds: 1')
                                    clicks.setText('Clicks: 0')
                                    i = 0
                                    clickcount = 0
                                    # Restart background music
                                    winsound.PlaySound(None, winsound.SND_ASYNC)
                                    winsound.PlaySound('WiiMusic.wav', winsound.SND_ASYNC)
                                    break
                                
                        # If exit or new game buttons were clicked during animation, then break
                        if playing == False or roundcontinues == False:
                                break
                                    
                        # Undraw the circles once they are off the screen
                        for circle in circles:
                            circle.undraw()

                        # After other circles leave the window, activate the Golden Pete Minigame
                        # Initiate variables
                        dx,dy = 3,-5
                        k = 0
                        # Find the current time
                        thetime = time()
                        timepassed = time() - thetime

                        # Initiate while loop that ends when the time passed is 5 seconds
                        while timepassed < 5:

                            # Undraw old circle
                            goldcirc.undraw()
                            # Find the center of the old circle
                            center = goldcirc.getCenter()
                            # Check if the user clicked in that circle or on control buttons
                            gameclick = ghwin.checkMouse()
                            click = controlwin.checkMouse()
                            # If the window has been clicked find the distance from the radius the click should be in
                            if gameclick != None:
                                # Distance formula from click point to the center of the circle
                                distance = sqrt(((gameclick.x - center.x)**2) + ((gameclick.y - center.y)**2))
                                # If the click is within the radius of the circle, reward the user
                                if distance <= goldcirc.getRadius() and clickcount > 0:
                                    winsound.PlaySound('coin.wav', winsound.SND_ASYNC)
                                    # Subtract 2 clicks for everytime the user clicks on Pete
                                    clickcount -= 2
                                    # Update the score
                                    clicks.setText('Clicks: {0}'.format(clickcount))
                                    
                            # If EXIT button was clicked set playing to False and break out of mini game
                            elif click != None and (180 <= click.x <= 245 and 155 <= click.y <= 190):
                                playing = False
                                break
                            
                            # If new game button was clicked then break out of mini game loop and reset counters and name
                            elif click != None and (5 <= click.x <= 105 and 155 <= click.y <= 190):
                                roundcontinues = False
                                # Undraw old circles and player text
                                for circle in circles:
                                    circle.undraw()
                                playertxt.undraw()
                                # Reset counters
                                rounds.setText('Rounds: 1')
                                clicks.setText('Clicks: 0')
                                i = 1
                                clickcount = 0
                                # Restart background music
                                winsound.PlaySound(None, winsound.SND_ASYNC)
                                winsound.PlaySound('WiiMusic.wav', winsound.SND_ASYNC)
                                break
                            # Draw a new gold circle with a decreased radius
                            goldcirc = Circle(Point(center.x + dx, center.y + dy),15-k)
                            goldcirc.setFill('gold')
                            goldcirc.draw(ghwin)
                            # Make the circle move soothly
                            sleep(0.03)
                            # Find the center of the new circle
                            goldcenter = goldcirc.getCenter()
                            # Change direction if the new circle hits a boundry of the window
                            if goldcenter.x not in range(0, 480):
                                dx *= -1
                            if goldcenter.y not in range(47, 520):
                                dy *= -1
                            # Find the time passed since the game started
                            timepassed = time() - thetime
                            # Increase the number tht the circles radius will decrease by
                            k+=.07
                            
                        # If exit or new game buttons were clicked during mini game then break
                        if playing == False or roundcontinues == False:
                                break
                    
                        # Displays congratulatory message
                        Congrats = Text(Point(240, 280), 'You win!')
                        Congrats.setSize(15)
                        Congrats.setStyle('bold')
                        Congrats.draw(ghwin)

                        # Click to start new round
                        Continue = Text(Point(240, 300), 'Click to continue...')
                        Continue.setSize(11)
                        Continue.setStyle('italic')
                        Continue.draw(ghwin)
                        # Pause for a click in order to continue
                        ghwin.getMouse()

                        # When click is detected, undraw messages and gold circle in order to prepare for next round
                        Congrats.undraw()
                        Continue.undraw()
                        goldcirc.undraw()
                        roundcontinues = False
                        i += 1
                        
            # Only after all 5 rounds have been completed, add the player's name and number of clicks to the scores file with scores in the correct order
            if i == 5:
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
                # Restart background music
                winsound.PlaySound(None, winsound.SND_ASYNC)
                winsound.PlaySound('WiiMusic.wav', winsound.SND_ASYNC)

    # Close windows when large loop is broken
    # Stop playing background music
    winsound.PlaySound(None, winsound.SND_ASYNC)
    winsound.PlaySound('endgame.wav', winsound.SND_ASYNC)
    ghwin.close()
    controlwin.close()

# Call the  main() function
main()
