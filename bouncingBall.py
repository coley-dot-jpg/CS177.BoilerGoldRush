from graphics import *
from time import sleep


def main():
    win = GraphWin("Win",300,300)
    ball = Circle(Point(150,150),15)
    ball.setFill('gold')
    ball.draw(win)
    dx,dy = 3,-5
    i = 0
    while not win.checkMouse():
        ball.undraw()
        center = ball.getCenter()
        ball = Circle(Point(center.x + dx, center.y + dy),15-i)
        ball.setFill('gold')
        ball.draw(win)
        sleep(0.03)
        center=ball.getCenter()
        if center.x not in range(8,293):
            dx *= -1
        if center.y not in range(8,293):
            dy *= -1
        i+=.05
        if ball.getRadius() <= 0:
            break
    
    win.getMouse()
    win.close()

main()
