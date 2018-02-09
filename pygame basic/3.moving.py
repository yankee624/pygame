# -*- coding: utf-8 -*-

import pygame
pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('레이싱')


black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False
carImg = pygame.image.load('racecar.png')


def car(x,y):
    gameDisplay.blit(carImg,(x,y))


x = (display_width * 0.45)
y = (display_height * 0.8)
x_change = 0

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -30
            if event.key == pygame.K_RIGHT:
                x_change = 30
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0
       
    x += x_change
    
    gameDisplay.fill(white)
    car(x,y)
    
    
    pygame.display.update()
    clock.tick(1)

#만약 저 위에 crashed =True 자리에 pygame.quit() 하면 error뜸
#pygame을 종료한 후에 display에 뭔가를 하려고 하니까...
#즉, pygame.quit은 pygame을 uninitialize할뿐임. 그 밑에 코드들은 그대로 실행    
pygame.quit()
    

