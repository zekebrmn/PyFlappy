import pygame as pg
from settings import *
from util import *
from buttons import *

class Menu(object):
    def __init__(self, title, screen, app):
        self.title = title
        self.screen = screen
        self.app = app
        self.buttons = []
        self.back_button = sizable_button(50,22,'Back',self.screen,80,25,16,6, WHITE, GRAY)
        self.buttons.append(self.back_button)
        self.button_group = pg.sprite.Group()
        self.button_group.add(self.back_button)
        self.draw()

    def draw(self):
        self.screen.fill(BACKGROUND)
        draw_text(self.screen, self.title, 32, WHITE, WIDTH/2, HEIGHT/10)
        pg.display.flip()