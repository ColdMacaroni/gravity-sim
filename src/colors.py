##
# src/colors.py
# Some colours that can be easily accessed

from pygame import Color
from random import randint

class RGB:
    WHITE = Color(0xFF, 0xFF, 0xFF)

    def random():
        return Color(randint(0x00, 0xFF), randint(0x00, 0xFF), randint(0x00, 0xFF))

