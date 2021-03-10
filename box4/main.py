import pygame
import random

from vector import (
    Vector,
    normalize,
    dist,
    approach,
    dot
)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

FRAME_RATE = 60

BACKGROUND_COLOUR = (0, 0, 0)
PLAYER_COLOR = (255, 255, 255)
ENEMY_COLOR = (random.randint(100, 255), 0, 0)

PLAYER_SIZE = (40, 40)
ENEMY_SIZE = (10, 10)

class Box:

    def __init__(self, x: float, y: float, width: int, height: int):
        self.v_pos = Vector(x, y)
        self.v_goal = Vector(0, 0)
        self.v_velocity = Vector(0, 0)
        self.speed = 600
        self.gravity = -4
        self.rect = pygame.rect.Rect(x, y, width, height)
    
    def update(self, dt: float):
        self.v_velocity.x = approach(self.v_goal.x, self.v_velocity.x, dt * 30)
        self.v_velocity.y = approach(self.v_goal.y, self.v_velocity.y, dt * 30)
        self.v_pos = self.v_pos + self.v_velocity * dt
        self.v_velocity = self.v_velocity + self.gravity * dt
        self.rect.x = self.v_pos.x
        self.rect.y = self.v_pos.y


class Player(Box):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
    
    def key_down(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.v_goal.x = self.speed
        if keys[pygame.K_LEFT]:
            self.v_goal.x = -self.speed
        if keys[pygame.K_UP]:
            self.v_goal.y = -self.speed
        if keys[pygame.K_DOWN]:
            self.v_goal.y = self.speed
    
    def key_up(self, key: int):
        if key == pygame.K_RIGHT or key == pygame.K_LEFT:
            self.v_goal.x = 0
        if key == pygame.K_UP or key == pygame.K_DOWN:
            self.v_goal.y = 0
    
    def update(self, dt: float):
        self.key_down()
        super().update(dt)
        self.remain_within_bounds()

    def remain_within_bounds(self):
        if self.rect.x < 0:
            self.rect.x = 0
            self.v_velocity.x = self.rect.x
            self.v_pos.x = self.rect.x
        if (self.rect.x+self.rect.width) > SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH - self.rect.width
            self.v_velocity.x = 0
            self.v_pos.x = self.rect.x
        if self.rect.y < 0:
            self.rect.y = 0
            self.v_velocity.y = self.rect.y
            self.v_pos.y = self.rect.y
        if (self.rect.y+self.rect.height) > SCREEN_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.v_velocity.y = 0
            self.v_pos.y = self.rect.y


class Enemy(Box):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.speed = 2
        self.speed_factor = 0.5
        self.FACTOR = random.uniform(0.5, 1.0)
    
    def update(self, dt: float, player: Player):
        self.v_goal = player.v_pos - self.v_pos
        self.v_goal = normalize(self.v_goal) * self.speed_factor
        self.speed_factor += self.FACTOR
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.speed_factor -= self.FACTOR
        if self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT - self.rect.height:
            self.speed_factor -= self.FACTOR
        distance = dist(player.v_pos, self.v_pos)
        if distance >= 0 and distance <= player.rect.width and distance <= player.rect.height:
            self.speed_factor /= 2
        return super().update(dt)


class Missile(Box):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
    
    def update(self, dt):
        return super().update(dt)


def create_enemies(amount: int):
    enemies = []
    for i in range(amount):
        e_start_x = random.randrange(int(SCREEN_WIDTH/2)-ENEMY_SIZE[0], SCREEN_WIDTH-ENEMY_SIZE[0])
        e_start_y = random.randrange(0, int(SCREEN_HEIGHT/2)-ENEMY_SIZE[1])
        enemies.append(Enemy(e_start_x, e_start_y, *ENEMY_SIZE))
    return enemies

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    player = Player(0, SCREEN_HEIGHT - PLAYER_SIZE[1], *PLAYER_SIZE)
    enemies = create_enemies(1)
    while running:
        clock.tick(FRAME_RATE)
        dt = clock.tick(FRAME_RATE) / 100
        for evt in pygame.event.get():
            if evt.type == pygame.KEYUP and evt.key == pygame.K_ESCAPE:
                running = False
            if evt.type == pygame.KEYUP:
                player.key_up(evt.key)
            if evt.type == pygame.KEYUP and evt.type == pygame.K_SPACE:
                pass
        player.update(dt)
        for enemy in enemies:
            enemy.update(dt, player)
        # drawing objects
        screen.fill(color=BACKGROUND_COLOUR)
        for enemy in enemies:
            screen.fill(rect=enemy.rect, color=ENEMY_COLOR)
        screen.fill(rect=player.rect, color=PLAYER_COLOR)
        # flip screen
        pygame.display.flip()

if __name__ == '__main__':
    main()