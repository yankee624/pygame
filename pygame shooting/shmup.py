# -*- coding: utf-8 -*-

import pygame
import random
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 600
FPS = 50

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,'img')
snd_folder = os.path.join(game_folder,'snd')

def draw_text(surf,text,size,x,y):
    font = pygame.font.Font('C:/Windows/Fonts/arialbd.ttf',size)
    text_surf = font.render(text,True,WHITE)
    text_rect = text_surf.get_rect()
    text_rect.center = (x,y)
    surf.blit(text_surf,text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield(surf, x, y, percent):
    if percent < 0:
        percent = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percent / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,WHITE,outline_rect,2)
    pygame.draw.rect(surf,GREEN,fill_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #이미지 크기 조정 가능
        self.image = pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #radius를 설정하면 circular bounding collision 설정 가능
        self.radius = 20
        #아래는 radius 적절한지 테스트하기 위한 코드
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        #initial position
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.life = 3
        self.hidden = False
        self.hide_timer = 0
        self.power = 1
        self.power_timer = 0
        
    def update(self):
        #hide 한지 1000ms(1초) 지낫으면 초기 위치로.(unhide)
        if self.hidden and (pygame.time.get_ticks() - self.hide_timer) > 1000:
            player.unhide()

        #powerup 먹은지 5초 지났으면 power down
        if self.power >= 2 and pygame.time.get_ticks() - self.power_timer > 5000:
            player.power -= 1
            
        
        self.rect.x += self.speedx
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        #spacebar 누르고 있으면 계속 shoot      
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            self.shoot()
    
    def powerup(self):
        self.power += 1
        self.power_timer = pygame.time.get_ticks()
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left,self.rect.top)
                bullet2 = Bullet(self.rect.right,self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
    
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        #안보이는곳으로 이동해서 숨김
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT + 200)
    
    def unhide(self):
        self.hidden = False
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.orig_image = pygame.transform.scale(mob_img,random.choice(mob_scale))
        self.orig_image.set_colorkey(BLACK)
        self.image = self.orig_image.copy()
        self.rect = self.image.get_rect()
        #radius를 설정하면 circular bounding collision 설정 가능
        self.radius = int(self.rect.width*0.85 / 2)
        #아래는 radius 적절한지 테스트하기 위한 코드
        #pygame.draw.circle(self.image,WHITE,self.rect.center,self.radius)
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-50)
        self.speedx = random.randrange(-3,3)
        self.speedy = random.randrange(1,8)
        
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
        
        
    def rotate(self):
        now = pygame.time.get_ticks()
        #50milisecond 지날때마다 회전(매 프레임 회전하기는 힘듦)
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            #orig_image 만든 이유:rotate할때마다 lose some pixels
            #따라서 img하나로 계속 rotate하면 점점 이미지가 없어짐
            new_img = pygame.transform.rotate(self.orig_image,self.rot)
            #같은 중심에 대해 회전하도록.
            old_center = self.rect.center
            self.image = new_img
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    
    
    
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT + 10 or self.rect.left < -10 or self.rect.right > SCREEN_WIDTH + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-50)
            self.speedy = random.randrange(1,8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        #맨 위까지 가면 삭제
        if self.rect.bottom < 0 :
            self.kill()

class Powerup(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.type = random.choice(['gun','shield'])
        self.image = powerup_img[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = 3
        
    def update(self):
        self.rect.y += self.speedy
        #맨 위까지 가면 삭제
        if self.rect.bottom < 0 :
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        super().__init__()
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                self.image = explosion_anim[self.size][self.frame]
            
def show_go_screen():
    screen.blit(background,background_rect)
    draw_text(screen,"Shoot them up!",60,SCREEN_WIDTH / 2 ,SCREEN_HEIGHT / 4)
    draw_text(screen,"arrow keys to move, space to shoot",20,
              SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    draw_text(screen,"Press any key to start",15,
              SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

#initialize game and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Shooting them up!')
clock = pygame.time.Clock()

#load image
background = pygame.image.load(os.path.join(img_folder,'space.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_folder,'ship.png')).convert()
mob_img = pygame.image.load(os.path.join(img_folder,'meteor.png')).convert()
mob_scale = [(15,15),(40,30),(50,50),(70,80),(100,100)]
bullet_img = pygame.image.load(os.path.join(img_folder,'missile.png')).convert()

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(3):
    filename = 'explosion{}.png'.format(i)
    image = pygame.image.load(os.path.join(img_folder,filename)).convert()
    image.set_colorkey(BLACK)
    image_lg = pygame.transform.scale(image,[70,70])
    explosion_anim['lg'].append(image_lg)
    image_sm = pygame.transform.scale(image,[25,25])
    explosion_anim['sm'].append(image_sm)
for i in range(9):
    filename = 'sonicExplosion0{}.png'.format(i)
    image = pygame.image.load(os.path.join(img_folder,filename)).convert()
    image.set_colorkey(BLACK)
    explosion_anim['player'].append(image)

powerup_img = {}
powerup_img['gun'] = pygame.image.load(os.path.join(img_folder,'gun_powerup.png')).convert()
powerup_img['shield'] = pygame.image.load(os.path.join(img_folder,'shield_powerup.png')).convert()


#load sound
shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder,'laser.ogg'))
pygame.mixer.music.load(os.path.join(snd_folder,'background.ogg'))
pygame.mixer.music.set_volume(0.4)




done = False
game_over = True


#노래 끝날때마다 영원히 반복, 자연수 쓰면 그 숫자만큼 반복
pygame.mixer.music.play(loops=-1)

while not done:
    if game_over:
        show_go_screen()
        game_over = False

        #create sprite groups, sprites
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        
        player = Player()
        all_sprites.add(player)
        for i in range(10):
            newmob()
            
        score = 0
    
    clock.tick(FPS)
    #process events(input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speedx = -6
            if event.key == pygame.K_RIGHT:
                player.speedx = 6

            
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.speedx < 0:
                player.speedx = 0
            if event.key == pygame.K_RIGHT and player.speedx > 0:
                player.speedx = 0  

            
    #game logic(update)
    all_sprites.update()
    #mob이 bullet맞으면 서로 사라진 후, 사라진 mob 수만큼 새로운 mob 생성
    hits = pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        #작을수록 점수 크게
        score += 50 - hit.radius
        newmob()
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        #40프로 확률로 powerup 생성
        if random.random() > 0.6:
            powerup = Powerup(hit.rect.x,hit.rect.y)
            all_sprites.add(powerup)
            powerups.add(powerup)
            
    #player, mob 충돌시,shield 달고 mob 없어지고 새로운mob, circle collision
    hits = pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
    for hit in hits:
        newmob()
        expl = Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        player.shield -= hit.radius * 2
        if player.shield <= 0:
            death_explosion=Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.life -= 1
            player.shield = 100
     
    #plyaer가 powerup과 충돌 시...
    hits = pygame.sprite.spritecollide(player,powerups,True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += 30
            if player.shield > 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
    
    #player life 0이고, explosion animation 끝낫으면 게임 종료
    if player.life == 0 and not death_explosion.alive():
        game_over = True
        
    #draw
    screen.fill(WHITE)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(score),20,30,30)
    draw_shield(screen,5,5,player.shield)
    draw_text(screen,str(player.life),20,450,30)
    #update screen
    pygame.display.flip()
    

    
pygame.quit()
