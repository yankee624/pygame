# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 21:59:13 2018

@author: 공관
"""

import pygame
pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('레이싱')

#자주 쓰는 색들 미리 rgb값 설정해서 변수로 저장해놓고 쓰면 편함
#변수명 설정시 보통 변하지 않는 상수는 대문자로.
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

clock = pygame.time.Clock()
crashed = False
#이미지파일이 같은 디렉토리에 있으면 파일이름만, 아니면 전체경로.
#이미지의 배경색을 transparent로 해야 배경이 제대로 나옴
carImg = pygame.image.load('racecar.png')

#blit : 화면에 표시하기
def car(x,y):
    gameDisplay.blit(carImg,(x,y))

#이미지의 upper left가 좌표이므로 일부러 0.5, 1 대신 약간 여유를 준거
#0.5,1 할경우 이미지가 화면 넘어갈 듯
x= (display_width * 0.45)
y = (display_height * 0.8)

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    
    #아래 두 줄 순서를 바꾸면 차를 그린 후 배경을 칠하므로 흰색밖에안보임        
    gameDisplay.fill(WHITE)
    car(x,y)
    
    
    pygame.display.update()
    clock.tick(1)
    
pygame.quit()
