# -*- coding: utf-8 -*-

import pygame
import random


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

class Rectangle():
    def __init__(self):
        self.x = random.randrange(0,700)
        self.y = random.randrange(0,500)
        self.width = random.randrange(20,70)
        self.height = random.randrange(20,70)
        self.change_x = random.randrange(-3,4)
        self.change_y = random.randrange(-3,4)
        self.color = (random.randrange(0,256),random.randrange(0,256),random.randrange(0,256))
        
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,[self.x,self.y,self.width,self.height])

    def move(self):
        self.x += self.change_x
        self.y += self.change_y

class Ellipse(Rectangle):
    def __init__(self):
        super().__init__()
        
    def draw(self,screen):
        pygame.draw.ellipse(screen,GREEN,[self.x,self.y,self.width,self.height])

def main():
    pygame.init()

    size = (700,500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('My game')
    
    done = False
    clock = pygame.time.Clock()
    
    my_list = []
    for i in range(100):
        my_object = Rectangle()
        my_list.append(my_object)
        my_object = Ellipse()
        my_list.append(my_object)

    while not done:
        #main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
        #game logic
        for i in my_list:
            i.move()
        
        #screen clearing(either with white screen or other background images)
        screen.fill(WHITE)
        
        #drawing code
        for i in my_list:
            i.draw(screen)
        
        #update screen
        pygame.display.flip()
        
        clock.tick(60)
        
    pygame.quit()
        
if __name__ == "__main__":
    main()

