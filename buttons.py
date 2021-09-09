import pygame as pg
from settings import *
from util import *

class button(pg.sprite.Sprite):
    def __init__(self,x,y,text,screen,clr,cngclr):
        super().__init__()
        self.x = x
        self.y = y
        self.text = text
        self.screen = screen
        self.curclr = clr
        self.clr = clr
        self.cngclr = cngclr
        self.surf=pg.Surface((WIDTH/3,HEIGHT/10))
        self.rect=self.surf.get_rect() 
        self.rect.center=(self.x, self.y)
        self.draw()
    
    def draw(self):
        self.surf.fill(self.curclr)
        self.screen.blit(self.surf, self.rect)
        if self.text is not None:
            draw_text(self.screen, self.text, 18, BLACK, self.rect.centerx, self.rect.centery - 9)   

    #self.x - WIDTH
    def mouseover(self,pos):
        if pos[0] > self.x - (WIDTH/6) and pos[0] < self.x + (WIDTH/6):
            if pos[1] > self.y - (HEIGHT/20) and pos[1] < self.y + (HEIGHT/20):
                return True
        
        return False


class sizable_button(pg.sprite.Sprite):
    def __init__(self,x,y,text,screen,width,height,font_size,text_padding, clr, cngclr):
        super().__init__()
        self.x = x
        self.y = y
        self.text = text
        self.screen = screen
        self.curclr = clr
        self.clr = clr
        self.cngclr = cngclr
        self.size = font_size
        self.width = width
        self.height = height
        self.padding = text_padding
        self.surf=pg.Surface((self.width,self.height))
        self.rect=self.surf.get_rect()
        self.rect.center=(self.x,self.y)
        self.type = 'Menu'
        self.draw()

    def draw(self):
        self.surf.fill(self.curclr)
        self.screen.blit(self.surf,self.rect)
        if self.text is not None:
            draw_text(self.screen, self.text, self.size, BLACK, self.rect.centerx, self.rect.centery - self.padding)
    
    def mouseover(self,pos):
        if pos[0] > self.x - (self.width/2) and pos[0] < self.x + (self.width/2):
            if pos[1] > self.y - (self.height/2) and pos[1] < self.y + (self.height/2):
                return True
        
        return False