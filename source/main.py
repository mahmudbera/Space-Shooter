import os
import pygame
import random
from laser import *
from ships import *
from settings import *

pygame.init()


def main():

    pygame.font.init()
    pygame.display.set_caption("Space Shooter")

    run = True  # will be used to continue and end the game.
    game_over = False

    FPS = 60
    clock = pygame.time.Clock()

    start_time = pygame.time.get_ticks()

    aliens = []  # All created aliens are added to this list.
    aliens_lasers = []  # All created alien's lasers are added to this list.

    level = 0

    player_velocity = 5
    alien_velocity = 5

    laser_velocity = 3
    alien_length = 5

    player = Player(300, 650)

    # Function used to update and draw the game screen.
    def draw_screen():

        WINDOWS.blit(BACKGROUND, (0, 0))
        player.draw(WINDOWS)

        for alien in aliens:
            alien.draw(WINDOWS)

        # The time the player stays in the game is printed on the screen.
        font = pygame.font.SysFont("comicsans", 30)
        time_text = font.render(
            "Süre: " + str(current_time // 1000) + " sn", True, (255, 255, 255)
        )
        WINDOWS.blit(time_text, (525, 40))

        # The player's level is printed on the screen.
        level_text = font.render("Level: " + str(level), True, (255, 255, 255))
        WINDOWS.blit(level_text, (525, 5))

        # When the player's health reaches 0, game over is declared.
        if player.health == 0:
            font = pygame.font.SysFont("comicsans", 80)
            game_over_text = font.render("Game Over", True, (255, 255, 255))
            WINDOWS.blit(
                game_over_text,
                (
                    WIDTH / 2 - game_over_text.get_width() / 2,
                    HEIGHT / 2 - game_over_text.get_height() / 2,
                ),
            )

        pygame.display.update()

    # Used to update elapsed time.
    def update_time():
        global current_time
        current_time = pygame.time.get_ticks() - start_time

    while run:

        clock.tick(FPS)

        update_time()
        draw_screen()

        # Player's controls
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and player.x < WIDTH - player.ship_image.get_width():
            player.x += player_velocity

        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_velocity

        if keys[pygame.K_UP] and player.y > 0:
            player.y -= player_velocity

        if keys[pygame.K_DOWN] and player.y < HEIGHT - player.ship_image.get_height():
            player.y += player_velocity

        if keys[pygame.K_SPACE]:
            player.shoot()

        if (
            len(aliens) == 0
        ):  # Every time the list is empty, an alien will be produced again.
            alien_velocity += 1
            alien_length += (
                3  # The number of aliens will increase with each level passed.
            )
            level += 1
            player.health = 100

            # This is the loop we use to get aliens from different places each time.
            for i in range(alien_length):
                x = random.randrange(0, WIDTH)
                y = random.randrange(0, int(HEIGHT / 2 - 200))

                alien = Alien(
                    x, y, random.choice(["black", "light_purple", "dark_purple"])
                )
                aliens.append(alien)

        player.move_lasers(
            laser_velocity, aliens
        )  # Player move_lasers fonksiyonuyla belirtilen hızda lazer atar.

        # In this for loop, we control the movements of the aliens.
        for alien in aliens:
            alien.move(alien_velocity)  # All aliens move at the speed specified.
            alien.move_lasers(
                -laser_velocity, player
            )  # All aliens shoot lasers at the speed specified.

            if random.randrange(0, 20) == 1:
                alien.shoot()

            for (
                laser
            ) in (
                aliens_lasers
            ):  # If the alien's laser hits the player, the player's health will decrease.
                if collide(laser, player):
                    player.health -= 10
                    aliens_lasers.remove(laser)

            # When the aliens themselves encounter the player, the player dies.
            if collide(alien, player):
                player.health -= 1

            if (
                alien.y > HEIGHT
            ):  # Finish the game when the aliens reach the lower limit and disappear completely.
                aliens.remove(alien)
                game_over = True
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # If the user wants to exit, we end the game loop by setting the run variable to False.

        # Control and handling of player death.
        if player.health == 0:
            player.reduce_health(10)
            if player.lives == 0:
                game_over = True
            #   ⬇⬇⬇⬇
        if game_over:
            WINDOWS.fill((0, 0, 0))
            font = pygame.font.SysFont("comicsans", 95)
            game_over_text = font.render("Game Over", True, (255, 255, 255))
            x = WIDTH / 2 - game_over_text.get_width() / 2
            y = HEIGHT / 2 - game_over_text.get_height() / 2
            WINDOWS.blit(game_over_text, (x, y))
            pygame.display.update()
            pygame.time.wait(3000)
            run = False


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 40)
    run = True
    while run:
        WINDOWS.blit(BACKGROUND, (0, 0))
        title_label = title_font.render(
            "Press the mouse to begin...", 1, (255, 255, 255)
        )
        WINDOWS.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_time = pygame.time.get_ticks()
                main()


main_menu()
