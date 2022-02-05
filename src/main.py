#!/usr/bin/env python3
# src/main.py
# A program to simulate gravity, oh no

import pygame

import colors

# Constants
SCREEN_SIZE = (600, 400)


# Objects
class Vector:
    line_scale = 15
    line_width = 2

    def __init__(self, x: float, y: float,
            color: pygame.Color = pygame.Color(0x00, 0x00, 0x00)):
        self.x = x
        self.y = y

        self.color = color

    def draw(self, screen, start):
        """
        Draws the vector as an arrow
        """
        # Remember that pygame y coordinates are inversed
        end = (start[0] + self.x * self.line_scale, start[1] - self.y * self.line_scale)

        # TODO: Add arrow head
        #       Get perpendicular line (reciprocal of gradient) and move like 10px or like
        #       half a scale on each direction

        pygame.draw.line(screen, self.color, start, end, self.line_width)


class Body:
    # How many pixels each radius unit represents
    scale = 1

    # Pixels per vector unit
    speed = 5
    def __init__(self, radius: float, pos: tuple[int|float, int|float], vector: Vector,
            color: pygame.Color = pygame.Color(0xb3, 0x31, 0xff)):
        """
        Radius: The radius of the object (not in pixels)
        Pos: Center of the body
        Vector: Vector obj representing the motion of the body.
        Color: Color object for drawing this body
        """
        self.radius = radius
        self.x, self.y = pos
        self.vector = vector

        self.color = color

    def draw(self, screen: pygame.Surface):
        """
        Draws this body on the surface as per its attributes.
        """
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        self.vector.draw(screen, (self.x, self.y))

    def move(self):
        """
        Uses the vector to change the position
        """
        # Substract y bc pygame coords
        self.x += self.vector.x * self.speed
        self.y -= self.vector.y * self.speed


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

    test_body = Body(15, (300, 200), Vector(1, 1))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # Reset screen
        screen.fill(BG)

        test_body.draw(screen)
        test_body.move()

        # Update display
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
