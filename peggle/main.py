import pygame

from vector import (
    Vector,
    normalize
)

from states import (
    playstate,
    menustate,
    gamestate
)

SCR_WIDTH = 800
SCR_HEIGHT = 600


class Circle:

    def __init__(self, x, y, radius):
        self.velocity = Vector(0, 0)
        self.position = Vector(x, y)
        self.following_mouse = False
        self.radius = radius
    
    def __str__(self):
        return f"velocityX={self.velocity.x}, velocityY={self.velocity.y}"

def update(dt: float, circle: Circle,
           m_pos_x: int, m_pos_y: int):

    if circle.following_mouse:
        mouse_pos_vec = Vector(m_pos_x, m_pos_y)
        # get the length direction from circle to mouse vectors
        diff_vec = mouse_pos_vec - circle.position
        # get the direction magnitude from circle_pos to mouse_pos
        n_direction = normalize(diff_vec)
        # incrment the velocity and return
        circle.velocity += n_direction * 500 * dt
        # update the position from the velocity
    circle.position += circle.velocity * dt
    print(circle)

def draw(screen: pygame.Surface, circle: Circle):
    screen.fill((50, 50, 50))
    pygame.draw.circle(screen, (255, 255, 255), circle.position.make_int_tuple(), circle.radius)

def main():
    pygame.init()
    app_running = True
    screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))

    clock = pygame.time.Clock()

    circle = Circle(0, 0, 10)
    mouse_position = (0, 0)

    dt = 0.0

    while app_running:
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                app_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    circle.following_mouse = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    circle.following_mouse = False
        update(dt, circle, *mouse_position)
        draw(screen, circle)
        pygame.display.flip()

        dt = 0.001 * clock.tick(120)

if __name__ == '__main__':
    main()