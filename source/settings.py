import os
import pygame

# screen options
WIDTH = 700
HEIGHT = 750
WINDOWS = pygame.display.set_mode((WIDTH, HEIGHT))

SLOW_MOT = 30
score = 0

# load images
BACKGROUND = pygame.image.load(os.path.join("images", "background.png"))

PLAYER_LASER = pygame.image.load(os.path.join("images", "player_laser.png"))

ALIENS1_LASER1 = pygame.image.load(os.path.join("images", "enemy_laser1.png"))
ALIENS2_LASER2 = pygame.image.load(os.path.join("images", "enemy_laser2.png"))
ALIENS3_LASER3 = pygame.image.load(os.path.join("images", "enemy_laser3.png"))

MISSION_SHIP = pygame.image.load(os.path.join("images", "space_ship.png"))

ALIENS1 = pygame.image.load(os.path.join("images", "black_alien.png"))
ALIENS2 = pygame.image.load(os.path.join("images", "light_alien.png"))
ALIENS3 = pygame.image.load(os.path.join("images", "dark_alien.png"))

STAR_SPEED = pygame.image.load(os.path.join("images", "star_speed.png"))
HEART = pygame.image.load(os.path.join("images", "heart.png"))
