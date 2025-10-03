from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

#create a class called PongPaddle to represent the game's paddles
class PongPaddle(Widget):
    score = NumericProperty(0) #a score attribute is attached to each paddle, and it starts at 0

    #method for using the paddle to manage ball collisions
    def bounce_ball(self,ball):
        if self.collide_widget(ball): #verify if the ball and paddle make collision
            ball.velocity_x *= -1.1 #reverse the ball and accelerate it a little bit

#create the PongBall class to serve as the game's ball
class PongBall(Widget):
    #properties for storing the ball's velocity on the x and y axes
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    #merge the velocities of x and y
    velocity = ReferenceListProperty(velocity_x,velocity_y)

    #method for updating the ball's position according to its velocity
    def movement(self):
        #latest position = current velocity + current position
        self.pos = Vector(*self.velocity) + self.pos

#create the PongGame class to regulate the game logic
class PongGame(Widget):
    #reference to the game's ball and player paddles
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    #method for serving the ball in an unexpected angle
    def serve_ball(self):
        self.ball.velocity = Vector(6, 0).rotate(randint(0, 360))

    #method for updating the current status of the game
    def update(self, dt):
        self.ball.movement()

        #set the ball to bounce off the top and bottom
        if (self.ball.y < 0) or (self.ball.y > self.height -50):
            self.ball.velocity_y *= -1

        #verify whether the ball touches the left boundary line
        if self.ball.x < 0:
            self.ball.velocity_x *= -1 #reverse the direction of the ball
            self.player1.score +=1 #increase player 1's total score

        # verify whether the ball touches the right boundary line
        if self.ball.x > self.width -50:
            self.ball.velocity_x *= -1 #reverse the direction of the ball
            self.player2.score += 1 #increase player 2's total score

        #use the paddles to manage ball collisions
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

    #method for managing touch input to move the paddles
    def on_touch_move(self, touch): #on_touch_move() - when players drug their finger on the screen
        #if the touch is on the left side of the screen, move the paddle of player 1
        if touch.x < self.width / 1/4:
            self.player1.center_y = touch.y

        #if the touch is on the right side of the screen, move the paddle of player 2
        if touch.x > self.width / 3/4:
            self.player2.center_y = touch.y

#create the PongApp class to execute the program
class PongApp(App):
    def build(self):
        game = PongGame() #create a PongGame object (instance)
        game.serve_ball() #to begin the game, serve the ball
        Clock.schedule_interval(game.update,1.0/60.0) #schedule the update method to execute 60 times in a second
        return game

#run the Pong Game
PongApp().run()