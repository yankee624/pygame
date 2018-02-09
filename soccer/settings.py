# -*- coding: utf-8 -*-

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
TITLE = 'Big head soccer'
WIDTH = 800
HEIGHT = 600
FPS = 50


#game properties
PLAYER_ACC = 1.2
PLAYER_JUMP = 15
PLAYER_FRICTION = -0.15

BALL_FRICTION = -0.1
BALL_AIR_RESIST = -0.02
GRAV = 1

NET = 95