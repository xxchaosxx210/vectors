import vector
import commons
import pygame
from vector import Vector

from enum import Enum

class BallType(Enum):
    DEFAULT = 0

class Ball:

    def __init__(self, position: Vector, velocity=Vector(0, 0), 
                 radius: float=8, ball_type=BallType.DEFAULT):
        self.position = vector.copy(position)
        self.velocity = vector.copy(velocity)

        self.radius = radius
        self.diameter = radius * 2.0
        self.bounding_box = pygame.rect.Rect(0, 0, 1, 1)
        self.alive = True
    
    def update(self):
        self.velocity.y = self.velocity.y + commons.DELTA_TIME * commons.GRAVITY
        self.position = self.position + self.velocity * commons.DELTA_TIME
        self.check_collisions()

    def draw(self):
        pygame.draw.circle(commons.SCREEN, (255, 255, 255), (self.position.x, self.position.y), self.radius)
    
    def check_collisions(self):
        if self.position.x < self.radius or self.position.x > commons.SCREEN_WIDTH - self.radius:
            self.velocity.x = -self.velocity.x
        if self.position.y < self.radius:
            self.velocity.y = -self.velocity.y
        if self.position.y > commons.SCREEN_HEIGHT + self.radius:
            self.alive = False