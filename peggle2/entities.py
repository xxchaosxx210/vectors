from ball import Ball

balls = []

def update_balls():
    for i in range(balls.__len__()-1, -1, -1):
        balls[i].update()
        if not balls[i].alive:
            balls.remove(balls[i])

def draw_balls():
    for ball in balls:
        ball.draw()