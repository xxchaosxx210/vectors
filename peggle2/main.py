import pygame
import commons
import entities

from ball import Ball
from vector import Vector
from vector import random_vector

from states import (
    playstate,
    menustate,
    gamestate
)

def update():
    entities.update_balls()

def draw():
    commons.SCREEN.fill((0, 0, 0))
    entities.draw_balls()

def main():
    pygame.init()
    app_running = True
    commons.SCREEN = pygame.display.set_mode((commons.SCREEN_WIDTH, commons.SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    while app_running:
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                app_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    rvec = random_vector() * 500
                    entities.balls.append(Ball(Vector(event.pos[0], event.pos[1]), rvec))

        update()
        draw()
        pygame.display.flip()
        commons.DELTA_TIME = 0.001 * clock.tick(120)

if __name__ == '__main__':
    main()