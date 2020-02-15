import pygame as pg
import sys
from random import uniform
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2

def collide_with_walls(sprite, group,  dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(sprite,group,False, collide_hit_rect)
            if hits:
                if hits[0].rect.centerx > sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
                if hits[0].rect.centerx < sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x
        if dir == 'y':
             hits = pg.sprite.spritecollide(sprite,group,False, collide_hit_rect)
             if hits:
                 if hits[0].rect.centery > sprite.hit_rect.centery:
                     sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height /2
                 if hits[0].rect.centery < sprite.hit_rect.centery:
                     sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height /2
                 sprite.vel.y = 0
                 sprite.hit_rect.centery = sprite.pos.y





class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        
    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0,0)
        self.vx, self.vy =0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED/2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE] or keys[pg.K_g]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos , dir ) 
                self.vel = vec(-KICKBACK, 0).rotate(-self.rot)

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / PLAYER_HEALTH)
        self.health_bar = pg.Rect(0,0, width, 10)
        if self.health < PLAYER_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)   
    
    

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos 
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.obstacles,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.obstacles, 'y')
        self.rect.center = self.hit_rect.center
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.trees,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.trees, 'y')
        self.rect.center = self.hit_rect.center


class Middlemob(pg.sprite.Sprite):
    def __init__(self, game, x ,y):
        self.groups = game.all_sprites, game.middlemobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.middlemob_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.rot = 0
        self.last_shot = 0
        self.health = MIDDLE_MOB_HEALTH

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MIDDLE_MOB_HEALTH)
        self.health_bar = pg.Rect(0,0, width, 10)
        if self.health < MIDDLE_MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)
    
    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.middlemob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        if self.health <= 0:
            self.kill()
        now = pg.time.get_ticks()
        if now - self.last_shot > MIDDLE_MOB_BULLET_RATE:
            self.last_shot = now
            dir = vec(1,0).rotate(-self.rot)
            Bullet1(self.game, self.pos, dir)
    

class Bigboss(pg.sprite.Sprite):
    def __init__(self, game, x ,y):
        self.groups = game.all_sprites, game.bigboss
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bigboss_img
        self.rect = self.image.get_rect()
        self.hit_rect = BIGBOSS_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x,y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.last_shot = 0
        self.health = BIGBOSS_HEALTH

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / BIGBOSS_HEALTH)
        self.health_bar = pg.Rect(0,0, width, 10)
        if self.health < BIGBOSS_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.bigboss_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(BIGBOSS_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x') 
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self,self.game.obstacles, 'x')
        self.hit_rect.centery = self.pos.y 
        collide_with_walls(self, self.game.obstacles, 'y')
        self.rect.center = self.hit_rect.center
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.trees,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.trees, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
        now = pg.time.get_ticks()
        if now - self.last_shot > BIGBOSS_BULLET_RATE:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos1 = self.pos + BARREL_OFFSET_BB1.rotate(-self.rot)
            pos2 = self.pos + BARREL_OFFSET_BB2.rotate(-self.rot)
            BulletBB1(self.game, pos1 , dir ) 
            BulletBB2(self.game, pos2 , dir)
            self.vel = vec(-KICKBACK_BIGBOSS, 0).rotate(-self.rot)

class Item(pg.sprite.Sprite):
    def __init__(self, game , x,y):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_img
        self.rect = self.image.get_rect()
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos

class BulletBB1(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bulletsbb1
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bulletbb_img
        self.rect = self.image.get_rect()
        self.rot = 0
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BIGBOSS_BULLET_SPEED 
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.sprite.spritecollideany(self, self.game.trees):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > MIDDLE_MOB_BULLET_LIFETIME:
            self.kill()

class BulletBB2(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bulletsbb2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bulletbb_img
        self.rect = self.image.get_rect()
        self.rot = 0
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BIGBOSS_BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.sprite.spritecollideany(self, self.game.trees):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > MIDDLE_MOB_BULLET_LIFETIME:
            self.kill()



class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x,y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x') 
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self,self.game.obstacles, 'x')
        self.hit_rect.centery = self.pos.y 
        collide_with_walls(self, self.game.obstacles, 'y')
        self.rect.center = self.hit_rect.center
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.trees,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.trees, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0,0, width, 10)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)
       





class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.sprite.spritecollideany(self, self.game.trees):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > MIDDLE_MOB_BULLET_LIFETIME:
            self.kill()



class Bullet1(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets1
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rot = 0
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * MIDDLE_MOB_BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.sprite.spritecollideany(self, self.game.trees):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        self.groups = game.all_sprites, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.obstacle_img
        self.rect = self.image.get_rect()
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos

class Tree(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        self.groups = game.all_sprites, game.trees
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.tree_img
        self.rect = self.image.get_rect()
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
        


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE