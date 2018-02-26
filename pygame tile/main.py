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
        
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder,'img')
        self.map_folder = path.join(game_folder,'maps')
        self.title_font = path.join('img','ZOMBIE.TTF')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0,180)) # RGBA 이용. 마지막숫자(A) 커질수록 어둡
        
        self.player_img = pg.image.load(path.join(img_folder,PLAYER_IMG)).convert_alpha()
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder,BULLET_IMG)).convert_alpha()      
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'],(10,10))
#        self.wall_img = pg.image.load(path.join(img_folder,WALL_IMG)).convert_alpha()
#        self.wall_img = pg.transform.scale(self.wall_img,(TILESIZE,TILESIZE))
        self.mob_img = pg.image.load(path.join(img_folder,MOB_IMG)).convert_alpha()
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder,img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder,ITEM_IMAGES[item])).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder,'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()    
        
#        for row, tiles in enumerate(self.map.data): #enumerate: index와 value 동시에
#            for col, tile in enumerate(tiles):
#                if tile == 'P':
#                    self.player = Player(self,col,row)
#                if tile == '1':
#                    Wall(self,col,row)
#                if tile == 'M':
#                    Mob(self,col,row)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self,obj_center.x,obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self,tile_object.x,tile_object.y,
                         tile_object.width,tile_object.height)
            if tile_object.name == 'zombie':
                Mob(self,obj_center.x,obj_center.y)
            if tile_object.name in ['health','shotgun']:
                Item(self,obj_center,tile_object.name)
                
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False #hit box 표시하는 용도
        self.paused = False


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        
        #game over
        if len(self.mobs) == 0:
            self.playing = False
        
        #player item collision
        hits = pg.sprite.spritecollide(self.player,self.items,False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < 100:
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'shotgun':
                hit.kill()
                self.player.weapon = 'shotgun'
        
        #mobs player collision
        hits = pg.sprite.spritecollide(self.player,self.mobs,False,collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK,0).rotate(-hits[0].rot) #넉백
        
        #bullets mobs collision
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            for bullet in hits[mob]:
                mob.health -= bullet.damage       
            mob.vel = vec(0,0) #총 맞으면 멈칫

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))


    def draw(self):       
        pg.display.set_caption('{:.2f}'.format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        #self.draw_grid()
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        
        for sprite in self.all_sprites:
            if isinstance(sprite,Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen,BLUE,self.camera.apply_rect(sprite.hit_rect),1)
        
        if self.draw_debug:
            for wall in self.walls: #obstacle은 all_sprites에 포함 안되므로 따로해줌
                pg.draw.rect(self.screen,BLUE,self.camera.apply_rect(wall.rect),1)
        
        #player의 rect와 hit_rect(충돌 검사용 rect) 보고싶으면 아래 코드..
        #pg.draw.rect(self.screen,RED,self.camera.apply(self.player),2)
        #pg.draw.rect(self.screen,WHITE,self.player.hit_rect,2)
        
        if self.paused:
            self.screen.blit(self.dim_screen,(0,0))
            self.draw_text("Paused",self.title_font,105,RED,WIDTH/2,HEIGHT/2,'center')
        
        #HUD functions
        draw_player_health(self.screen,10,10,self.player.health/PLAYER_HEALTH)
        self.draw_text('Zombies - {}'.format(len(self.mobs)),self.title_font,30,WHITE,WIDTH-10,10,'ne')
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused


    def show_start_screen(self):
        pass

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED,
                       WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press a key to start", self.title_font, 75, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait() #첫 event나올때까지 기다리다가 첫event무시.(키 누르고있을때 게임오버됐는데 떼자마자 시작되는거 방지)
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

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