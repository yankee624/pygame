# -*- coding: utf-8 -*-

import pygame as pg
import random
import importlib
import settings
importlib.reload(settings)
from settings import *

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self,game,x,img):
        self.game = game
        self.groups = self.game.all_sprites,self.game.players
        super().__init__(self.groups)
        self.image = pg.transform.scale(img,(50,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,HEIGHT)
        self.pos = vec(self.rect.center)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
        self.run = 1.2
        self.jump_height = 15
        
        self.superspeed = False
        self.superjump = False
        self.freeze = False
        self.superspeed_timer = pg.time.get_ticks()
        self.superjump_timer = pg.time.get_ticks()
        self.freeze_timer = pg.time.get_ticks()
        
    def update(self):
        self.acc.y = GRAV
        self.pos += self.vel #vec(int(self.vel.x),int(self.vel.y))
        #int안해주면 -> vel 양수면 rect가 예상보다 작아지고, vel 음수면 rect 예상보다 커짐(-1.5는 -2가됨)
        
        #floating inaccuracy 방지
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        if abs(self.vel.y) < 0.1:
            self.vel.y = 0
        
        if self.pos.y > HEIGHT - self.rect.height / 2:
            self.pos.y = HEIGHT - self.rect.height / 2
            self.vel.y = 0
        if self.pos.x < self.rect.width / 2:
            self.pos.x = self.rect.width / 2
        if self.pos.x > WIDTH - self.rect.width / 2:
            self.pos.x = WIDTH - self.rect.width / 2

                
        self.vel += self.acc
        self.rect.center = self.pos
        
        #friction
        self.vel.x += self.vel.x * PLAYER_FRICTION
        
    def go_left(self):
        self.acc.x = -self.run
        
    def go_right(self):
        self.acc.x = self.run
    
    def go_down(self):
        self.vel.y += 13
    
    def stop(self):
        self.acc.x = 0
    
    def jump(self):
        if self.rect.bottom == HEIGHT:
            self.vel.y = -self.jump_height
        
class Ball(pg.sprite.Sprite):
    def __init__(self,game):
        self.game = game
        self.groups = self.game.all_sprites
        super().__init__(self.groups)
        self.image = pg.transform.scale(self.game.ball_img,(30,30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH / 2, HEIGHT-200)
        self.pos = self.rect.center
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.collide = None
        self.not_collide = None
        
    def update(self):
        self.acc.y = GRAV
        self.pos += vec(self.vel.x,self.vel.y) #바로 rect에 집어넣으면 data loss(소숫점 버리니까)
        #pos에 먼저 넣으면 pos은 data loss 안일어남. 그후 rect를 계속 pos값으로 동기화시키기
        
        #floating inaccuracy 방지
        if abs(self.vel.x) < 0.01:
            self.vel.x = 0
        if abs(self.vel.y) < 0.01:
            self.vel.y = 0
        
        #경계 넘어갈 시 bounce
        if self.pos.y > HEIGHT - self.rect.height / 2:
            self.pos.y = HEIGHT - self.rect.height / 2
            self.vel.y *= -0.9
            
        if self.pos.x < self.rect.width / 2:
            self.pos.x = self.rect.width / 2
            self.vel.x *= -0.9
        
        if self.pos.x > WIDTH - self.rect.width / 2:
            self.pos.x = WIDTH - self.rect.width / 2
            self.vel.x *= -0.9

        self.rect.center = self.pos

        self.vel += self.acc
        
        #friction and air resistance
        if self.vel.x != 0 and self.rect.bottom == WIDTH:
            self.vel.x += (self.vel.x / abs(self.vel.x)) * BALL_FRICTION
        if vec.length(self.vel) != 0 and self.rect.bottom < WIDTH:
            self.vel.x += self.vel.x * BALL_AIR_RESIST
        

class Item(pg.sprite.Sprite):
    last_spawn = pg.time.get_ticks()
    spawn_time = random.choice([5000,10000,15000])
    def __init__(self,game,x,y):
        self.game = game
        self.groups = self.game.all_sprites, self.game.items
        super().__init__(self.groups)
        self.type = random.choice(['superspeed','superjump','freeze'])
        if self.type == 'superspeed': self.image = self.game.superspeed_img
        elif self.type == 'superjump': self.image = self.game.superjump_img
        elif self.type == 'freeze': self.image = self.game.freeze_img
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
