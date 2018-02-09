# -*- coding: utf-8 -*-

import pygame
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
SKY = (179,236,255)
GRAY = (196,196,196)
BROWN = (156,101,42)

size = (700,700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('My game')

done = False
clock = pygame.time.Clock()



class human():
    def __init__(self,x,x_change):
        self.x = x
        self.x_change = x_change
        self.y = 550
        self.foot = -20
        self.foot_change = 2
        self.hand = -10
        self.hand_change = 1
        self.head = -70
        self.head_fall = 1
        
    
    def stand(self):
        #leg
        pygame.draw.line(screen,BLACK,[self.x,self.y],[self.x + self.foot,600])
        pygame.draw.line(screen,BLACK,[self.x,self.y],[self.x - self.foot,600])
        #body
        pygame.draw.line(screen,BLACK,[self.x,self.y],[self.x,self.y-50])
        #head
        pygame.draw.circle(screen,BLACK,[self.x,self.y-70],20)
        #arm
        pygame.draw.line(screen,BLACK,[self.x,self.y-30],[self.x + self.hand,550])
        pygame.draw.line(screen,BLACK,[self.x,self.y-30],[self.x - self.hand,530])
        
        
    def move(self):
        pygame.draw.line(screen,BLACK,[self.x,self.y],[self.x + self.foot,600])
        pygame.draw.line(screen,BLACK,[self.x,self.y],[self.x - self.foot,600])
        #waving leg
        self.foot += self.foot_change
        if self.foot > 20 or self.foot < -20:
            self.foot_change *= -1
            
        pygame.draw.line(screen,BLACK,[self.x,self.y],[self.x,self.y-50])
        pygame.draw.circle(screen,BLACK,[self.x,self.y-70],20)
        
        pygame.draw.line(screen,BLACK,[self.x,self.y-30],[self.x + self.hand,550])
        pygame.draw.line(screen,BLACK,[self.x,self.y-30],[self.x - self.hand,530])
        #waving arm
        self.hand += self.hand_change
        if self.hand > 10 or self.hand < -10:
            self.hand_change *= -1
        #moving    
        self.x += self.x_change
        if self.x < 0 or self.x > 700:
            self.x_change *= -1

    def dead(self):
        pygame.draw.line(screen,BLACK,[self.x,self.y],[self.x + self.foot,600])
        pygame.draw.line(screen,BLACK,[self.x,self.y],[self.x - self.foot,600])
        
        pygame.draw.line(screen,BLACK,[self.x,self.y],[self.x,self.y-50])
        pygame.draw.circle(screen,RED,[self.x,self.y+self.head],20)
        #head drop
        self.head -= self.head_fall
        if self.y+self.head <400:
            self.head_fall *= -1
        
        pygame.draw.line(screen,BLACK,[self.x,self.y-30],[self.x + self.hand,550])
        pygame.draw.line(screen,BLACK,[self.x,self.y-30],[self.x - self.hand,530])
        

        
h1 = human(100,0)
h2 = human(200,5)
bullet_x = 140
bullet_change = 5

while not done:
    #main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    #game logic
    
    #screen clearing(either with white screen or other background images)
    screen.fill(SKY)
    
    
    #drawing code
    pygame.draw.rect(screen,BROWN,[0,600,700,100])
    
    #sun
    pygame.draw.circle(screen,YELLOW,[0,0],100)
    #cloud
    pygame.draw.ellipse(screen,GRAY,[100,50,100,50])
    pygame.draw.ellipse(screen,GRAY,[150,50,100,50])
    pygame.draw.ellipse(screen,GRAY,[200,50,100,50])
    
    pygame.draw.ellipse(screen,GRAY,[400,50,100,50])
    pygame.draw.ellipse(screen,GRAY,[450,50,100,50])
    pygame.draw.ellipse(screen,GRAY,[500,50,100,50])
    
    #house
    for i in range(-50,1000,200):
        pygame.draw.rect(screen,GREEN,[i,400,200,200])
        pygame.draw.polygon(screen,BLUE,[[i,400],[i+200,400],[i+100,300]])
        pygame.draw.rect(screen,WHITE,[i+50,500,100,100])
    
    h1.stand()
    pygame.draw.rect(screen,BLACK,[110,530,10,20])
    pygame.draw.rect(screen,BLACK,[110,530,30,10])
    pygame.draw.line(screen,BLACK,[bullet_x,535],[bullet_x + 2,535],2)
    bullet_x += bullet_change
    
    if bullet_x < h2.x:
        h2.move()
    else:
        h2.dead()
    
    
    
    
    #update screen
    pygame.display.flip()
    
    clock.tick(30)
    
pygame.quit()

