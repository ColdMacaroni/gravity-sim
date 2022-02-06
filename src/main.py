#!/usr/bin/env python3
# src/main.py
# A program to simulate gravity, oh no

import pygame

import math
from math import sqrt

import colors

# Constants
SCREEN_SIZE = (600, 400)
OUTER_LIMITS = (800, 800)


# Objects
class Vector:
    line_scale = 50
    line_width = 2

    head_len = 0.15

    def __init__(
        self, x: float, y: float, color: pygame.Color = pygame.Color(0x00, 0x00, 0x00)
    ):
        self.x = x
        self.y = y

        self.color = color

    def __iadd__(self, other: 'Vector'):
        """
        support for += with other vectors
        """
        self.x += other.x
        self.y += other.y

    def draw(self, screen, start):
        """
        Draws the vector as an arrow
        """
        # Dont draw static vectors and also avoid calculation errors i think
        if self.x + self.y == 0:
            return

        # Remember that pygame y coordinates are inversed
        end = (start[0] + self.x * self.line_scale, start[1] - self.y * self.line_scale)

        # - Right side
        # will create a point 90° off the start. pp=perpendicular
        pp_r = (start[0] + self.y * self.line_scale, self.x * self.line_scale + start[1])

        # We can then use a linear interpolation to see how long the head will be
        # It'll be done between the end of the arrow body and the perpendicular line
        # P0 + t(P1 - P0)
        head_end_r = end[0] + self.head_len * (pp_r[0] - end[0]), \
                     end[1] + self.head_len * (pp_r[1] - end[1])

        pygame.draw.line(screen, self.color, end, head_end_r, self.line_width)

        # - Left side
        # Reflect the pp point across the start to get the other side arrow and repeat
        pp_l = start[0] + (start[0] - pp_r[0]), start[1] + (start[1] - pp_r[1])

        head_end_l = end[0] + self.head_len * (pp_l[0] - end[0]), \
                     end[1] + self.head_len * (pp_l[1] - end[1])
        pygame.draw.line(screen, self.color, end, head_end_l, self.line_width)

        # Draw arrow head
        # pygame.draw.line(screen, self.color, (0, 0), end, self.line_width)
        # pygame.draw.line(screen, self.color, (0, 0), end, self.line_width)

        # Draw arrow body
        pygame.draw.line(screen, self.color, start, end, self.line_width)


class Body:
    # How many pixels each radius unit represents
    scale = 1

    # Pixels per vector unit
    speed = 5

    def __init__(
        self,
        radius: float,
        pos: tuple[int | float, int | float],
        vector: Vector,
        color: pygame.Color = pygame.Color(0x78, 0x52, 0x46),
        active: bool = True,
    ):
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
        self.active = active

    def get_pos(self) -> tuple[float, float]:
        """
        Returns x, y position in a tuple
        """
        return self.x, self.y

    def get_area(self) -> float:
        """
        Returns area of body
        """
        return math.pi * self.radius ** 2

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
        if self.active:
            self.x += self.vector.x * self.speed
            self.y -= self.vector.y * self.speed


def dist(pos1, pos2) -> float:
    """
    Distance between two points
    """
    return sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)


def main():
    """
    The main game loop
    """
    # Consts
    BG = colors.RGB.WHITE

    # Pygame stuff
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, vsync=1)
    clock = pygame.time.Clock()

    bodies = list()

    test_body = Body(15, (300, 200), Vector(1, 1))

    # For creating new Objects
    # TODO: Find a better way to do this?
    creating = None
    starting_pos = None

    running = True
    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    exit()

                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if starting_pos is None:
                            # Create a new obj at the mouse pos
                            starting_pos = pygame.mouse.get_pos()
                            bodies.append(
                                Body(
                                    1,
                                    starting_pos,
                                    Vector(0, 0),
                                    colors.RGB.random(),
                                    False,
                                )
                            )
                        elif isinstance(starting_pos, tuple):
                            # Stop setting the radius to the mouse position, now vector
                            starting_pos = Vector
                        else:
                            # All done, you can go now
                            starting_pos = None
                            bodies[-1].active = True

            # Show size
            if isinstance(starting_pos, tuple):
                bodies[-1].radius = (
                    dist(bodies[-1].get_pos(), pygame.mouse.get_pos())
                    / Body.scale
                )
            # Now show vector
            elif starting_pos is Vector:
                mouse_pos = pygame.mouse.get_pos()
                bodies[-1].vector.x = (mouse_pos[0] - bodies[-1].x) / Vector.line_scale
                bodies[-1].vector.y = (bodies[-1].y - mouse_pos[1]) / Vector.line_scale

        # Reset screen
        screen.fill(BG)

        for body in bodies:
            body.move()
            body.draw(screen)

            # Check for collisions, increasing mass to the biggest
            for other in bodies:
                if other is body or not body.active or not other.active:
                    continue
                if dist(body.get_pos(), other.get_pos()) <= body.radius + other.radius:
                    # the mass of the smaller body will be absorbed into the biggest one
                    smaller, bigger = sorted([body, other], key=lambda x: x.get_area())

                    # TODO: add vectors together, proportionally based on are maybe?

                    # Calculate new radius based on the sum of their areas
                    bigger.radius = sqrt((smaller.get_area() +  bigger.get_area())/math.pi)


                    bodies.remove(smaller)
                    del smaller


            # Remove bodies that are out of bounds
            if (
                body.x < (0 - OUTER_LIMITS[0])
                or body.x > (SCREEN_SIZE[0] + OUTER_LIMITS[0])
                or body.y < (0 - OUTER_LIMITS[1])
                or body.y > (SCREEN_SIZE[1] + OUTER_LIMITS[1])
            ):
                bodies.remove(body)
                del body

        test_body.draw(screen)
        test_body.move()

        # Update display
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
