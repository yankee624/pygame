# -*- coding: utf-8 -*-
import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0 ,0, 255)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tile"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'wall.png'

#player settings
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
PLAYER_IMG = 'manBlue_gun.png'
BARREL_OFFSET = vec(30,10) #총 위치가 player의 center에서 얼마나 떨어져있는지 설정
#총알을 player의 center가 아니라 거기서 나가도록
PLAYER_HEALTH = 100

#bullet settings
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
KICKBACK = 200 #쐈을때 밀려나기
GUN_SPREAD = 5 #약간의 부정확성
BULLET_DAMAGE = 10

#mob settings
MOB_IMG = 'zombie_hold.png'
MOB_ACC = 150
MOB_HIT_RECT = pg.Rect(0,0,30,30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20