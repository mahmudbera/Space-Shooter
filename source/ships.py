import pygame
import random
from laser import Laser
from settings import *

# health bar features
BAR_COLOR = (128, 0, 128)
BAR_WIDTH = 200
BAR_HEIGHT = 20
BAR_MARGIN = 10


# Superclass
class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = None
        self.laser_image = None
        self.lasers = []
        self.slow_mot_counter = 0

    def draw(self, window):
        window.blit(self.ship_image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def get_width(self):
        return self.ship_image.get_width()

    def get_height(self):
        return self.ship_image.get_height()

    def shoot(self):
        if self.slow_mot_counter == 0:
            laser = Laser(self.x, self.y, self.laser_image)
            self.lasers.append(laser)

    def slow_motion(self):
        if self.slow_mot_counter >= SLOW_MOT:
            self.slow_mot_counter = 0
        else:
            self.slow_mot_counter += 1


# Subclass
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_image = MISSION_SHIP
        self.laser_image = PLAYER_LASER
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.max_health = health
        global score
        score = 0
        self.lives = 3

    def shoot(self):
        if self.slow_mot_counter == 0:
            laser = Laser(self.x + 20, self.y, self.laser_image)
            self.lasers.append(laser)

    def move_lasers(self, velocity, objects):
        self.slow_motion()
        for laser in self.lasers:
            laser.move(velocity)
            for object in objects:
                if laser.collision(object):
                    objects.remove(object)
                    self.lasers.remove(laser)
                    global score  # Declare 'score' as a global variable
                    score += 10  # Increment the score by 10 when an alien is hit
                    break

    def draw_score(self, window):

        font = pygame.font.SysFont("comicsans", 30)
        score_text = font.render("Puan: " + str(score), True, (255, 255, 255))
        window.blit(score_text, (525, 75))

    def draw(self, window):
        window.blit(self.ship_image, (self.x, self.y))
        self.healt_bar(window)
        self.draw_score(window)
        self.draw_lives(window)

        for laser in self.lasers:
            laser.draw(window)

    def healt_bar(self, window):
        pygame.draw.rect(
            WINDOWS,
            BAR_COLOR,
            (
                self.x,
                self.y + self.ship_image.get_height(),
                self.ship_image.get_width(),
                7,
            ),
        )
        pygame.draw.rect(
            WINDOWS,
            (0, 255, 0),
            (
                self.x,
                self.y + self.ship_image.get_height(),
                int(self.ship_image.get_width() * (self.health / self.max_health)),
                7,
            ),
        )

    def reduce_health(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            if self.lives > 0:
                self.lives -= 1
                self.health = 100
            else:
                global game_over
                game_over = True

    def draw_lives(self, window):
        for i in range(self.lives):
            heart_rect = HEART.get_rect()
            heart_rect.x = 10 + i * (heart_rect.width + 5)
            heart_rect.y = 10
            window.blit(HEART, heart_rect)


# Subclass
class Alien(Ship):
    COLOR = {
        "black": (ALIENS1, ALIENS1_LASER1),
        "light_purple": (ALIENS2, ALIENS2_LASER2),
        "dark_purple": (ALIENS3, ALIENS3_LASER3),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_image, self.laser_image = self.COLOR[color]
        self.direction = 1
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.x = random.randint(0, WIDTH - self.get_width())  # generate random location
        global score
        score = 0

    def move(self, velocity):
        self.x += velocity * self.direction
        if self.x <= 0 or self.x >= WIDTH - self.get_width():
            self.y += self.get_height()
            self.direction *= -1

    def shoot(self):
        if self.slow_mot_counter == 0:
            laser = Laser(self.x, self.y, self.laser_image)
            self.lasers.append(laser)

    def move_lasers(self, velocity, obj):
        self.slow_motion()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.collision(obj):
                obj.health -= 10
                global score
                score -= 4
                self.lasers.remove(laser)

    def draw_score(self, window):
        pass

    def draw(self, window):
        window.blit(self.ship_image, (self.x, self.y))
        self.draw_score(window)

        for laser in self.lasers:
            laser.draw(window)
