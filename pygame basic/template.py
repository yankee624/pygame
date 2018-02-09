# -*- coding: utf-8 -*-

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

def main():
    pygame.init()

    size = (700,500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('My game')
    
    done = False
    clock = pygame.time.Clock()
    
    while not done:
        #main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
        #game logic
        
        
        #screen clearing(either with white screen or other background images)
        screen.fill(WHITE)
        
        #drawing code
        
        #update screen
        pygame.display.flip()
        
        clock.tick(60)
        
    pygame.quit()
        
if __name__ == "__main__":
    main()

