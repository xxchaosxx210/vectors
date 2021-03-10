import pygame

import vector
from vector import Vector
from properties import (
    screen,
    BOUNDING_BOX_COLOUR
)


class Player:

    def __init__(self, width: int=100, height: int=30):
        self.reset(width, height)
        self.color = (50, 150, 150)
    
    def reset(self, width, height):
        x = screen.width/2-width
        y = screen.height-height
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.position = Vector(x, y)
        self.velocity = Vector(0, 0)
        self.goal = Vector(0, 0)
        self.speed = 300

    def draw(self):
        #pygame.draw.rect(screen.surface, BOUNDING_BOX_COLOUR, self.rect, 2)
        screen.surface.fill(rect=self.rect, color=self.color)

    def update(self, dt):
        self.velocity.x = vector.approach(self.goal.x, self.velocity.x, dt * 30)
        self.velocity.y = vector.approach(self.goal.y, self.velocity.y, dt * 30)
        self.position = self.position + self.velocity * dt
        self.velocity = self.velocity + -4 * dt
        self.rect.x = self.position.x
        self.rect.y = screen.height - self.rect.height
        self.check_bounds()
    
    def check_bounds(self):
        if self.rect.x < 0:
            self.rect.x = 0
            self.position.x = self.rect.x
            self.velocity.x = 0.5
        if self.rect.x > screen.width-self.rect.width:
            self.rect.x = screen.width-self.rect.width
            self.position.x = self.rect.x
            self.velocity.x = 0.5

    def onkeydown(self, key):
        if key == pygame.K_LEFT:
            self.goal.x = -self.speed
        elif key == pygame.K_RIGHT:
            self.goal.x = self.speed

    def onkeyup(self, key):
        if key == pygame.K_LEFT:
            self.goal.x = 0
        elif key == pygame.K_RIGHT:
            self.goal.x = 0
    
    def __str__(self):
        return f"PLAYER RECT: posX={self.position.x}, posY={self.position.y}, right={self.position.x+self.rect.width}, top={self.position.y-self.rect.height}"