import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *


#player health




class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
    
    def draw_text(self, text,font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder,'img')
        self.map = Map(path.join(game_folder, 'map2.txt'))
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.title_font = path.join(img_folder, 'TANK.TTF')
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.middlemob_img = pg.image.load(path.join(img_folder, MIDDLE_MOB_IMG)).convert_alpha()
        self.bigboss_img = pg.image.load(path.join(img_folder, BIGBOSS_IMG)).convert_alpha()
        self.bulletbb_img = pg.image.load(path.join(img_folder, BULLETBB_IMG)).convert_alpha()
        self.item_img = pg.image.load(path.join(img_folder, ITEM_IMG)).convert_alpha()
        #self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.obstacle_img = pg.image.load(path.join(img_folder, OBSTACLE_IMG)).convert_alpha()
        self.tree_img = pg.image.load(path.join(img_folder, TREE_IMG)).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.middlemobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.bullets1 = pg.sprite.Group()
        self.bulletsbb1 = pg.sprite.Group()
        self.bulletsbb2 = pg.sprite.Group()
        self.bigboss = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.trees = pg.sprite.Group()
        self.player = Player(self, 10, 10)
        
        #self.mob = Mob(self, 15, 15)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self,col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'L':
                    Middlemob(self, col, row)
                if tile == 'B':
                    Bigboss(self, col , row)
                if tile == 'H':
                    Item(self, col ,row)
                if tile == 'O':
                    Obstacle(self, col ,row)
                if tile == 'T':
                    Tree(self, col ,row)     
                #if tile == 'P':
                  #  self.player = Player(self,col,tile)  
      
        
        
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

        #if (( len(self.mobs) == 0 ) & (len(self.middlemobs) == 0) & (len(self.bigboss) == 0)):
            #self.playing = False


        global MOBS_COUNT
        global MIDDLEMOB_COUNT
        global BIGBOSS_COUNT
        if ((len(self.mobs) == 0)&(MOBS_COUNT != 0)):
            Mob(self, 37,27)
            Mob(self,40,4)
            MOBS_COUNT -= 1
        if ((MOBS_COUNT == 2)&(MIDDLEMOB_COUNT != 0)):
            Middlemob(self, 19 , 3)
            Middlemob(self, 19 , 20)
            MIDDLEMOB_COUNT -=1
        
        if ((len(self.middlemobs)==0)&(len(self.mobs)==0)&(MIDDLEMOB_COUNT == 0)&(MOBS_COUNT == 0)&(BIGBOSS_COUNT != 0)):
            Bigboss(self, 20, 15)
            BIGBOSS_COUNT -= 1
        #if MOBS_COUNT == 0:
            #self.playing = False

        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.player.health = self.player.health + 100

        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
            if hits:
                self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

       

        hits = pg.sprite.spritecollide(self.player, self.bullets1, False, collide_hit_rect )
        for hit in hits:
            self.player.health -= MIDDLE_MOB_BULLET_DAMAGE
            hit.vel = vec(0,0)
            if self.player.health <=0:
                self.playing = False
            if hits:
                self.player.pos -= vec(MIDDLE_MOB_KNOCKBACK,0).rotate(-hits[0].rot)

        
        hits = pg.sprite.spritecollide(self.player, self.bulletsbb1, False, collide_hit_rect )
        for hit in hits:
            self.player.health -= BIGBOSS_BULLET_DAMAGE
            hit.vel = vec(0,0)
            if self.player.health <=0:
                self.playing = False
            if hits:
                self.player.pos -= vec(BIGBOSS_KNOCKBACK,0).rotate(-hits[0].rot)


        hits = pg.sprite.spritecollide(self.player, self.bulletsbb2, False, collide_hit_rect )
        for hit in hits:
            self.player.health -= BIGBOSS_BULLET_DAMAGE
            hit.vel = vec(0,0)
            if self.player.health <=0:
                self.playing = False
            if hits:
                self.player.pos -= vec(BIGBOSS_KNOCKBACK,0).rotate(-hits[0].rot)



        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0,0)
            

        hits = pg.sprite.groupcollide(self.middlemobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0,0)
        
        hits = pg.sprite.groupcollide(self.bigboss, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0,0)
            
        #LEVEL1_MOBS = 5
        #if (LEVEL1_MOBS != 0):
            #Mob(self,37,3)
            #LEVEL1_MOBS = LEVEL1_MOBS - 1
           #Mob(self, 37, 27)
           #LEVEL1_MOBS = LEVEL1_MOBS - 1
        #if (LEVEL1_MOBS == 0):
            #Middlemob(self, 18, 22)
        #if self.mobs.has() != True:
            #Mob(self, 10, 10)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
       # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()

        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                sprite.draw_health()
        
        for sprite in self.all_sprites:
            if isinstance(sprite, Middlemob):
                sprite.draw_health()
        
        for sprite in self.all_sprites:
            if isinstance(sprite, Bigboss):
                sprite.draw_health()


            self.screen.blit(sprite.image, self.camera.apply(sprite))

        
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER",self.title_font, 100,RED,WIDTH /2, HEIGHT/2, align="center")
        self.draw_text("PRESS ANY KEY",self.title_font, 75, WHITE, WIDTH /2 , HEIGHT*3 /4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                waiting = False
                self.quit()
            if event.type == pg.KEYUP:
                waiting = False

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()