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

####################################################################################################################################################################

# Game control window
def GameControl():

    # Create window
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
    name = Text(Point(125,50), 'PLAYER NAME')
    name.setSize(11)
    name.draw(win)
    inputbox = Entry(Point(125,80), 11)
    inputbox.setFill('white')
    inputbox.draw(win)

    # Create and display New Game button
    newgamerect = Rectangle(Point(5, 120), Point(105, 190))
    newgamerect.setFill('gold')
    newgamerect.draw(win)
    newgamelabel = Text(Point(55,155), 'NEW GAME')
    newgamelabel.setStyle('bold')
    newgamelabel.draw(win)

    # Create and display Exit button
    exitrect = Rectangle(Point(180, 120), Point(245,190))
    exitrect.setFill('black')
    exitlabel = Text(Point(212.5, 155), 'EXIT')
    exitlabel.setFill('lightgray')
    exitlabel.setStyle('bold')
    exitrect.draw(win)
    exitlabel.draw(win)

    # Return the player's name, new game, exit, and the graphics window
    return  inputbox, newgamerect, exitrect, win

####################################################################################################################################################################

# Define the goldhunt() funtion
def GoldHunt():

    # Create the window
    win = GraphWin('GoldHunt', 480, 520)#, autoflush=False)

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

        # Wait for click in appropriate parameter
        click = controlwin.checkMouse()
        
        # Exit the game/while loop if the click is detected on the exit control
        if click != None and 180 <= click.x <= 245 and 120 <= click.y <= 190:
            playing = False

        # If the player has entered their name and clicks new game, a grid of circles should appear
        elif click != None and name != '' and (5 <= click.x <= 105 and 120 <= click.y <= 190):

            # Intiate a counter for the amount of clicks
            clickcount = 0
            
            # 5 rounds, if user clicks circle, set fill to assigned colors
            #for i in range(5):
            i = 0
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
                goldcirc = circles[circnum]
                    
                # While loop for each individual round that counts clicks, sets circle fill, and tells user when they have found the gold circle
                roundcontinues = True
                while roundcontinues:

                    # Check for mouse click in either goldhunt window or the control window here so exit or new game can be clicked or game can continue.
                    gameclick = None
                    click = None
                    name = playername.getText()
                    while gameclick == None and click == None:
                        gameclick = ghwin.checkMouse()
                        click = controlwin.checkMouse()

                    # If EXIT button was clicked set playing to False and break out of while loop for round
                    if click != None and (180 <= click.x <= 245 and 120 <= click.y <= 190):
                        playing = False
                        break
                    
                    # If new game button was clicked then break loop and reset counters and name
                    elif click != None and (5 <= click.x <= 105 and 120 <= click.y <= 190):
                        roundcontinues = False
                        name = playername.getText()
                        playertxt.undraw()
                        rounds.setText('Rounds: 1')
                        clicks.setText('Clicks: 0')
                        i = 0
                        clickcount = 0
                        break
                        
                    # Get the click so that the program can check which circle the mouse has clicked in 
                
                    # Fill the clicked circles with the assigned color if it has been clicked
                    for j in range(225):
                        center = circles[j].getCenter()
                        distance = sqrt(((gameclick.x - center.x)**2) + ((gameclick.y - center.y)**2))
                        goldcenter = goldcirc.getCenter()
                        golddistance = sqrt(((gameclick.x - goldcenter.x)**2) + ((gameclick.y - goldcenter.y)**2))
    
                        # If the click is detected on within the circle(in rsdius), fill it with assigned color
                        if distance < 15:
                            circles[j].setFill(colors[j])
                            # Add one to click counter when the circle is clicked and color is revealed
                            clickcount += 1
                            clicks.setText('Clicks: {0}'.format(clickcount))
                            
                    # If the click is in the gold circle, display winning message, moves all circles except gold circle down, and restart round.
                    if golddistance < 15:  
                        
                        # Make all circles besides the gold circle fall off the screen
                        for k in range(47):
                            for circle in circles:
                                if circle != goldcirc:
                                    circle.move(0, 10)
                                    update(5000)
                                    
                        # Undraw the circles once they are off the screen
                        for circle in circles:
                            circle.undraw()

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
                        ghwin.getMouse()

                        # When click is detected, undraw messages and gold circle in order to prepare for next round
                        Congrats.undraw()
                        Continue.undraw()
                        goldcirc.undraw()
                        roundcontinues = False
                        i += 1
                        
            # ONly after all 5 rounds have been completed, add the player's name and number of clicks to the scores file with scores in the correct order
            if i == 4:
                # Open the file to read its data
                scorefile = open('scores.txt', 'r')
                # Save the file as a list
                scoredata = scorefile.readlines()

                # Close the file
                scorefile.close()
                
                # Create an updated version without extra characters
                cleandata = []
                # Append the reently made score
                cleandata.append(('{0}, {1}\n').format(name, clickcount))
                if scoredata != []:
                    for line in scoredata:
                        cleandata.append(line.rstrip('\n').replace(' ', '').split(','))

                    # Make a list of sorted scores
                    scores = [int(item[1]) for item in cleandata]
                    # Make a temporary list of these scores but sorted in ascending order
                    temp = [int(item[1]) for item in cleandata]
                    temp.sort()

                    # Make a list with the new data with name and score in order ascending order
                    updatedscores = []
                    # for loop to loop through scores 
                    for i in range(len(scores)):
                        # The best score is always the first one in the list
                        bestscore = temp[0]
                        # find the location of this score in the unsorted list whose indexes correspond with their item in newdata
                        location = scores.index(bestscore)
                        # Add this new best score tot he updated list
                        updatedscores.append(cleandata[location])
                        # Remove the first character(the lowest score) in the list so that the next round can find the next lowest
                        temp = temp[1:]

                    # Open the file again in order to manipulate it
                    scorefile = open('test.txt', 'w')
                    
                    # Write this updated list to the file
                    for item in updatedscores:
                        scorefile.write(('{0}, {1}\n').format(item[0], item[1]))
                    scorefile.close()

            elif cleandata == []:
                # Open the file again in order to manipulate it
                scorefile = open('test.txt', 'w')
                # Write this updated list to the file
                for item in updatedscores:
                    scorefile.write(('{0}, {1}\n').format(name, clickcount))
                scorefile.close()

    # Close windows when large loop is broken
    ghwin.close()
    controlwin.close()

# Call the  main() function
main()
