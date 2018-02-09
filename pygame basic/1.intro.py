# -*- coding: utf-8 -*-

import pygame
t=pygame.init()

ourScreen= pygame.display.set_mode((400,300))
pygame.display.set_caption('레이싱')
clock = pygame.time.Clock()

crashed = False

while not crashed:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
            
        print(event)
    
    #display 작업은 매우 복잡한 작업이므로 계산할것들 최대한 다 계산 후
    #한꺼번에 display하도록 한다.
    #update에 parameter를 넣으면 그 하나만 update하고 없으면 전부.
    #pygame.display.flip()은 무조건 전부.
    pygame.display.update()
    #30 frame per second(fps). 이게 높을수록 더 매끄러운 화면전환이 되는 대신
    #많은 작업이 필요함
    clock.tick(30)

#pygame 종료    
pygame.quit()
#python 종료
quit()