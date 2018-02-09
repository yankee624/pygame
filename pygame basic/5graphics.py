# -*- coding: utf-8 -*-

import pygame
import math

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
PI = math.pi

size = (700,500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('My game')


done = False
clock = pygame.time.Clock()

font = pygame.font.Font('C:/Windows/Fonts/calibrii.ttf',30)

frame_count = 0
frame_rate = 60
start_sec = 90

while not done:
    #main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    #game logic
    
    #screen clearing(either with white screen or other background images)
    screen.fill(WHITE)
    
    #drawing code
    pygame.draw.lines(screen, BLACK,False,[[0,0],[100,100],[100,40],[20,90]])


    #update screen
    pygame.display.flip()
    
    clock.tick(frame_rate)
    
pygame.quit()
        

