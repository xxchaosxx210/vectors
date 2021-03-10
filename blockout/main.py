import pygame
import properties

from properties import screen
from player import Player
from ball import Ball


def draw():
    screen.surface.fill(color=properties.BACKGROUND_COLOUR)

def main():
    clock = pygame.time.Clock()
    running = True
    player = Player()
    ball = Ball()
    ball.reset(player)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if not ball.moving:
                    ball.start(player)
                else:
                    ball.change_velocity(ball.speed*2)
            elif event.type == pygame.KEYUP:
                player.onkeyup(event.key)
            elif event.type == pygame.KEYDOWN:
                player.onkeydown(event.key)
        # update
        player.update(properties.dt)
        ball.update(properties.dt, player)
        if ball.fallen:
            player.reset(player.rect.width, player.rect.height)
            ball.reset(player)
        # draw
        draw()
        player.draw()
        ball.draw()
        # flip
        pygame.display.flip()
        # count frames
        properties.dt = 0.01 * clock.tick(properties.FRAME_RATE)

if __name__ == '__main__':
    main()