# -*- coding: utf-8 -*-
import pygame as pg
import random
from os import path
import sys

#import importlib
#import settings
#importlib.reload(settings)  - reload해줘야 수정사항 바로 반영되는줄알았는데 갑자기 안해도 되네
from settings import *

#import sprites
#importlib.reload(sprites)
from sprites import *

from tilemap import *


#HUD(Heads Up Display) functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    if pct > 0.6:
        col = GREEN
    elif pct> 0.3:
        col = YELLOW
    else:
        col = RED
    
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pg.Rect(x,y,fill,BAR_HEIGHT)
    pg.draw.rect(surf,WHITE,outline_rect,2)
    pg.draw.rect(surf,col,fill_rect)


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder,'img')
        self.player_img = pg.image.load(path.join(img_folder,PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder,BULLET_IMG)).convert_alpha()      
        self.wall_img = pg.image.load(path.join(img_folder,WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img,(TILESIZE,TILESIZE))
        self.mob_img = pg.image.load(path.join(img_folder,MOB_IMG)).convert_alpha()
        self.map = Map(path.join(game_folder,'map3.txt'))         

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data): #enumerate: index와 value 동시에
            for col, tile in enumerate(tiles):
                if tile == 'P':
                    self.player = Player(self,col,row)
                if tile == '1':
                    Wall(self,col,row)
                if tile == 'M':
                    Mob(self,col,row)


        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        #mobs player collision
        hits = pg.sprite.spritecollide(self.player,self.mobs,False,collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK,0).rotate(-hits[0].rot) #넉백
        
        #bullets mobs collision
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0,0) #총 맞으면 멈칫

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))


    def draw(self):       
        pg.display.set_caption('{:.2f}'.format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite,Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #player의 rect와 hit_rect(충돌 검사용 rect) 보고싶으면 아래 코드..
        #pg.draw.rect(self.screen,RED,self.camera.apply(self.player),2)
        #pg.draw.rect(self.screen,WHITE,self.player.hit_rect,2)
        
        #HUD functions
        draw_player_health(self.screen,10,10,self.player.health/PLAYER_HEALTH)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()


    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def quit(self):
        pg.quit()
        sys.exit()
    
# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()