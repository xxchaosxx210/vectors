from collections import namedtuple
import pygame

pygame.init()

dt = 0.0

FRAME_RATE = 60

screen = namedtuple("Screen", ["width", "height", "surface"])(
                    800, 600, pygame.display.set_mode((800, 600)))

BACKGROUND_COLOUR = (0, 0, 0)
BOUNDING_BOX_COLOUR = (255, 0, 255)