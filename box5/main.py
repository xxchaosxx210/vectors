from vector import (
    Vector,
    normalize,
    dist,
    approach,
    random_direction,
    random_vector
)

import pygame
import random

FRAME_RATE = 120

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BALL_SIZE = (20, 20)

BACKGROUND_COLOUR = (0, 0, 0)
BALL_COLOUR = (255, 255, 255)


class Box:

    def __init__(self, x, y, width, height):
        self.vecpos = Vector(x, y)
        self.vecvel = Vector(0, 0)
        self.vecgoal = Vector(0, 0)
        self.speed = 400
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.gravity = 200.0


class Player(Box):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.jumped = False
    
    def remain_within_bounds(self):
        if self.rect.x < 0:
            self.rect.x = 0
            self.vecvel.x = self.rect.x
            self.vecpos.x = self.rect.x
        if (self.rect.x+self.rect.width) > SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH - self.rect.width
            self.vecvel.x = 0
            self.vecpos.x = self.rect.x
        if self.rect.y < 0:
            self.rect.y = 0
            self.vecvel.y = self.rect.y
            self.vecpos.y = self.rect.y
        if (self.rect.y+self.rect.height) > SCREEN_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.vecvel.y = 0
            self.vecpos.y = self.rect.y
            self.jumped = False
    
    def key_down(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.vecgoal.x = self.speed
        if keys[pygame.K_LEFT]:
            self.vecgoal.x = -self.speed
        if keys[pygame.K_SPACE]:
            if not self.jumped:
                self.vecvel.y = -300
                self.jumped = True
    
    def key_up(self, key: int):
        if key == pygame.K_RIGHT or key == pygame.K_LEFT:
            self.vecgoal.x = 0
        if key == pygame.K_UP or key == pygame.K_DOWN:
            self.vecgoal.y = 0
    
    def update(self, dt):
        self.key_down()
        self.vecvel.x = approach(self.vecgoal.x, self.vecvel.x, dt * 30)
        self.vecvel.y = approach(self.vecgoal.y, self.vecvel.y, dt * 30)
        self.vecpos = self.vecpos + self.vecvel * dt
        self.vecvel.x = self.vecvel.x + -4 * dt
        self.vecvel.y = self.vecvel.y + self.gravity * dt
        self.rect.x = self.vecpos.x
        self.rect.y = self.vecpos.y
        self.remain_within_bounds()


def main():
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(0, SCREEN_HEIGHT-BALL_SIZE[1], *BALL_SIZE)
    while running:
        clock.tick(FRAME_RATE)
        dt = clock.tick(FRAME_RATE) / 100
        if dt > 0.15:
            dt = 0.15
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.KEYUP:
                player.key_up(event.key)
        player.update(dt)
        screen.fill(color=BACKGROUND_COLOUR)
        screen.fill(rect=player.rect, color=BALL_COLOUR)
        pygame.display.flip()
    

if __name__ == '__main__':
    main()