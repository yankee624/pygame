import pygame
import random
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
FPS = 30

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,'img')

def main():
    #initialize game and create window
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption('My game')
    clock = pygame.time.Clock()
    
    all_sprites = pygame.sprite.Group()
    
    done = False
    while not done:
        clock.tick(FPS)
        #process events(input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
        #game logic(update)
        all_sprites.update()

        
        #draw
        screen.fill(WHITE)
        all_sprites.draw(screen)
        
        #update screen
        pygame.display.flip()
        

        
    pygame.quit()
        
if __name__ == "__main__":
    main()