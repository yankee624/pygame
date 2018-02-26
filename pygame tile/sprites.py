# -*- coding: utf-8 -*-
import pygame as pg
import random
import itertools
import importlib

#import settings
#importlib.reload(settings)
from settings import *
import pytweening as tween

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
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = PLAYER_HIT_RECT #그냥 rect는 rotate할때 크기가 변함 ->
        self.hit_rect.center = self.rect.center#벽에 붙어서 rotate하면 갑자기 collision되는 경우 발생함
                                          #따라서 hit_rect로 collision check
        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.rot = 0
        self.last_shot = pg.time.get_ticks()
        self.health = PLAYER_HEALTH
        self.weapon = 'pistol'
        self.damaged = False
    
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
            self.shoot()
            
    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            dir = vec(1,0).rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]['kickback'],0).rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = random.uniform(-WEAPONS[self.weapon]['spread'],WEAPONS[self.weapon]['spread'])
                Bullet(self.game,pos,dir.rotate(spread),WEAPONS[self.weapon]['damage'])
            MuzzleFlash(self.game,pos)
            
    def hit(self):
        self.damaged = True
        self.damage_alpha = itertools.chain(DAMAGE_ALPHA * 2) #빨갛게 깜빡깜빡
    
    def update(self):
        self.get_keys()
        #time based movement(independent from frame rate)
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        if self.damaged:
            try:
                self.image.fill((255,0,0,next(self.damage_alpha)),special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt #self.rect.x에 이값을 바로 집어넣으면 소숫점 버림 - lose data
        #x,y방향 collision check 따로해서 대각선으로 벽에 부딪힐경우 충돌안한 축방향으로는 계속 slide해서 가도록
        self.hit_rect.centerx = self.pos.x
        collide_with_group(self,self.game.walls,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_group(self,self.game.walls,'y')
        self.rect.center = self.hit_rect.center
     
    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH
        
        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        super().__init__(self.groups)
        self.game = game
        self.image = self.game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class Obstacle(pg.sprite.Sprite): #invisible object(이미지 없이 충돌만 하는 용도)
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        super().__init__(self.groups)
        self.game = game
        self.rect = pg.Rect(x,y,w,h)
        self.x = x
        self.y = y

        
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        super().__init__(self.groups)
        self.game = game
        self.image = self.game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = MOB_HIT_RECT.copy() #rect는 mutable object여서 한놈이 바꾸면 다른놈꺼도 바뀜. copy해야.
        self.pos = vec(x,y)
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rot = 0
        self.health = MOB_HEALTH
        self.target = game.player
    
    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()
    
    def update(self):
        if (self.target.pos - self.pos).length_squared() < DETECT_RADIUS**2: #루트는 시간오래걸리므로 제곱해서비교
        #player 방향으로 rotate(항상 player를 바라보도록)
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
            self.image = pg.transform.rotate(self.game.mob_img,self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos        
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(random.choice(MOB_ACC))
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
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        super().__init__(self.groups)
        self.game = game
        self.image = self.game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos) #vec붙이는이유: copy만들기. 안하면 player pos을 수정해버림
        self.rect.center = self.pos
        self.vel = dir * WEAPONS[self.game.player.weapon]['bullet_speed']
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage
        
    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self,self.game.walls): #spritecollide보다 기능 적지만 빠름
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()
    
class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        size = random.randint(20,50)
        self.image = pg.transform.scale(random.choice(game.gun_flashes),(size,size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()
        
    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()
        
        
        
class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEM_LAYER
        self.groups = game.all_sprites, game.items
        super().__init__(self.groups)
        self.game = game
        self.type = type
        self.image = game.item_images[type]
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hit_rect = self.rect
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1
        
        
    def update(self):
        # 제자리에서 흔들흔들(tweening, bobbing)
        # tweening function 응용하면 화면이나 색 자연스럽게 변하는것 등 구현 가능
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1
        
        
        
        

        
        