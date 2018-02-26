# -*- coding: utf-8 -*-

import pygame as pg
import pytmx
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
        
    
class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha = True)
        #tmx파일을 editor로 열면 각종 설정 수정 가능(img source 같은거..)
        self.tmxdata = tm
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
    
    def make_map(self):
        temp_surf = pg.Surface((self.width,self.height))
        self.render(temp_surf)
        return temp_surf
    
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer,pytmx.TiledTileLayer):
                for x,y,gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))
    
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self,rect): #sprite가 아닌 것들 apply하는 용도
        return rect.move(self.camera.topleft)
    
    
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