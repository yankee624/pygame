# -*- coding: utf-8 -*-

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

def draw_player_image(screen,player_image,x,y):
    screen.blit(player_image,[x,y])

def bullet(screen,x,y):
    pygame.draw.line(screen,RED,[x,y],[x+5,y],2)

def main():
    pygame.init()

    size = (700,500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('My game')
    
    background_image = pygame.image.load("image/winter.jpg").convert()
    player_image = pygame.image.load("image/tank.png").convert()
    player_image.set_colorkey(BLACK)
    
    click_sound = pygame.mixer.Sound("sound/laser5.ogg")
    
    #background music
    pygame.mixer.music.load('sound/background.ogg')
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.mixer.music.play()
    
    
    done = False
    clock = pygame.time.Clock()
    
    font = pygame.font.SysFont('Calibri',25,True,False)
    
    player_x = 0
    player_y = 0
    player_x_speed = 0
    player_y_speed = 0  

    
    while not done:
        #main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            #spacebar 누르면 소리
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                click_sound.play()
        

                
            #background music 끝나면 다른 거 플레이하도록
            elif event.type == pygame.constants.USEREVENT:
                pygame.mixer.music.play()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_speed -= 3
                if event.key == pygame.K_RIGHT:
                    player_x_speed += 3
                if event.key == pygame.K_UP:
                    player_y_speed -= 3
                if event.key == pygame.K_DOWN:
                    player_y_speed += 3
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player_x_speed += 3
                if event.key == pygame.K_RIGHT:
                    player_x_speed -= 3
                if event.key ==pygame.K_UP:
                    player_y_speed += 3
                if event.key == pygame.K_DOWN:
                    player_y_speed -= 3

        #game logic
        player_x += player_x_speed
        player_y += player_y_speed

        
        #screen clearing(either with white screen or other background images)
        screen.blit(background_image,[0,0])
        
        #drawing code
        draw_player_image(screen,player_image,player_x,player_y)

        if player_x > 700:
            text = font.render('Too far',True, BLACK)
            screen.blit(text,[300,200])
            click_sound.play()
        
        #update screen
        pygame.display.flip()
        
        clock.tick(60)
        
    pygame.quit()
        
if __name__ == "__main__":
    main()