import pygame

from vector import (
    Vector,
    approach
)


class Player:

    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.rect.Rect((x, y), (width, height))
        self.vect_pos = Vector(x, y)
        self.vect_vel = Vector(0, 0)
        self.vect_goal = Vector(0, 0)

        self._speed = 100
    
    def update(self, evt: pygame.event.Event, dt: float):
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_LEFT:
                self.vect_goal.x = -15
            if evt.key == pygame.K_RIGHT:
                self.vect_goal.x = 15
            if evt.key == pygame.K_UP:
                self.vect_goal.y = -15
            if evt.key == pygame.K_DOWN:
                self.vect_goal.y = 15

        elif evt.type == pygame.KEYUP:
            if evt.key == pygame.K_LEFT:
                self.vect_goal.x = 0
            if evt.key == pygame.K_RIGHT:
                self.vect_goal.x = 0
            if evt.key == pygame.K_UP:
                self.vect_goal.y = 0
            if evt.key == pygame.K_DOWN:
                self.vect_goal.y = 0
    
        self.vect_vel.x = approach(self.vect_goal.x, self.vect_vel.x, dt * 20)
        self.vect_vel.y = approach(self.vect_goal.y, self.vect_vel.y, dt * 20)
        self.vect_pos = self.vect_pos + self.vect_vel * dt
        self.vect_vel = self.vect_vel + -4 * dt
        self.rect.x = self.vect_pos.x
        self.rect.y = self.vect_pos.y
        
def main():
    running = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    player = Player(0, 0, 50, 50)
    prev_ticks = 0
    current_ticks = clock.tick(60)
    while running:
        prev_ticks = current_ticks
        current_ticks = clock.tick(60)
        dt = current_ticks - prev_ticks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                player.update(event, dt)
        screen.fill(color=(200, 200, 200))
        screen.fill(color=(0, 0, 0), rect=player.rect)
        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    main()