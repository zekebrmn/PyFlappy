import pygame as pg
from settings import *

def draw_text(screen, text, size, color, x, y):
    font = pg.font.Font(FONT, size)
    text_surf = font.render(text,True,color)
    text_rect = text_surf.get_rect()
    text_rect.midtop = (x,y)
    screen.blit(text_surf, text_rect)

class button(object):
    def __init__(self,x,y,text,screen):
        self.x = x
        self.y = y
        self.text = text
        self.screen = screen
        self.clr = WHITE
        self.surf=pg.Surface((WIDTH/3,HEIGHT/10))
        self.rect=self.surf.get_rect() 
        self.draw()
    
    def draw(self):
        self.surf.fill(self.clr)
        self.rect.center=(self.x, self.y)
        self.screen.blit(self.surf, self.rect)
        draw_text(self.screen, self.text, 18, BLACK, self.rect.centerx, self.rect.centery - 9)   

    def mouseover(self,pos):
        if pos[0] > self.x and pos[0] < self.x + (WIDTH/3):
            if pos[1] > self.y and pos[1] < self.y + (HEIGHT/3):
                return True
        
        return False