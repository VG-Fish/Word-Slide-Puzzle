import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((640,480), HWSURFACE|DOUBLEBUF|RESIZABLE)
while True:
    pygame.event.pump()
    event = pygame.event.wait()
    if event.type == QUIT: pygame.display.quit()
    elif event.type == VIDEORESIZE:
        width, height = event.size
        if width < 600:
            width = 600
        if height < 400:
            height = 400
        screen = pygame.display.set_mode((width,height), HWSURFACE|DOUBLEBUF|RESIZABLE)