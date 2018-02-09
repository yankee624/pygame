# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import pygame as pg
import random
from os import path
import importlib

import settings
importlib.reload(settings)
from settings import *

import sprites
importlib.reload(sprites)
from sprites import *

vec = pg.math.Vector2

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init() 
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.game_over = False
        self.score1 = 0
        self.score2 = 0
    
        #load image
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir,'img')
        self.player1_img = pg.image.load(path.join(img_dir,'p1.png')).convert()
        self.player2_img = pg.image.load(path.join(img_dir,'p2.png')).convert()
        self.ball_img = pg.image.load(path.join(img_dir,'ball.png')).convert()
        self.bg_img = pg.transform.scale(pg.image.load(path.join(img_dir,'bg.png')).convert(), (WIDTH,HEIGHT))
        self.goal1_img = pg.transform.scale(pg.image.load(path.join(img_dir,'goal1.png')).convert(), (50,NET))
        self.goal1_img.set_colorkey(BLACK)
        self.goal2_img = pg.transform.scale(pg.image.load(path.join(img_dir,'goal2.png')).convert(), (50,NET))
        self.goal2_img.set_colorkey(BLACK)
        self.superspeed_img = pg.transform.scale(pg.image.load(path.join(img_dir,'superspeed.png')).convert(), (40,40))
        self.superjump_img = pg.transform.scale(pg.image.load(path.join(img_dir,'superjump.png')).convert(), (40,40))
        self.freeze_img = pg.transform.scale(pg.image.load(path.join(img_dir,'freeze.png')).convert(), (40,40))

    def new_game(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.player1 = Player(self,50,self.player1_img)
        self.player2 = Player(self,WIDTH-50,self.player2_img)
        self.ball = Ball(self)


    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update        
        self.all_sprites.update()
        
        #spawn item
        now = pg.time.get_ticks()
        if now - Item.last_spawn > Item.spawn_time:
            Item.last_spawn = now
            Item.spawn_time = random.choice([5000])
            Item(self,random.randrange(WIDTH/2-100,WIDTH/2+100),random.randrange(HEIGHT-50,HEIGHT-10))
        
        #player - player collision
        if pg.sprite.collide_rect(self.player1,self.player2):
        #self.player1.vel, self.player2.vel = self.player2.vel, self.player1.vel
            direction = vec(self.player2.rect.center) - vec(self.player1.rect.center)           
            power = (vec.length(self.player2.vel) + vec.length(self.player1.vel)) * 0.5      
            try:
                self.player1.vel = vec.normalize(-direction) * (power)
            except:
                self.player1.vel = vec(0,0)
            try:
                self.player2.vel = vec.normalize(direction) * (power)
            except:
                self.player2.vel = vec(0,0)

        
        
        
        #ball - item collide (공 마지막으로 찬 사람한테 효과 적용)
        hits = pg.sprite.spritecollide(self.ball,self.items,True)
        for hit in hits:
            player = self.ball.collide
            other = self.ball.not_collide
            if player == None:
                break
            
            if hit.type == 'superspeed':
                player.run = 5
                player.superspeed = True
                player.superspeed_timer = pg.time.get_ticks()
            
            if hit.type == 'superjump':
                player.jump_height = 20
                player.superjump = True
                player.superjump_timer = pg.time.get_ticks()
                
            if hit.type == 'freeze':
                other.run = 0
                other.freeze = True
                other.freeze_timer = pg.time.get_ticks()
                
        # 일정 시간 후 아이템 효과 사라짐        
        for player in self.players:
            if player.superspeed and now - player.superspeed_timer > 5000:
                player.run = 1.2
                player.superspeed = False
            if player.superjump and now - player.superjump_timer > 5000:
                player.jump_height = 15
                player.superjump = False
            if player.freeze and now - player.freeze_timer > 5000:
                player.run = 1.2
                player.freeze = False
        
        #player1 - ball collision
        if pg.sprite.collide_rect(self.player1,self.ball):
            #마지막으로 공 찬 사람 저장. 아이템 먹을 때 이 정보 이용
            self.ball.collide = self.player1
            self.ball.not_collide = self.player2
            direction = vec(self.ball.rect.center) - vec(self.player1.rect.center)           
            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]: #shooting
                power = (vec.length(self.player1.vel) + vec.length(self.ball.vel)) *1.5
            elif keys[pg.K_b]: #trapping
                power = (vec.length(self.player1.vel) + vec.length(self.ball.vel)) *0.2
                direction.y = 0
            else:
                power = (vec.length(self.player1.vel) + vec.length(self.ball.vel)) *0.8
            
            try:
                self.ball.vel = vec.normalize(direction) * (power)
            except:
                self.ball.vel.y -= 15 #player와 ball이 완전 겹치면 위로 튀어오름
        
        #player2 - ball collision
        if pg.sprite.collide_rect(self.player2,self.ball):
            #마지막으로 공 찬 사람 저장. 아이템 먹을 때 이 정보 이용
            self.ball.collide = self.player2
            self.ball.not_collide = self.player1
            direction = vec(self.ball.rect.center) - vec(self.player2.rect.center)           
            keys = pg.key.get_pressed()
            if keys[pg.K_o]: #shooting
                power = (vec.length(self.player2.vel) + vec.length(self.ball.vel)) *1.5
            elif keys[pg.K_p]: #trapping
                power = (vec.length(self.player2.vel) + vec.length(self.ball.vel)) *0.2
                direction.y = 0
            else:
                power = (vec.length(self.player2.vel) + vec.length(self.ball.vel)) *0.8
            
            try:
                self.ball.vel = vec.normalize(direction) * (power)
            except:
                self.ball.vel.y -= 15    
            
        
        #골
        if self.ball.rect.right >= WIDTH and self.ball.rect.top >= HEIGHT - NET:
            self.score1 += 1
            self.playing = False
        if self.ball.rect.left <= 0 and self.ball.rect.top >= HEIGHT - NET:
            self.score2 += 1
            self.playing = False
        
        #게임 끝
        if self.score1 >= 5 or self.score2 >= 5:
            self.game_over = True
        
    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.playing = False
                self.game_over = True
                self.running = False
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    self.player1.go_left()
                if event.key == pg.K_d:
                    self.player1.go_right()
                if event.key ==pg.K_s:
                    self.player1.go_down()
                if event.key == pg.K_w:
                    self.player1.jump()
                
                if event.key == pg.K_LEFT:
                    self.player2.go_left()
                if event.key == pg.K_RIGHT:
                    self.player2.go_right()
                if event.key ==pg.K_DOWN:
                    self.player2.go_down()
                if event.key == pg.K_UP:
                    self.player2.jump()
                           
            if event.type == pg.KEYUP:
                if event.key == pg.K_a and self.player1.acc.x < 0:
                    self.player1.stop()
                if event.key == pg.K_d and self.player1.acc.x > 0:
                    self.player1.stop()
                
                if event.key == pg.K_LEFT and self.player2.acc.x < 0:
                    self.player2.stop()
                if event.key == pg.K_RIGHT and self.player2.acc.x > 0:
                    self.player2.stop()

    def draw(self):
        # Game Loop - draw
        self.screen.blit(self.bg_img,[0,0])
        self.screen.blit(self.goal1_img,[0,HEIGHT - NET])
        self.screen.blit(self.goal2_img,[WIDTH - 50,HEIGHT - NET])
        self.draw_text(str(self.score1),50,WHITE,40,20)
        self.draw_text(str(self.score2),50,WHITE,WIDTH-40,20)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.blit(self.bg_img,[0,0])
        self.draw_text('BIG HEAD SOCCER',60,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text('Arrow keys to move',30,WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text('Press enter to start',20,WHITE,WIDTH/2,HEIGHT*3/4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        if not self.running:
            return
        self.score1 = 0
        self.score2 = 0
        self.screen.blit(self.bg_img,[0,0])
        self.draw_text('BIG HEAD SOCCER',60,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text('Arrow keys to move',30,WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text('Press enter to play again',20,WHITE,WIDTH/2,HEIGHT*3/4)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP and event.key == pg.K_RETURN:
                    waiting = False
                    self.game_over = False

    def next_game_load(self):
        pg.time.wait(500)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.SysFont('arial',size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface,text_rect)


g = Game()
g.show_start_screen()
while g.running:
    while not g.game_over:
        g.new_game()
        g.run()
        g.next_game_load()
    g.show_go_screen()

pg.quit()