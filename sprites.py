import pygame as pg
from settings import *
import random
vec = pg.math.Vector2
FRIC=-0.12
HEIGHT=525
WIDTH=340

class Player(pg.sprite.Sprite):
    def __init__(self, app):
        super().__init__()
        self.app = app
        if app.character is None:
            self.surf = pg.Surface((32, 32))
            self.surf.fill(BLACK)
        else :
            self.surf = pg.image.load('./img/' + app.character_root[app.character])
        self.rect=self.surf.get_rect()
        self.rect.center=(85,185)

        self.pos = vec((85,185))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def flap(self):
        self.vel.y = -4

    def move(self):
        self.acc = vec(0,0.19)

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.center = self.pos

class floor(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pg.Surface((WIDTH,100))
        self.surf.fill((107,64,40))
        self.rect=self.surf.get_rect()
        self.rect.center=((WIDTH/2,HEIGHT-10))

class pipe_bottom(pg.sprite.Sprite):
    def __init__(self,len,start,top_pipe):
        super().__init__()
        self.length = int(len)
        self.start = int(start)
        self.top_pipe = top_pipe
        self.surf=pg.Surface((35,self.length))
        self.surf.fill((255,255,255))
        #self.surf = pg.image.load("./img/pipe_bottom.png")
        self.scored=False
        self.rect=self.surf.get_rect()
        self.rect.center=(self.start,HEIGHT-(self.length/2))
    
    def move(self):
        self.rect.centerx -= 2

    def move_y(self):
        if self.top_pipe.moving_up:
            self.rect.centery -= 1
        elif self.top_pipe.moving_up == False:
            self.rect.centery += 1



class pipe_top(pg.sprite.Sprite):
    def __init__(self,len,start):
        super().__init__()
        self.length = int(len)
        self.start = int(start)
        self.surf=pg.Surface((35,self.length))
        self.surf.fill((255,255,255))
        self.moving_up = random.choice([True,False])
        #self.surf = pg.image.load("./img/pipe_top.png")
        self.rect=self.surf.get_rect()
        self.rect.center=(self.start,self.length/2)

    def move(self):
        self.rect.centerx -= 2
    
    def move_y(self):
        if self.moving_up:
            self.rect.centery -= 1
        elif self.moving_up == False:
            self.rect.centery += 1
        
        if self.rect.centery <= 50:
            self.moving_up = False
        elif self.rect.centery >= 200:
            self.moving_up = True
        