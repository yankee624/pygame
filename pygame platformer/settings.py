import pygame
import random

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
SKY = (102,204,255)

#game options, settings
TITLE = 'Platformer'
WIDTH = 480
HEIGHT = 600
FPS = 20
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

#player properties
PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.35
PLAYER_GRAV = 0.7
PLAYER_JUMP = 20

#Game properties
BOOST = 50
POW_SPAWN_PCT = 10
PLAYER_LAYER = 2
MOB_LAYER = 2
POW_LAYER = 1
PLATFORM_LAYER = 1
CLOUD_LAYER = 0


#starting platforms
PLATFORM_LIST = [(0,HEIGHT - 40),
                 (WIDTH / 2,HEIGHT * 3/4),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]