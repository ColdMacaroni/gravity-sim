#!/usr/bin/env python3
# src/main.py
# A program to simulate gravity
# Copyright (C) 2022  ColdMacaroni
# Licensed under GPLv3

import pygame

import math
from math import sqrt
from enum import Enum, auto
import colors

# Constants
SCREEN_SIZE = (600, 600)
OUTER_LIMITS = (300, 300)


class BodyStatus(Enum):
    ACTIVE = auto()
    INACTIVE = auto()
    PASSIVE = auto()


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

    def add_vector(self, other: "Vector", mult: float = 1):
        """
        Adds a vector to this one. Can use the mult(iplier) parameter to determine influence
        """
        self.x += other.x * mult
        self.y += other.y * mult

    def div(self, num: float):
        """
        Divides both x and y by the num
        """
        if num:
            self.x /= num
            self.y /= num

    # TODO: Add reset method that sets x and y to 0

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
        pp_r = (
            start[0] + self.y * self.line_scale,
            self.x * self.line_scale + start[1],
        )

        # We can then use a linear interpolation to see how long the head will be
        # It'll be done between the end of the arrow body and the perpendicular line
        # P0 + t(P1 - P0)
        head_end_r = end[0] + self.head_len * (pp_r[0] - end[0]), end[
            1
        ] + self.head_len * (pp_r[1] - end[1])

        pygame.draw.line(screen, self.color, end, head_end_r, self.line_width)

        # - Left side
        # Reflect the pp point across the start to get the other side arrow and repeat
        pp_l = start[0] + (start[0] - pp_r[0]), start[1] + (start[1] - pp_r[1])

        head_end_l = end[0] + self.head_len * (pp_l[0] - end[0]), end[
            1
        ] + self.head_len * (pp_l[1] - end[1])
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
        status: BodyStatus = BodyStatus.ACTIVE,
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
        self.status = status

    def get_pos(self) -> tuple[float, float]:
        """
        Returns x, y position in a tuple
        """
        return self.x, self.y

    def get_area(self) -> float:
        """
        Returns area of body
        """
        return math.pi * self.radius**2

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
        if self.status is BodyStatus.ACTIVE:
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

    starting_pos = None

    paused_text = pygame.font.SysFont(
        pygame.font.get_default_font(), 42).render("Paused", True, (0, 0, 0))
    paused = False

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
                                    BodyStatus.INACTIVE,
                                )
                            )
                        elif isinstance(starting_pos, tuple):
                            # Stop setting the radius to the mouse position, now vector
                            starting_pos = Vector
                        else:
                            # All done, you can go now
                            starting_pos = None
                            bodies[-1].status = BodyStatus.ACTIVE

                    # Right click used to set passive obj
                    elif event.button == 3:
                        if starting_pos is Vector:
                            starting_pos = None

                            bodies[-1].vector.x = 0
                            bodies[-1].vector.y = 0
                            bodies[-1].status = BodyStatus.PASSIVE

                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            # Make it start with a 0 vector
                            if starting_pos is Vector:
                                bodies[-1].vector.x = 0
                                bodies[-1].vector.y = 0
                                bodies[-1].status = BodyStatus.ACTIVE
                                starting_pos = None

                        # R to reset bodies
                        case pygame.K_r:
                            # Countermeasures for crashes
                            if starting_pos is None:
                                bodies.clear()

                        # Z as in undo
                        case pygame.K_z:
                            # Only pop if there are things to pop and it wont interfere
                            # on some other thing
                            if bodies and starting_pos is None:
                                bodies.pop()
                        
                        # Change paused state if nothing else is going on
                        case pygame.K_SPACE:
                            # if starting_pos is None:
                            paused = not paused

            # Show size
            if isinstance(starting_pos, tuple):
                bodies[-1].radius = (
                    dist(bodies[-1].get_pos(), pygame.mouse.get_pos()) / Body.scale
                )
            # Now show vector
            elif starting_pos is Vector:
                mouse_pos = pygame.mouse.get_pos()
                bodies[-1].vector.x = (mouse_pos[0] - bodies[-1].x) / Vector.line_scale
                bodies[-1].vector.y = (bodies[-1].y - mouse_pos[1]) / Vector.line_scale

        # Reset screen
        screen.fill(BG)

        for body in bodies:
            # dont move the bodies when paused
            if paused:
                body.draw(screen)

            else:
                body.move()
                body.draw(screen)
                # Check for collisions, increasing mass to the biggest
                for other in bodies:
                    if (
                        other is body
                        or body.status is BodyStatus.INACTIVE
                        or other.status is BodyStatus.INACTIVE
                    ):
                        continue

                    # Handle collisions
                    if dist(body.get_pos(), other.get_pos()) <= body.radius + other.radius:
                        # Remove smaller if both are active objects
                        if (
                            body.status is BodyStatus.ACTIVE
                            and other.status is not BodyStatus.PASSIVE
                        ):
                            # the mass of the smaller body will be absorbed into the biggest one
                            smaller, bigger = sorted(
                                [body, other], key=lambda x: x.get_area()
                            )

                            # Add vectors together, using ratio between areas to determine influence
                            # Pi would simplify out which is why it isn't included
                            bigger.vector.add_vector(
                                smaller.vector, (smaller.radius**2) / (bigger.radius**2)
                            )

                            # Calculate new radius based on the sum of their areas
                            bigger.radius = sqrt(
                                (smaller.get_area() + bigger.get_area()) / math.pi
                            )

                            bodies.remove(smaller)
                            del smaller

                        # Delete the other if this is passive and other is not
                        elif (
                            body.status is BodyStatus.PASSIVE
                            and other.status is BodyStatus.ACTIVE
                        ):
                            bodies.remove(other)
                            del other

                    # gravitate
                    elif body.status is BodyStatus.ACTIVE:
                        # Create new vector based on the other body
                        grav_vector = Vector(other.x - body.x, body.y - other.y)

                        # Scale down
                        grav_vector.div(Vector.line_scale**2)

                        # grav_vector.draw(screen, (body.x, body.y))

                        body.vector.add_vector(
                            grav_vector,
                            (other.get_area())
                            / (dist(body.get_pos(), other.get_pos()) ** 2),
                        )

                # Remove bodies that are out of bounds
                if (
                    body.x < (0 - OUTER_LIMITS[0])
                    or body.x > (SCREEN_SIZE[0] + OUTER_LIMITS[0])
                    or body.y < (0 - OUTER_LIMITS[1])
                    or body.y > (SCREEN_SIZE[1] + OUTER_LIMITS[1])
                ):
                    bodies.remove(body)
                    del body

        # Show that it is paused to avoid confusion
        # Needs to be drawn outside previous for loop, otherwise it's skipped if 
        # bodies is empty
        if paused:
            screen.blit(paused_text, (5,5))

        # Update display
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
