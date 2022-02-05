##
# src/main.py
# A program to simulate gravity, oh no

import pygame

import colors

SCREEN_SIZE = (600, 400)

def main():
    """
    The main game loop
    """
    # Consts
    BG = colors.RGB.WHITE

    # Pygame stuff
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # Reset screen
        screen.fill(BG)

        # Update display
        pygame.display.flip()

        clock.tick(60)



if __name__ == "__main__":
    main()
