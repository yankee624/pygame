# -*- coding: utf-8 -*-
import pygame as pg
import random
import importlib

#import settings
#importlib.reload(settings)
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx = 0
        self.vy = 0
    
    def get_keys(self):
        self.vx = 0
        self.vy = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self,self.game.walls,False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.rect.x = self.x
                self.vx = 0
        if dir == 'y':
            hits = pg.sprite.spritecollide(self,self.game.walls,False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.rect.y = self.y
                self.vy = 0  
                
    
    def update(self):
        self.get_keys()
        #time based movement(independent from frame rate)
        self.x += self.vx * self.game.dt #self.rect.x에 이값을 바로 집어넣으면 소숫점 버림 - lose data
        self.y += self.vy * self.game.dt
        #x,y방향 collision check 따로해서 대각선으로 벽에 부딪힐경우 충돌안한 축방향으로는 계속 slide해서 가도록
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        super().__init__(self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
        