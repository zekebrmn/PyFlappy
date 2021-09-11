import pygame as pg
from sprites import *
from buttons import *
from settings import *
from menu import *
from util import *
import random

def pipeLength():
    return random.randint(50,300)

class App():
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        pg.font.init()
        self.font_path = './font/font.TTF'
        self.font_size = 44
        self.font_obj = pg.font.Font(self.font_path, self.font_size)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        #self.screen = pg.image.load("./img/background.png")
        pg.display.set_caption(TITLE + VERSION)
        self.clock = pg.time.Clock()
        self.running = True
        self.started = False
        self.pipes = False
        self.pipeListTop = pg.sprite.Group()
        self.pipeListBottom = pg.sprite.Group()
        self.score = 0
        self.label = self.font_obj.render(str(self.score), 1, (0,0,0))
        self.buttonlist=[]
        self.button_sprites = pg.sprite.Group()
        self.menu = False
        self.selected_menu = None
        self.character_list = ['Troll', 'Among Us', 'Bernard']
        self.character_root = {'Troll': 'default.png', 'Among Us': 'amongus.png', 'Bernard': 'bnard.png'}
        self.character = None
        for i in range(5):
            length = random.randint(50,300)
            self.pipeListTop.add(pipe_top(length,400 + (i * 165)))
            self.pipeListBottom.add(pipe_bottom((HEIGHT-length)-140,400 + (i*165)))

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.ground = floor()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.ground)
        if self.pipeListBottom.sprites()[0].rect.x < 340:
            self.score = 0
            self.label = self.font_obj.render(str(self.score), 1, (0,0,0))
            self.pipeListBottom.empty()
            self.pipeListTop.empty()

            for i in range(5):
                length = random.randint(50,300)
                self.pipeListTop.add(pipe_top(length,400 + (i*165)))
                self.pipeListBottom.add(pipe_bottom((HEIGHT-length)-140,400+(i*165)))
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            if self.started:
                self.player.move()
                if self.pipes:
                    for bottom_pipe in self.pipeListBottom:
                        bottom_pipe.move()
                        if bottom_pipe.rect.x <= -50:
                            bottom_pipe.kill()
                            pass
        
                    for top_pipe in self.pipeListTop:
                        top_pipe.move()
                        if top_pipe.rect.x <= -50:
                            top_pipe.kill()
                            pass
                    
                    while len(self.pipeListBottom) < 5:
                        length = random.randint(50,300)
                        self.pipeListTop.add(pipe_top(length,400 + ((len(self.pipeListBottom) - 1.6)  * 165)))
                        self.pipeListBottom.add(pipe_bottom((HEIGHT-length)-140,400 + ((len(self.pipeListBottom) - 1.6)*165)))
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.pipeListBottom.update()
        self.pipeListTop.update()
        hit_ground = pg.sprite.collide_rect(self.player, self.ground)
        hit_pipe = False

        #Pipe Collision
        for bottom_pipe in self.pipeListBottom:
            #if bottom_pipe.rect.x > 85:
            hit_pipe = pg.sprite.collide_rect(self.player, bottom_pipe)
            #hit_pipe = self.player.rect.colliderect(bottom_pipe.rect)
            if hit_pipe:
                break
            if bottom_pipe.rect.x == self.player.rect.x or bottom_pipe.rect.x == self.player.rect.x - 1:
                self.score += 1
                self.label = self.font_obj.render(str(self.score), 1, (0,0,0))
        
        for top_pipe in self.pipeListTop:
            if hit_pipe == False:
            #if top_pipe.rect.x > 85 and hit_pipe == False:
                hit_pipe = self.player.rect.colliderect(top_pipe.rect)
                #hit_pipe = pg.sprite.collide_rect(self.player, top_pipe)
                if hit_pipe:
                    break

        #End Cycle - Player loss
        if hit_pipe:
            self.pipes = False
            self.playing = False
            if self.score > 0:
                write_scoreboard('Undefined', self.score)
        if hit_ground:
            self.started = False
            self.playing = False
            if self.score > 0:
                write_scoreboard('Undefined', self.score)
        
    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.started==False:
                    self.started=True
                    self.pipes=True
                self.player.flap()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if self.started==False:
                        self.started=True
                        self.pipes=True
                    self.player.flap()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BACKGROUND)
        for pipe_bottom in self.pipeListBottom:
            self.screen.blit(pipe_bottom.surf, pipe_bottom.rect)
        for pipe_top in self.pipeListTop:
            self.screen.blit(pipe_top.surf, pipe_top.rect)
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)
        self.screen.blit(self.label, ((WIDTH/2)-15,55))
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BACKGROUND) 
        self.draw_text("PyFlappy", 32, WHITE, WIDTH/2,HEIGHT/4-40) # Draw text
        self.draw_text(VERSION, 18, WHITE, WIDTH/2,HEIGHT/4 -5)
        self.draw_text("Press any key to begin", 18, WHITE, WIDTH/2,HEIGHT * 3/4)
        character_button = button(WIDTH/2 - (WIDTH/4), 450, 'Character', self.screen, WHITE, GRAY) #Draw buttons and add to list
        scoreboard_button = button(WIDTH/2 + (WIDTH/4), 450, 'Scoreboard', self.screen, WHITE, GRAY)
        settings_button = sizable_button(290, 22, 'Settings', self.screen, 80,25, 16, 6, WHITE, GRAY)
        self.buttonlist.append(character_button)
        self.buttonlist.append(scoreboard_button)
        self.button_sprites.add(character_button)
        self.button_sprites.add(scoreboard_button)
        self.buttonlist.append(settings_button)
        self.button_sprites.add(settings_button)
        pg.display.flip()
        self.wait()


    def show_go_screen(self):
        self.screen.fill(BACKGROUND)
        self.draw_text("GAME OVER", 32, WHITE, WIDTH/2,HEIGHT/4-40) # Draw text
        self.draw_text("Your Score: " + str(self.score), 18, WHITE, WIDTH/2,HEIGHT/4 -5)
        self.draw_text("Press any key to restart", 18, WHITE, WIDTH/2,HEIGHT * 3/4)
        pg.display.flip()
        self.wait()
        pass

    def wait(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            if self.menu == False:
                draw_menu_buttons(self.buttonlist, self.button_sprites)
            else:
                draw_menu_buttons(self.selected_menu.buttons, self.selected_menu.button_group)
            for event in pg.event.get(): #Listen for Key input
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP and self.menu == False:
                    waiting = False
                    self.pipes = True
                if event.type == pg.MOUSEMOTION: #Check for mouse hover
                    pos = pg.mouse.get_pos()
                    if self.menu == False: #Main Menu check
                        button_hover(self.buttonlist,self.button_sprites,pos)
                    else: #In secondary menu
                        button_hover(self.selected_menu.buttons, self.selected_menu.button_group, pos)
                if event.type == pg.MOUSEBUTTONDOWN: #Check for button click
                    if event.button == 1:
                        pos = pg.mouse.get_pos()
                        if self.menu == False:
                            for b in self.buttonlist:
                                if b.mouseover(pos):
                                    self.selected_menu = Menu(b.text, self.screen, self) #Create menu
                                    self.menu = True 
                                    if b.text == "Character":
                                        grid(self.screen, self.character_list, self.selected_menu, self)
                                    elif b.text == "Scoreboard":
                                        draw_scoreboard(self.screen)
                                    break
                        else:
                            for b in self.selected_menu.buttons: #Check for menu button clicks
                                if b.mouseover(pos):
                                    if b.type == 'Menu':       
                                        if b.text == "Back":
                                            self.selected_menu = None
                                            self.menu = False
                                            self.screen.fill(BACKGROUND) 
                                            self.draw_text("PyFlappy", 32, WHITE, WIDTH/2,HEIGHT/4-40) # Draw text
                                            self.draw_text(VERSION, 18, WHITE, WIDTH/2,HEIGHT/4 -5)
                                            self.draw_text("Press any key to begin", 18, (255,255,255), WIDTH/2,HEIGHT * 3/4)
                                            draw_menu_buttons_clr(self.buttonlist, self.button_sprites, WHITE)
                                    elif b.type == 'Grid':
                                        b.callback()
                                        pass
                                    break
        

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_path, size)
        text_surf = font.render(text,True,color)
        text_rect = text_surf.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surf, text_rect)

app = App()
app.show_start_screen()
while app.running:
    app.new()
    app.show_go_screen()

