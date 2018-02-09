import pygame as pg
import random
from os import path
#reloading module(이렇게 해야 setting 수정했을때 바로 반영)
#안해주면 수정할때마다 console창 껐다켰다 해야 수정사항 반영
import importlib
import settings
importlib.reload(settings)
from settings import *

import sprites
importlib.reload(sprites)
from sprites import *


class Game:
    def __init__(self):
        #initialize game window, clock, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = 'arial'
        self.load_data()
        
    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir,'img')        
        #load high score
        #with 구문 쓰면 file close 알아서 해줌
        with open(path.join(self.dir,HS_FILE),'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                #내용 아무것도 없으면 int변환 불가능
                self.highscore = 0
        
        #load images(spritesheet, cloud)
        self.spritesheet = Spritesheet(path.join(img_dir,SPRITESHEET))
        self.cloud_images = []
        for i in range(1,4):
            self.cloud_images.append(pg.image.load(path.join(img_dir,'cloud{}.png'.format(i))).convert())
        #load sounds
        self.snd_dir = path.join(self.dir,'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir,'jump.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir,'boost.wav'))
        
    def new(self):
        #start a new game and run
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates() #물체들 겹칠때 뭐를 위에 그릴지 정할수잇음
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self,*plat)
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500
        self.mob_timer = 0

        
    def run(self):
        #game loop
        pg.mixer.music.load(path.join(self.snd_dir,'playing.ogg'))
        pg.mixer.music.play(loops=-1)
        
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw() 
        
        pg.mixer.music.fadeout(1000)
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
           
    def update(self):
        self.all_sprites.update()
        #spawn mob
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000,-500,0,500,1000]):
            self.mob_timer = now
            Mob(self)
            
        #mob collide 확인
        mob_hits = pg.sprite.spritecollide(self.player,self.mobs,False)
        if mob_hits: #항상 mask collision 체크하면 너무 시간오래걸림 - 평소엔 AABB collision
                     #하다가 거기서 collide하면 mask collision 체크
            mob_hits = mob_hits = pg.sprite.spritecollide(self.player,self.mobs,False,pg.sprite.collide_mask)
            if mob_hits:
                self.playing = False
        
        #platform collide 확인
        if self.player.vel.y > 0: #밑으로 떨어지는 중에만(이 조건 없으면 위로 순간이동함)
            hits = pg.sprite.spritecollide(self.player,self.platforms,False)
            if hits:
                #여러 platform 동시 충돌시 가장 낮은 놈하고만 충돌하도록
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                #player발 중앙이 platform 양쪽끝 사이에 있고,
                #player 발이 platform보다 위에 있을때만 충돌
                if self.player.pos.x < lowest.rect.right + 10 and \
                   self.player.pos.x > lowest.rect.left - 10 and \
                   self.player.pos.y < lowest.rect.centery:           
                    self.player.pos.y = lowest.rect.top
                    #실제 이미지는 rect에 그려지므로 draw하기전에 rect도 바꿔줘야 함
                    self.player.rect.midbottom = self.player.pos
                    #vel 0으로 안해주면 vel이 무한히 증가(가속도는 계속 0.5이므로)
                    self.player.vel.y = 0
                    self.player.jumping = False
            
        
        #powerup collide 확인
        pow_hits = pg.sprite.spritecollide(self.player,self.powerups,True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y -= BOOST
                #점프하면서 powerup먹었을때 space에서 손떼는순간 jumpcut 되면서
                #boost 씹히는 것 방지
                self.player.jumping = False
            
        #player가 화면높이 4분의1 지나면 카메라 위로(즉,물체들을 밑으로) 
        if self.player.rect.top < HEIGHT / 4:
            #player 속도와 같은 속도로 물체들이 내려가야 자연스럽게 화면 움직임
            #int 안해주면 player pos은 바뀌는데 plat rect는 소숫점때매 안바뀌어서 이상해질수있음
            self.player.pos.y += int(abs(self.player.vel.y)) +2
            self.player.rect.midbottom = self.player.pos
            
            if random.randrange(100) < 15:
                Cloud(self)
            for cloud in self.clouds:
                cloud.rect.y += int(abs(self.player.vel.y)/2) + 2 #구름은 좀 느리게 가도록
            for mob in self.mobs:
                mob.rect.y += int(abs(self.player.vel.y)) +2
            for plat in self.platforms:
                plat.rect.y += int(abs(self.player.vel.y)) +2
                if plat.rect.top > HEIGHT:
                    plat.kill()
                    self.score += 10
        

             
        #떨어지면 모든 spirte 위로. platform 다없어지면 게임 끝
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(10,self.player.vel.y)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
        
        
        #platform kill한만큼 새로운 platform 생성
        while len(self.platforms) < 6:
            Platform(self,random.randrange(0,WIDTH-100),
                     random.randrange(-80,-30))
        
    def draw(self):
        self.screen.fill(SKY)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score),20,WHITE,WIDTH/2,15)
        
        pg.display.flip()
        
    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir,'menu.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(SKY)
        self.draw_text('Jump..',60,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text('Arrow keys to move, space to jump',30,WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text('Press any key to start',20,WHITE,WIDTH/2,HEIGHT*3/4)
        self.draw_text('High score: {}'.format(self.highscore),20,WHITE,WIDTH/2,15) 
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(1000)
        
    def show_go_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir,'menu.ogg'))
        pg.mixer.music.play(loops=-1)
        
        #이거 안하면 x 눌러도 바로 안나가지고 게임오버 화면 나옴
        if not self.running:
            return
        self.screen.fill(SKY)
        self.draw_text('GAME OVER',60,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text('Score: {}'.format(self.score),30,WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text('Press any key to play again',20,WHITE,WIDTH/2,HEIGHT*3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text('New High Score!',30,WHITE,WIDTH/2,HEIGHT/2+40)
            with open(path.join(self.dir,HS_FILE),'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text('High score: {}'.format(self.highscore),30,WHITE,WIDTH/2,HEIGHT/2+40)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(1000)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.SysFont(self.font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface,text_rect)

    
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_go_screen()
    
pg.quit()


