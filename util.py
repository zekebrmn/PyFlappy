from typing import List
import pygame as pg
from pygame.scrap import get
from settings import *
import os, sys

def sort_key(scores):
    return int(scores[1])

def get_scoreboard():
    list = []
    file = open('./strg/scores.txt', 'r')
    i = 0
    for line in file:
        strip = line.strip()
        score = strip.split()
        list.append(score)
        i += 1
    list.sort(key=sort_key, reverse=True)
    return list

def write_scoreboard(name, score):
    name = str(name)
    score = str(score)
    file = open('./strg/scores.txt', 'a')
    file.write('%s %s\n' % (name, score))
    file.close()

def draw_text(screen, text, size, color, x, y):
    font = pg.font.Font(FONT, size)
    text_surf = font.render(text,True,color)
    text_rect = text_surf.get_rect()
    text_rect.midtop = (x,y)
    screen.blit(text_surf, text_rect)

def draw_menu_buttons(list, sprite_group):
    for b in list:
        b.draw()
        sprite_group.update()
        pg.display.flip()

def draw_menu_buttons_clr(list, sprite_group, color):
    for b in list:
        b.curclr = color
        b.draw()
        sprite_group.update()
        pg.display.flip()

def button_hover(list, sprite_group, pos):
    for b in list:
        if b.mouseover(pos):
            b.curclr = b.cngclr
            b.draw()
            sprite_group.update()
            pg.display.flip()
        else:
            b.curclr = b.clr
            b.draw()
            sprite_group.update()
            pg.display.flip()

def char(input, list):
    input = int(input)
    return list[input]

class grid():
    def __init__(self, screen, list, menu, app):
        self.screen = screen
        self.list = list
        self.menu = menu
        self.app = app
        self.x = 70
        self.y = 150
        self.width = 64
        self.height = 64
        self.draw_grid()
    
    def draw_grid(self):
        for i in range(len(self.list)):
            if i % 3 == 0 and i > 2:
                self.y += 100
                self.x = 70
            grid_button = self._subclass_container(None,0,0,TILE,TILE_HOVER, i)
            self.menu.button_group.add(grid_button)
            self.menu.buttons.append(grid_button)
            #surf = pg.Surface((width,height))
            #lock = pg.image.load("./img/lock.png")
            #rect = surf.get_rect()
            #surf.fill(TILE)
            #rect.center=(x,y)
            draw_text(self.screen, self.list[i],16,WHITE,self.x,self.y+35)
            #screen.blit(surf,rect)
            #screen.blit(lock,rect)
            self.x+=100
            
    
    def _subclass_container(self,text,font_size,text_padding,clr,cngclr,slot):
        _parent_class = self
        class grid_button(pg.sprite.Sprite):
            def __init__(self):
                super().__init__()
                self.text = text
                self.screen = _parent_class.screen
                self.curclr = clr
                self.clr = clr
                self.cngclr = cngclr
                self.size = font_size
                self.padding = text_padding
                self.type = 'Grid'
                self.slot = slot
                self.width=_parent_class.width
                self.height=_parent_class.height
                self.x = _parent_class.x
                self.y = _parent_class.y
                self.surf = pg.Surface((self.width,self.height))
                self.rect = self.surf.get_rect()
                self.rect.center = (self.x,self.y)
                self.draw()
            
            def draw(self):
                self.surf.fill(self.curclr)
                self.screen.blit(self.surf,self.rect)
                if self.text is not None:
                    draw_text(self.screen, self.text, self.size, BLACK, self.rect.centerx, self.rect.centery - self.padding)
                self.draw_icon()
            
            def draw_icon(self):
                icon = _parent_class.app.character_list[self.slot]
                self.icon_surf = pg.image.load('./img/' + _parent_class.app.character_root[icon])
                self.icon_rect = self.icon_surf.get_rect()
                self.icon_rect.center = (self.x, self.y)
                self.screen.blit(self.icon_surf, self.icon_rect)
                
            
            def callback(self):
                _parent_class.app.character = char(self.slot, _parent_class.list)
                print(_parent_class.app.character)
                print(_parent_class.app.character_root[_parent_class.app.character])
    
            def mouseover(self,pos):
                if pos[0] > self.x - (self.width/2) and pos[0] < self.x + (self.width/2):
                    if pos[1] > self.y - (self.height/2) and pos[1] < self.y + (self.height/2):
                        return True
        
                return False
            
        return grid_button()

def draw_scoreboard(screen):
    y = 100
    width = 292
    height = 32
    scoreboard = get_scoreboard()
    for i in range(len(scoreboard)):
        if i <= 9:
            y += 37
            surf = pg.Surface((width,height))
            rect = surf.get_rect()
            surf.fill(TILE)
            rect.center=(WIDTH/2, y)
            screen.blit(surf,rect)
            if scoreboard[i] is not None:
                score = scoreboard[i]
                draw_text(screen, score[0], 18, WHITE, WIDTH/2 - 60, y-8)
                draw_text(screen, score[1], 18, WHITE, WIDTH/2 + 60, y-8)
        else:
            break