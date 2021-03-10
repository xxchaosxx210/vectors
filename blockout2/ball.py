import pygame
import random
import math

from vector import (
    Vector,
    normalize
)

from objects import Circle
from paddle import Paddle

from screen import Screen

BALL_DEFAULT_SPEED = 50


class Ball(Circle):

    def __init__(self, x, y, radius, colour=(255,255,255)):
        super().__init__(x, y, radius, colour=colour)
        self.moving = False
        self.fallen = False
        self.speed= BALL_DEFAULT_SPEED

def reset(ball: Ball):
    ball.moving = False
    ball.fallen = False
    ball.speed = BALL_DEFAULT_SPEED
    ball.velocity = Vector(0, 0)
    ball.position = Vector(0, 0)

def draw(ball: Ball, screen: Screen):
    pygame.draw.circle(screen.surface, ball.colour, (ball.rect.x, ball.rect.y), ball.radius)

def attach_to_paddle(ball: Ball, paddle: Paddle, screen: Screen):
    ball_center = (paddle.rect.width/2)-ball.radius
    x = paddle.position.x + ball_center
    y = paddle.rect.top - 2
    ball.position = Vector(x, y)
    ball.rect.x = ball.position.x
    ball.rect.y = ball.position.y

def update(ball: Ball, paddle: Paddle, screen: Screen, dt: float):
    if ball.moving:
        ball.position = ball.position + ball.velocity * dt
    else:
        attach_to_paddle(ball, paddle, screen)
    ball.rect.x = ball.position.x
    ball.rect.y = ball.position.y

    if not been_hit(ball, paddle):
        check_boundaries(ball, screen)

def been_hit(ball: Ball, paddle: Paddle):
    """check to see if ball hit paddle

    Args:
        ball (Ball): Ball object
        paddle (Paddle): Paddle Object

    Returns:
        [bool]: returns True if Ball benn hit
    """
    collision_threasold = 15
    if ball.rect.colliderect(paddle.rect) and ball.velocity.y > 0.0:
        ontop = abs(ball.rect.bottom-paddle.rect.top)
        if ontop < collision_threasold:
            ball.velocity.y = -ball.velocity.y
        else:
            ball.velocity.x = -ball.velocity.x
        return True
    return False

def check_boundaries(ball: Ball, screen: Screen):
    """make sure the ball bounces off the walls and falls if hit the floor

    Args:
        ball (Ball):
        screen (Screen):
    """
    threshold = 5
    if ball.rect.left < threshold and ball.velocity.x < 0.0:
        ball.velocity.x = -ball.velocity.x
    if ball.rect.right > screen.rect.width-threshold and ball.velocity.x > 0.0:
        ball.velocity.x = -ball.velocity.x
    if ball.rect.top < threshold and ball.velocity.y < 0.0:
        ball.velocity.y = -ball.velocity.y
    if ball.rect.top > screen.rect.height+100:
        ball.fallen = True

def new_angled_velocity(ball: Ball):
    angles = [float(x) for x in range(120, 150, 1)]
    angles.extend([float(x) for x in range(30, 50, 1)])
    angle = random.choice(angles)
    x = math.cos(math.radians(angle))
    y = math.sin(math.radians(angle))
    return normalize(Vector(x, y))

def start(ball: Ball, paddle: Paddle):
    direction = new_angled_velocity(ball)
    ball.velocity = ball.velocity + direction * ball.speed
    ball.moving = True
    ball.fallen = False