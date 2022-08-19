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

"""


import turtle
import platform

try:
    import winsound
except ImportError:
    import os



class Paddle(object):
    def __init__(self):
        self.entity = turtle.Turtle()
        self.entity.speed(0) # 0 is the max speed
        self.entity.shape("square")
        self.entity.color("white")
        self.entity.shapesize(stretch_wid=5, stretch_len=1)
        self.entity.penup()

    def move_up(self):
        y = self.entity.ycor()
        y += 20

        self.entity.sety(y)

    def move_down(self):
        y = self.entity.ycor()
        y -= 20

        self.entity.sety(y)

# Setup

wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor("black")
wn.setup(width=800, height=600) 
wn.tracer(0) # stops the window from updating

paddle_a = Paddle()
paddle_a.entity.goto(-350, 0)

paddle_b = Paddle()
paddle_b.entity.goto(350, 0)


# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)

ball.dx = 4 # delta == change
ball.dy = 4

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


# Keyboard binding

# listens for keyboard input
wn.listen()
wn.onkeypress(paddle_a.move_up, "w")
wn.onkeypress(paddle_a.move_down, "s")



def playSound():
    """

        aplay == linux
        afplay == mac
        winsound == windows

    """

    if platform.system() == "Darwin":
        os.system("afplay bounce.wav&")
    if platform.system() == "Linux":
        os.system("aplay bounce.wav&")
    if platform.system() == "Windows":
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

def updateDifficulty():
    if(abs(ball.dx) < 8):
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
        #ball.setx(390)
        ball.goto(0, 0)
        ball.dx *= -1
        playerAScore += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(playerAScore, playerBScore), align="center", font=("Courier", 24, "normal"))
        updateDifficulty()
        playSound()

    if ball.xcor() < -390:
        #ball.setx(-390)
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
    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)


def doAI():
    difficulty = 25
    print("Called")
    #print(str(ball.xcor()) + " " + str(ball.ycor()))

    # ball is moving to the AI
    if(ball.xcor() > 0):
        print("it's comming")
        if( (ball.ycor() > paddle_b.entity.ycor()+difficulty) or (ball.ycor() > paddle_b.entity.ycor()-difficulty) ):
            y = paddle_b.entity.ycor()
            y += 5

            paddle_b.entity.sety(y)
        else:
            y = paddle_b.entity.ycor()
            y -= 5

            paddle_b.entity.sety(y)
    else:
        print("oh fine")
    
    
# Main game loop

def logic():
    global playerAScore, playerBScore

    moveBall()

    checkCollision()

    doAI()


while True:
    wn.update()
    turtle.ontimer(logic, 15)
