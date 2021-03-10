import pygame
import random
import math

import vector
from vector import Vector
from properties import (
    screen,
    BOUNDING_BOX_COLOUR
)

from player import Player

class Ball:

    def __init__(self, radius: int = 5):
        self.radius = radius
        self.diameter = self.radius * 2
        self.colour = (255, 255, 255)
        self.moving = False
        self.rect = pygame.rect.Rect(0, 0, self.diameter, self.diameter)
    
    def reset(self, player: Player):
        """reset the ball position above the player box

        Args:
            player (Player): payer object
        """
        x = screen.width/2 - (player.rect.right-self.radius)
        y = player.rect.y - 20
        self.position = Vector(x, y)
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        self.velocity = Vector(0, 0)
        self.moving = False
        self.fallen = False
        self.speed = 50
        self.timer = 0

    def draw(self):
        # pygame.draw.line(screen.surface, (100, 100, 255), (self.velocity.x, self.velocity.y), 
        #                  (self.position.x, self.position.y), 2)
        #pygame.draw.rect(screen.surface, BOUNDING_BOX_COLOUR, self.rect, 2)
        pygame.draw.circle(screen.surface, self.colour, (self.rect.x, self.rect.y), int(self.radius))
    
    def attach_to_player(self, player: Player):
        """put the ball at the center and on top of the Player. if not moving

        Args:
            player (Player): player object
        """
        ball_center_x = (player.rect.width/2)-self.radius
        new_x = player.position.x + ball_center_x
        new_y = player.position.y - 20
        self.position = Vector(new_x, new_y)
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def update(self, dt: float, player: Player):
        if self.moving:
            self.position = self.position + self.velocity * dt
            if self.timer > 60*5:
                prev_velocity = vector.copy(self.velocity)
                self.change_velocity(self.speed+5)
                self.timer = 0
            self.timer += 1
        else:
            self.attach_to_player(player)
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        if not self.hit(player):
            self.check_bounds()
    
    def change_velocity(self, speed: int):
        self.speed = speed
        self.velocity = vector.normalize(self.velocity) * speed

    def hit(self, player: Player):
        collision_threshold = 15
        if self.rect.colliderect(player.rect) and self.velocity.y > 0.0:
            # check if ball is on top of paddle. 
            # make sure ball doesnt get stuck. so if velocity zero dont move ball Y velocity
            on_top = abs(self.rect.bottom-player.rect.top)
            print(f"OnTop: {on_top}, Threshold: {collision_threshold}")
            if on_top < collision_threshold:
                self.velocity.y = -self.velocity.y
            else:
                self.velocity.x = -self.velocity.x
            return True
        return False

    def check_bounds(self):
        threshold = 5
        if self.rect.left < threshold:
            self.velocity.x = -self.velocity.x
        
        if self.rect.right > screen.width-threshold and self.velocity.x > 0.0:
            self.velocity.x = -self.velocity.x
        
        if self.rect.top < threshold:
            self.velocity.y = -self.velocity.y
        
        if self.rect.top > screen.height+100:
            # fallen off screen
            self.fallen = True
    
    def new_angled_velocity(self):
        """returns a random velocity vector pointing at a non straight direction

        Returns:
            [Vector]: returns a unit Vector
        """
        # 0.0 = right
        # 90.0 straight up
        # 180 = left
        # between 20.0 - 60.0 right, 120.0 - 160.0
        # use angles that will start well in game. Avoid straight paths
        # angles that point to the left
        angles = [float(x) for x in range(120, 150, 1)]
        # angles that point to the right
        angles.extend([float(x) for x in range(30, 50, 1)])
        # choose our angle from the list
        angle = random.choice(angles)
        x = math.cos(math.radians(angle))
        y = math.sin(math.radians(270))
        return vector.normalize(Vector(x, y))
    
    def start(self, player: Player):
        direction = self.new_angled_velocity()
        self.velocity = self.velocity + direction * self.speed
        self.moving = True
        self.fallen = False
    
    def __str__(self):
        return f"BALL RECT: posX={self.position.x}, posY={self.position.y}, right={self.rect.right}, top={self.rect.bottom}"