# -*- coding: utf-8 -*-

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)


def draw_stick_figure(screen,x,y):
    # Head
    pygame.draw.ellipse(screen, BLACK, [1+x,y,10,10], 0)
 
    # Legs
    pygame.draw.line(screen, BLACK ,[5+x,17+y], [10+x,27+y], 2)
    pygame.draw.line(screen, BLACK, [5+x,17+y], [x,27+y], 2)
 
    # Body
    pygame.draw.line(screen, RED, [5+x,17+y], [5+x,7+y], 2)
 
    # Arms
    pygame.draw.line(screen, RED, [5+x,7+y], [9+x,17+y], 2)
    pygame.draw.line(screen, RED, [5+x,7+y], [1+x,17+y], 2)
    

def main():
    pygame.init()

    size = (700,500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('My game')
    
    done = False
    clock = pygame.time.Clock()
    

    
    x_coord = 10
    y_coord = 10
    x_speed = 0
    y_speed = 0
    
    while not done:
        #main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            '''
            만약 사이트에 설명대로 keydown일때 speed를 3으로,
            keyup일때 speed를 0으로 설정하면,
            왼쪽과 오른쪽 둘 다 눌렀다가 둘 중 하나 떼면 멈춤.
            (하나 떼는순간 speed가 0으로 되니까)
            그래서 이렇게 speed를 3빼고 더하고 하는 식으로 한것.
            '''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_speed -= 3
                if event.key == pygame.K_RIGHT:
                    x_speed += 3
                if event.key == pygame.K_UP:
                    y_speed -= 3
                if event.key == pygame.K_DOWN:
                    y_speed += 3
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    x_speed += 3
                if event.key == pygame.K_RIGHT:
                    x_speed -= 3
                if event.key ==pygame.K_UP:
                    y_speed += 3
                if event.key == pygame.K_DOWN:
                    y_speed -= 3
        #game logic
        x_coord += x_speed
        y_coord += y_speed
        
        if x_coord < 0:
            x_coord = 0
        if x_coord > 690:
            x_coord = 690
        
        if y_coord < -10:
            y_coord = 490
        if y_coord > 500:
            y_coord = -10
        
        #screen clearing(either with white screen or other background images)
        screen.fill(WHITE)
        
        #drawing code
        draw_stick_figure(screen,x_coord,y_coord)
        
        #update screen
        pygame.display.flip()
        
        clock.tick(60)
        
    pygame.quit()
        
if __name__ == "__main__":
    main()