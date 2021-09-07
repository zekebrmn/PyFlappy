import pygame as pg
from sprites import *
from buttons import *
from settings import *
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
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.started = False
        self.pipes = False
        self.pipeListTop = []
        self.pipeListBottom = []
        self.score = 0
        self.label = self.font_obj.render(str(self.score), 1, (0,0,0))
        self.buttonlist=[]
        for i in range(1000):
            length = random.randint(50,300)
            self.pipeListTop.append(pipe_top(length,400 + (i * 165)))
            self.pipeListBottom.append(pipe_bottom((HEIGHT-length)-140,400 + (i*165)))

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.ground = floor()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.ground)
        for bottom_pipe in self.pipeListBottom:
            self.all_sprites.add(bottom_pipe)
        
        for top_pipe in self.pipeListTop:
            self.all_sprites.add(top_pipe)

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            if self.started:
                self.player.move()
                if self.pipes:
                    for bottom_pipe in self.pipeListBottom:
                        bottom_pipe.move()
        
                    for top_pipe in self.pipeListTop:
                        top_pipe.move()
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        hit_ground = pg.sprite.collide_rect(self.player, self.ground)
        hit_pipe = False

        #Pipe Collision
        for bottom_pipe in self.pipeListBottom:
            if bottom_pipe.rect.x == self.player.rect.x or bottom_pipe.rect.x == self.player.rect.x - 1:
                self.score += 1
                self.label = self.font_obj.render(str(self.score), 1, (0,0,0))
            if bottom_pipe.rect.x > 85:
                hit_pipe = pg.sprite.collide_rect(self.player, bottom_pipe)
                if hit_pipe:
                    break
        
        for top_pipe in self.pipeListTop:
            if top_pipe.rect.x > 85 and hit_pipe == False:
                hit_pipe = pg.sprite.collide_rect(self.player, top_pipe)
                if hit_pipe:
                    break

        #End Cycle
        if hit_pipe:
            self.pipes = False
        if hit_ground:
            self.started = False
        
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
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)
        self.screen.blit(self.label, ((WIDTH/2)-15,55))
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BACKGROUND)
        self.draw_text("PyFlappy", 32, (255,255,255), WIDTH/2,HEIGHT/4)
        self.draw_text("Press any key to begin", 18, (255,255,255), WIDTH/2,HEIGHT * 3/4)
        character_button = button(WIDTH/2 - (WIDTH/4), 450, 'Character', self.screen)
        scoreboard_button = button(WIDTH/2 + (WIDTH/4), 450, 'Scoreboard', self.screen)
        self.buttonlist.append(character_button)
        self.buttonlist.append(scoreboard_button)
        pg.display.flip()
        self.wait()

    def show_go_screen(self):
        # game over/continue
        #self.clip = VideoFileClip('./mp4/troll.mp4')
        #self.clip.fx(resize, width=WIDTH)
        #self.clip.preview()
        pass

    def wait(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
                if event.type == pg.MOUSEMOTION:
                    pass
            
            
        

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_path, size)
        text_surf = font.render(text,True,color)
        text_rect = text_surf.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surf, text_rect)

game = App()
game.show_start_screen()
while game.running:
    game.new()
    game.run()
game.show_go_screen()