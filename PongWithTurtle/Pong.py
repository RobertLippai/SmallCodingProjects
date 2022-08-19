"""

    Based of a FreeCodeBootcamp Tutorial

    I have added / implemeneted the following things:
        * Platform indepentent audio playing
            (Checks the current platform and uses the corresponding audio library)

        * Fixed the game speed changing depending the computer's computation performance
            (Logic is separated into a method that gets called every 15 milliseconds)
        
        * The ball gets progressibly faster if someone scores a point

        * The paddles now use an Object Orianted structure

        * Code is separeted into smaller functions

    
    The game was tested and development using Python 3.10.

    Later I plan to add:
        * Single Player function with a CPU enemy player

        * A title screen

        * Restarting option

"""


import turtle
import platform

try:
    import winsound
except ImportError:
    import os


# Classes and Functions

class Paddle(object):
    """
    
        Creates a controllable paddle object.
        Currenty there are a two methods to move it in a vertical direction.

        Later a CPU Enemy could be added to support singleplayer rounds.
    
    """

    def __init__(self):
        self.entity = turtle.Turtle()
        self.entity.speed(0) # GUI drawing speed, 0 is instant
        self.entity._moveStep = 20 # move the paddle n pixels
        self.entity.shape("square")
        self.entity.color("white")
        self.entity.shapesize(stretch_wid=5, stretch_len=1)
        self.entity.penup()
        

    def move_up(self):
        y = self.entity.ycor()
        y += self.entity._moveStep

        self.entity.sety(y)

    def move_down(self):
        y = self.entity.ycor()
        y -= self.entity._moveStep

        self.entity.sety(y)

def playSound():
    """
        Plays a sound using the current platform's bulit-in audio player

        aplay == linux
        afplay == mac
        winsound == windows

    """

    _fileName = "bounce.wav"

    if platform.system() == "Darwin":
        os.system("afplay {0}&".format(_fileName))

    if platform.system() == "Linux":
        os.system("aplay {0}&".format(_fileName))

    if platform.system() == "Windows":
        winsound.PlaySound("{0}".format(_fileName), winsound.SND_ASYNC)

def updateDifficulty():
    global maxDifficulty

    # Setting a maximum delta value

    if(abs(ball.dx) < maxDifficulty):
        ball.dx = ball.dx * 1.25
        ball.dy = ball.dy * 1.25


def checkCollision():
    global playerAScore, playerBScore

    # Border checking
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        playSound()

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        playSound()

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        playerAScore += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(playerAScore, playerBScore), align="center", font=("Courier", 24, "normal"))
        updateDifficulty()
        playSound()

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        playerBScore += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(playerAScore, playerBScore), align="center", font=("Courier", 24, "normal"))
        updateDifficulty()
        playSound()

    # Paddle and ball collisions
    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.entity.ycor() + 40 and ball.ycor() > paddle_b.entity.ycor() - 40):
       ball.setx(340)
       ball.dx *= -1
       playSound()

    if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.entity.ycor() + 40 and ball.ycor() > paddle_a.entity.ycor() - 40):
       ball.setx(-340)
       ball.dx *= -1
       playSound()

def moveBall():
    # Moves the ball with the given delta values

    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

def logic():
    moveBall()

    checkCollision()

# Game Setup

wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor("black")
wn.setup(width=800, height=600) 
wn.tracer(0) # stops the window from auto-updating

# Creating the paddles

paddle_a = Paddle()
paddle_a.entity.goto(-350, 0)

paddle_b = Paddle()
paddle_b.entity.goto(350, 0)


# Crearing the Ball

ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)

# Delta change values
ball.dx = 4
ball.dy = 4

maxDifficulty = 8

# Score Writing
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

playerAScore = 0
playerBScore = 0


# Keyboard bindings

# Listens for keyboard input
wn.listen()

# Player A

wn.onkeypress(paddle_a.move_up, "w")
wn.onkeypress(paddle_a.move_down, "s")

# Player B

wn.onkeypress(paddle_b.move_up, "Up")
wn.onkeypress(paddle_b.move_down, "Down")


# Main game loop

while True:
    wn.update()
    turtle.ontimer(logic, 15)