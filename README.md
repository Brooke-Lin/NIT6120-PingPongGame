# **Pong Game**


## Introduction
In this file, I will be using Kivy to develop a pong game. I will also explain the classes and methods in each step.


### 1. Building Kivy Framework


#### Description:
The PongGame class, currently devoid of content, houses the game's logic and user interface. It is derived from Widget. And the build method, which produces an instance of PongGame as the application's root widget, is overridden by the PongApp class, which derives from App. To run the code, use PongApp(). run(), which launches the PongGame gadget and initiates the Kivy event loop.


main.py:
```
from kivy.app import App
from kivy.uix.widget import Widget

class PongGame(Widget):
    pass
    
class PongApp(App):
    def build(self):
        return PingPongGame()
        
PongApp().run()
```


output:

![](/Users/brooke/Desktop/1.png)


### 2. Adding the Pong Ball


#### Description:
The PongBall class, which inherits from Widget, is defined by this code to represent the ball in a game of pong. The ball's velocity along the x and y axis is stored in two different properties of this class, velocity_x and velocity_y, which are both instances of NumericProperty. In order to enable simultaneous access and updating of these two properties as a single vector, they are merged into a ReferenceListProperty named velocity. By adding the current velocity (as a Vector) to the ball's current position, the movement method modifies the ball's position and allows it to be moved on the screen.


main.py:
```
from kivy.properties import NumericProperty,ReferenceListProperty
from kivy.vector import Vector

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x,velocity_y)

    def movement(self):
        self.pos = Vector(*self.velocity) + self.pos
```


output:

![](/Users/brooke/Desktop/3.png)


### 3. Setting the Ball Animation and Bouncing


#### Description:
The ball, which is the game's ball widget, is specified as an ObjectProperty. In terms of the serve_ball() method, it uses a vector rotated by a random angle to set the ball's velocity in an unspecified direction. Moreover, the ball will move, and its motion will reverse when it collides with the top, bottom, left, or right limits of the screen. This is done by calling the update() function 60 times per second. Using Kivy's Clock element, the PongApp class creates and launches the game and uses it to schedule the update() function to run continually.


main.py:
```
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty
from kivy.clock import Clock
from random import randint

class PongGame(Widget):
    ball = ObjectProperty(None)

    def serve_ball(self):
        self.ball.velocity = Vector(6, 0).rotate(randint(0, 360))

    def update(self,dt):
        self.ball.movement()

        if (self.ball.y < 0) or (self.ball.y > self.height -50):
            self.ball.velocity_y *= -1

        if (self.ball.x < 0) or (self.ball.x > self.width -50):
            self.ball.velocity_x *= -1

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update,1.0/60.0)
        return game
```


output:

![](/Users/brooke/Desktop/4.png)


### 4. Creating the Paddles


#### Description:
By using the PongPaddle class, which has a bounce_ball() method to reverse and slightly accelerate the ball when it collides with a paddle, this code extends the Pong game with paddles. Now, player1 and player2, two paddles declared as ObjectProperty instances, are part of the PongGame class. In addition, the bounce_ball() method on the paddles is called in order to manage ball collisions, and the update() method will check the ball's movement for collisions with the screen edges and the paddles. In terms of the on_touch_move() method, it enables players to move the paddles vertically depending on touch input.


main.py:
```
class PongPaddle(Widget):
    def bounce_ball(self,ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1.1

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self):
        self.ball.velocity = Vector(6, 0).rotate(randint(0, 360))

    def update(self,dt):
        self.ball.movement()

        if (self.ball.y < 0) or (self.ball.y > self.height -50):
            self.ball.velocity_y *= -1

        if (self.ball.x < 0) or (self.ball.x > self.width -50):
            self.ball.velocity_x *= -1

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

    def on_touch_move(self, touch):
        if touch.x < self.width / 1/4:
            self.player1.center_y = touch.y
        if touch.x > self.width / 3/4:
            self.player2.center_y = touch.y
```


output:

![](/Users/brooke/Desktop/5.png)


### 5. Increasing the Score


#### Description:
The Pong game now has a scoring system. Each of the two players in the PongGame class, player 1 and player 2, has a score attribute that increases when the ball touches the left or right side of the screen. In addition, the update() method will check the ball's movement, reverse its velocity if it touches the left or right side of the screen, and increase the score of the relevant player.


main.py:
```
class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self):
        self.ball.velocity = Vector(6, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.movement()

        if (self.ball.y < 0) or (self.ball.y > self.height -50):
            self.ball.velocity_y *= -1

        if self.ball.x < 0:
            self.ball.velocity_x *= -1
            self.player1.score +=1

        if self.ball.x > self.width -50:
            self.ball.velocity_x *= -1
            self.player2.score += 1

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
```


output:

![](/Users/brooke/Desktop/6.png)


## Final Code


main.py:
```
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

class PongPaddle(Widget):
    score = NumericProperty(0)
    def bounce_ball(self,ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1.1

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x,velocity_y)

    def movement(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self):
        self.ball.velocity = Vector(6, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.movement()

        if (self.ball.y < 0) or (self.ball.y > self.height -50):
            self.ball.velocity_y *= -1

        if self.ball.x < 0:
            self.ball.velocity_x *= -1
            self.player1.score +=1

        if self.ball.x > self.width -50:
            self.ball.velocity_x *= -1
            self.player2.score += 1

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

    def on_touch_move(self, touch):
        if touch.x < self.width / 1/4:
            self.player1.center_y = touch.y
        if touch.x > self.width / 3/4:
            self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update,1.0/60.0)
        return game

PongApp().run()
```


pong.kv:
```
<PongPaddle>:
    size: 25, 200
    canvas:
        Rectangle:
            pos: self.pos
            size: self.size

<PongBall>:
    size: 50, 50
    canvas:
        Ellipse:
            pos: self.pos
            size: self.size

<PongGame>:
    ball: pong_ball
    player1: player_left
    player2: player_right
    canvas:
        Rectangle:
            pos: self.center_x -5, 0
            size: 10, self.height

    Label:
        font_size: 250
        center_x: root.width /4
        top: root.top -150
        text: str(root.player2.score)

    Label:
        font_size: 250
        center_x: root.width * 3/4
        top: root.top -150
        text: str(root.player1.score)

    PongBall:
        id: pong_ball
        center: self.parent.center

    PongPaddle:
        id: player_left
        x: root.x
        center_y: root.center_y

    PongPaddle:
        id: player_right
        x: root.width - self.width
        center_y: root.center_y
```


## Reference
https://kivy.org/doc/stable/tutorials/pong.html






