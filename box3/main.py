__description__ = """Example of using vectors to work out distance between two objects and direction of an object
    also uses Lerp to smooth movement.
    The red box (Enemy) will always chase the White Box (Player)
    """
__author__ = "Paul Millar"

import pygame
import vector
import random

FRAME_RATE = 90

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

BOX_SIZE = 40

ENEMY_SIZE = 10

class Box:

    def __init__(self, x: float, y:float, width: int, height):
        self.pos = vector.Vector(x, y)
        self.current_velocity = vector.Vector(0, 0)
        self.velocity_goal = vector.Vector(0, 0)
        self.gravity = -4
        self.speed = 100
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect((x, y), (width, height))
    
    def update(self, dt: float):
        """uses a linear interpolation (Lerp) to calculate the next position from velocity and the goal

        Args:
            dt (float): time delta from last frame calculate the diffeence and add it to velocity
        """
        self.current_velocity.x = vector.approach(self.velocity_goal.x, self.current_velocity.x, dt * 30)
        self.current_velocity.y = vector.approach(self.velocity_goal.y, self.current_velocity.y, dt * 30)
        # vector = vector + vector * deltatime
        self.pos = self.pos + self.current_velocity * dt
        # vector = vector + gravity * deltatime
        # add the velocity for next frame
        self.current_velocity = self.current_velocity + -4 * dt
        # set rect x and y coords to be updated onto screen
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        # Make sure the Box doesnt go off the Screen
        if self.rect.x < 0:
            self.rect.x = 0
            self.current_velocity.x = -self.current_velocity.x
            self.pos.x = self.rect.x
        if (self.rect.x+self.rect.width) > SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH - self.rect.width
            self.current_velocity.x = -self.current_velocity.x
            self.pos.x = self.rect.x
        if self.rect.y < 0:
            self.rect.y = 0
            self.current_velocity.y = -self.current_velocity.y
            self.pos.y = self.rect.y
        if (self.rect.y+self.rect.height) > SCREEN_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.current_velocity.y = -self.current_velocity.y
            self.pos.y = self.rect.y

class Player(Box):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
    
    def key_down(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.velocity_goal.x = self.speed
        if keys[pygame.K_LEFT]:
            self.velocity_goal.x = -self.speed
        if keys[pygame.K_UP]:
            self.velocity_goal.y = -self.speed
        if keys[pygame.K_DOWN]:
            self.velocity_goal.y = self.speed
    
    def on_key_up(self, key):
        if key == pygame.K_RIGHT or key == pygame.K_LEFT:
            self.velocity_goal.x = 0
        if key == pygame.K_UP or key == pygame.K_DOWN:
            self.velocity_goal.y = 0
    
    def update(self, dt):
        self.key_down()
        return super().update(dt)


class Enemy(Box):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.speed = 2
        self.speed_factor = 0.5
        self.FACTOR = random.uniform(0.1, 0.5)
    
    def update(self, dt: float, player: Player):
        """get the direction of the player and head towards the player incrmeneting the speed_factor counter
        everytime this method is called

        Args:
            dt (float): delta time
            player (Player): player object pos to be calculated

        Returns:
            [super]: returned from parent class
        """
        # get the direction of the player
        self.velocity_goal = player.pos - self.pos
        # multiply the direction unit by speed factor
        self.velocity_goal = vector.normalize(self.velocity_goal) * self.speed_factor
        # increase enemy speed factor for next frame
        self.speed_factor += self.FACTOR
        # get the distance between the player and enemy
        distance = vector.dist(player.pos, self.pos)
        if distance >= 0 and distance <= player.width:
            # if boxes are touching then slow the speed_factor down
            self.speed_factor /= 2
        return super().update(dt)


def create_enemies(amount: int):
    enemies = []
    for i in range(10):
        # get random X and Y starting position. inbetween Center and Edge of screen
        e_start_x = random.randrange(int(SCREEN_WIDTH/2)-ENEMY_SIZE, SCREEN_WIDTH-ENEMY_SIZE)
        e_start_y = random.randrange(0, int(SCREEN_HEIGHT/2)-ENEMY_SIZE)
        enemies.append(Enemy(e_start_x, e_start_y, ENEMY_SIZE, ENEMY_SIZE))
    return enemies


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    # Player Box. Start at bottom left of screen
    player = Player(0, SCREEN_HEIGHT-BOX_SIZE, BOX_SIZE, BOX_SIZE)

    # Create enemy boxes
    enemies = create_enemies(10)

    while running:
        clock.tick(FRAME_RATE)
        dt = clock.tick(FRAME_RATE) / 100
        for evt in pygame.event.get():
            if evt.type == pygame.KEYUP and evt.key == pygame.K_ESCAPE:
                # quit the game
                running = False
            if evt.type == pygame.KEYUP and evt.key == pygame.K_SPACE:
                enemies = create_enemies(10)
            if evt.type == pygame.KEYUP:
                player.on_key_up(evt.key)
        # update the player position
        player.update(dt)
        # loop through enemy positions
        list(map(lambda e: e.update(dt, player), enemies))
        screen.fill(color=(0, 0, 0))
        screen.fill(rect=player.rect, color=(200, 200, 200))
        # draw enemies to buffer
        list(map(lambda e: screen.fill(rect=e.rect, color=(200, 0, 0)), enemies))
        pygame.display.flip()


if __name__ == '__main__':
    main()