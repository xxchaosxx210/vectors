import pygame
import vector

FRAME_RATE = 90

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

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
    
    def update(self, dt: float):
        self.key_down()
        # small incrmenets
        n = vector.normalize(self.pos)
        #print(f"Normalize Position: {n.x}, {n.y}")
        self.current_velocity.x = vector.approach(self.velocity_goal.x, self.current_velocity.x, dt * 30)
        self.current_velocity.y = vector.approach(self.velocity_goal.y, self.current_velocity.y, dt * 30)
        # vector = vector + vector * deltatime
        self.pos = self.pos + self.current_velocity * dt
        # vector = vector + gravity * deltatime
        # add the velocity for next frame
        self.current_velocity = self.current_velocity + -4 * dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        # bounds check
        if self.rect.x < 0:
            self.rect.x = 0
            self.current_velocity.x = 0
            self.pos.x = self.rect.x
        if (self.rect.x+self.rect.width) > SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH - self.rect.width
            self.current_velocity.x = 0
            self.pos.x = self.rect.x
        if self.rect.y < 0:
            self.rect.y = 0
            self.current_velocity.y = 0
            self.pos.y = self.rect.y
        if (self.rect.y+self.rect.height) > SCREEN_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.current_velocity.y = 0
            self.pos.y = self.rect.y


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
box = Box(0, SCREEN_HEIGHT-40, 40, 40)
while running:
    clock.tick(FRAME_RATE)
    dt = clock.tick(FRAME_RATE) / 100
    # if dt > 0.15:
    #     dt = 0.15
    for evt in pygame.event.get():
        if evt.type == pygame.KEYUP and evt.key == pygame.K_ESCAPE:
            running = False
        if evt.type == pygame.KEYUP:
            box.on_key_up(evt.key)
    box.update(dt)
    screen.fill(color=(0, 0, 0))
    screen.fill(rect=box.rect, color=(200, 200, 200))
    pygame.display.flip()