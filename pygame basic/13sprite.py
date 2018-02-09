# -*- coding: utf-8 -*-

import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

screen_width = 700
screen_height = 500

class Block(pygame.sprite.Sprite):
    def __init__(self,color,width,height):
        super().__init__()
        #pygame.Surface((5,5)): create blank surface(image), default color : black
        #load image 할때는 convert 반드시 해줘야 이미지 처리 속도 빨라짐
        self.image = pygame.image.load("image/tank.png").convert()
        #making the color transparent
        self.image.set_colorkey(BLACK)
    
        
        #dimesion of the object(rect.x,rect.y로 접근 가능)
        #default는 (0,0)
        self.rect = self.image.get_rect()
        
        #sprite 에는 반드시 image와 rect attribute가 필요함!
        
    def update(self):
        self.rect.y += 1
        if self.rect.bottom > screen_height:
            self.reset()
            
    def reset(self):
        self.rect.x = random.randrange(screen_width)
        self.rect.y = random.randrange(-100,-10)

def main():
    pygame.init()
    
    size = (screen_width,screen_height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('My game')
    
    done = False
    clock = pygame.time.Clock()
    
    #making list of sprites
    block_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()
    
    for i in range(20):
        block = Block(BLACK,20,15)
        block.rect.x = random.randrange(screen_width)
        block.rect.y = random.randrange(screen_height)
        
        block_list.add(block)
        all_sprites_list.add(block)
    
    player = Block(RED, 20, 15)
    all_sprites_list.add(player)
    
    score = 0
    
    while not done:
        #main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        #screen clearing(either with white screen or other background images)
        screen.fill(WHITE)
        
        #drawing code
        pos = pygame.mouse.get_pos()
        player.rect.centerx = pos[0]
        player.rect.centery = pos[1]
        
        #group의 각 sprite에 대해 update라는 메서드 불러오기.
        #기본적으로 sprite class의 update method는 do nothing
        #여기선 block class 정의할때 update method를 override했으므로 그거 실행됨
        block_list.update()
        #checks collision(player against block_list), return overlapping sprite
        #True 는 충돌시 그 sprite 삭제, false는 삭제 안함
        blocks_hit_list = pygame.sprite.spritecollide(player,block_list,False)
        
        for block in blocks_hit_list:
            score += 1
            block.reset()
        
        font = pygame.font.SysFont('Calibri',25)
        text = font.render("score: {0}".format(score),True,BLACK)
        screen.blit(text,[0,0])
        
        
        all_sprites_list.draw(screen)
        
        
        #update screen
        pygame.display.flip()
        
        clock.tick(60)
        
    pygame.quit()
        
if __name__ == "__main__":
    main()

