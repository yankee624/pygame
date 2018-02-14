# -*- coding: utf-8 -*-
import pygame as pg
import random
import importlib

#import settings
#importlib.reload(settings)
from settings import *

vec = pg.math.Vector2

def collide_hit_rect(one,two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_group(sprite, group, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(sprite,group,False,collide_hit_rect)
            if hits:
                if sprite.rect.centerx < hits[0].rect.centerx:
                    sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width/2
                if sprite.rect.centerx > hits[0].rect.centerx:
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width/2
                sprite.hit_rect.centerx = sprite.pos.x
                sprite.vel.x = 0
        if dir == 'y':
            hits = pg.sprite.spritecollide(sprite,group,False,collide_hit_rect)
            if hits:
                if sprite.rect.centery < hits[0].rect.centery:
                    sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height/2
                if sprite.rect.centery > hits[0].rect.centery:
                    sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height/2
                sprite.hit_rect.centery = sprite.pos.y
                sprite.vel.y = 0  
     


class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT #그냥 rect는 rotate할때 크기가 변함 ->
        self.hit_rect.center = self.rect.center#벽에 붙어서 rotate하면 갑자기 collision되는 경우 발생함
                                          #따라서 hit_rect로 collision check
        self.pos = vec(x,y) * TILESIZE
        self.vel = vec(0,0)
        self.rot = 0
        self.last_shot = pg.time.get_ticks()
        self.health = PLAYER_HEALTH
    
    def get_keys(self):
        self.vel = vec(0,0)
        self.rot_speed = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
            #좌표평면 상에서는 vec(1,0)을 양의방향(시계반대)회전하면 y>0지만 여기선 y<0(화면위쪽이 y작음)
            #그래서 -self.rot 회전시킨것
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot) #뒤로갈땐 속도 반
         
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                dir = vec(1,0).rotate(-self.rot)
                Bullet(self.game,pos,dir)
                self.vel = vec(-KICKBACK,0).rotate(-self.rot)
            
    
    def update(self):
        self.get_keys()
        #time based movement(independent from frame rate)
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt #self.rect.x에 이값을 바로 집어넣으면 소숫점 버림 - lose data
        #x,y방향 collision check 따로해서 대각선으로 벽에 부딪힐경우 충돌안한 축방향으로는 계속 slide해서 가도록
        self.hit_rect.centerx = self.pos.x
        collide_with_group(self,self.game.walls,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_group(self,self.game.walls,'y')
        self.rect.center = self.hit_rect.center
        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        super().__init__(self.groups)
        self.game = game
        self.image = self.game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        super().__init__(self.groups)
        self.game = game
        self.image = self.game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy() #rect는 mutable object여서 한놈이 바꾸면 다른놈꺼도 바뀜. copy해야.
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rot = 0
        self.health = MOB_HEALTH
        
        
    def update(self):
        #player 방향으로 rotate(항상 player를 바라보도록)
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.mob_img,self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos        
        self.acc = vec(MOB_ACC, 0).rotate(-self.rot)
        self.acc += self.vel * -1 #friction
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_group(self,self.game.walls,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_group(self,self.game.walls,'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
            
    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0,0,width,7)
        if self.health < MOB_HEALTH: #한대 맞았을때부터 표시
            pg.draw.rect(self.image,col,self.health_bar)
        
        
     
class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        super().__init__(self.groups)
        self.game = game
        self.image = self.game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos) #vec붙이는이유: copy만들기. 안하면 player pos을 수정해버림
        self.rect.center = self.pos
        spread = random.uniform(-GUN_SPREAD,GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        
    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self,self.game.walls): #spritecollide보다 기능 적지만 빠름
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()
    
        
        

        
        