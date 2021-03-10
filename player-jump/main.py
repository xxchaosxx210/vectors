import pygame

from vector import (
    Vector,
    normalize,
    dist,
    approach
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20

FRAME_RATE = 60

BACKGROUND_COLOUR = (0, 0, 0)
PLAYER_COLOR = (255, 255, 255)


class Player:

    def __init__(self, x, y, width, height):
        self.v_pos = Vector(x, y)
        self.v_goal = Vector(0, 0)
        self.v_vel = Vector(0, 0)
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.gravity = 200.0
        self.speed = 400
        self.jumped = False
    
    def update(self, dt):
        self.v_vel.x = approach(self.v_goal.x, self.v_vel.x, dt * 30)
        self.v_vel.y = approach(self.v_goal.y, self.v_vel.y, dt * 30)
        if self.v_vel.x > 50.0:
            self.v_vel.x = 50.0
        if self.v_vel.x < -50.0:
            self.v_vel.x = -50.0
        self.v_pos = self.v_pos + self.v_vel * dt
        self.v_vel.x = self.v_vel.x + -4 * dt
        self.v_vel.y = self.v_vel.y + self.gravity * dt
        self.rect.x = self.v_pos.x
        self.rect.y = self.v_pos.y
        self.check_bounds()
        print(f"VelocityX={self.v_vel.x}")

    def check_bounds(self):
        # Check player is left edge
        if self.rect.x < 0:
            self.rect.x = 0
            self.v_vel.x = self.rect.x
            self.v_pos.x = self.rect.x
        # Check Player is near right edge
        if (self.rect.x+self.rect.width) > SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH - self.rect.width
            self.v_vel.x = 0
            self.v_pos.x = self.rect.x
        # Check PLayer is top of screen
        # if self.rect.y < 0:
        #     self.rect.y = 0
        #     self.v_pos.y = self.rect.y
        # Check Player is on Floor
        if (self.rect.y+self.rect.height) > SCREEN_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.v_vel.y = 0
            self.v_pos.y = self.rect.y
            self.jumped = False

    def key_down(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.v_goal.x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.v_goal.x = self.speed
        if keys[pygame.K_SPACE]:
            if not self.jumped:
                self.v_vel.y = -200
                self.jumped = True
    
    def key_up(self, key):
        if key == pygame.K_RIGHT or key == pygame.K_LEFT:
            self.v_goal.x = 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    player = Player(0, SCREEN_HEIGHT-PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    while running:
        clock.tick(FRAME_RATE)
        dt = clock.tick(FRAME_RATE)
        if dt > 0.15:
            dt = 0.15
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.KEYUP:
                player.key_up(event.key)
        player.key_down()
        player.update(dt)
        screen.fill(color=BACKGROUND_COLOUR)
        screen.fill(rect=player.rect, color=PLAYER_COLOR)
        pygame.display.flip()

if __name__ == '__main__':
    main()