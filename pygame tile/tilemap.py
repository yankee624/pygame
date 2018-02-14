# -*- coding: utf-8 -*-

import pygame as pg
from settings import *



class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename,'rt') as f:
            for line in f:
                self.data.append(line.strip())
         
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        
        
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def update(self, target):
        #이 x,y만큼 모든 sprite을 평행이동시켜서 screen에는 map의 특정부분이 보이도록 함
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)
        
        #limit scrolling to map size
        x = min(0,x) #left - 0보다 작게
        x = max(-(self.width - WIDTH),x) #right - 저 값보단 크게
        y = min(0,y)
        y = max(-(self.height - HEIGHT),y)
        self.camera = pg.Rect(x,y,self.width,self.height)