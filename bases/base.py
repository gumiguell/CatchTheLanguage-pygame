import pygame
from pygame.locals import *

pygame.init()

WHITE = (255,255,255)

screen = pygame.display.set_mode((800, 600))
screen.fill(WHITE)
pygame.display.set_caption("Base 1")

status = True

FPS = pygame.time.Clock()
x = 0
y = 0
ballSpeed = 10
direction = 1

while status:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                status = False
            if event.key == pygame.K_RIGHT:
                x += 20
            if event.key == pygame.K_LEFT:
                x -= 20
            if event.key == pygame.K_UP:
                y -= 20
            if event.key == pygame.K_DOWN:
                y += 20
                
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0, 0, 255), (x, y), 20)
    
    #x += direction * ballSpeed
    # if x > screen.get_width():
    #     x = screen.get_width()
    #     direction = -1 
    # elif x < 0:
    #     x = 0
    #     direction = 1  

    #pygame.display.flip()
    pygame.display.update()
    FPS.tick(60)

pygame.quit()