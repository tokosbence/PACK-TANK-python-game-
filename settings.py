import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BROWN

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

ITEM_IMG = 'crateMetal.png'


BULLET_IMG = 'bulletDark.png' 
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
KICKBACK = 200
GUN_SPREAD = 5
BULLET_DAMAGE = 50

WALL_IMG = 'tile_09.png'
OBSTACLE_IMG = 'barricadeWood.png'
TREE_IMG = 'treeGreen_large.png'

MOBS_COUNT = 5
MIDDLEMOB_COUNT = 1

MIDDLE_MOB_IMG = 'tank_darkLarge.png'
MIDDLE_MOB_BULLET_RATE = 500
MIDDLE_MOB_HEALTH = 150
MIDDLE_MOB_BULLET_DAMAGE = 15
MIDDLE_MOB_KNOCKBACK = 40
MIDDLE_MOB_BULLET_LIFETIME = 500
MIDDLE_MOB_BULLET_SPEED = 250


BIGBOSS_COUNT = 1
BULLETBB_IMG = 'bulletRed2.png'
BIGBOSS_IMG = 'tank_huge.png'
BIGBOSS_HEALTH = 250
BIGBOSS_SPEED = 200
BIGBOSS_HIT_RECT = pg.Rect(0,0,35,35)
KICKBACK_BIGBOSS = 0
BARREL_OFFSET_BB1 = vec(25,0) 
BARREL_OFFSET_BB2 = vec(0, 15)
BIGBOSS_BULLET_DAMAGE = 25
BIGBOSS_BULLET_RATE = 300
BIGBOSS_KNOCKBACK = 30
BIGBOSS_BULLET_SPEED = 350

MOB_IMG = 'tank_darkr.png'
MOB_SPEED = 200
MOB_HIT_RECT = pg.Rect(0,0,30,30)
MOB_HEALTH = 50
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20

PLAYER_HEALTH = 200
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'tank_bluer.png'
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
BARREL_OFFSET = vec(20, 0)
