import pygame
from prgrmr.settings import settings
from prgrmr.utils.direct_set_functions import *
from prgrmr.load_builtins import load_builtins
from prgrmr.exceptions import *
from prgrmr.events import events
from prgrmr.map_manager import load_mapfile, import_level
from prgrmr.engine import run


load_builtins()

print("-" * 20)
print("Welcome to prgrmr!")
print("prgrmr is an easy-to-use game engine written in Python, using pygame.")
print("For more information, visit https://prgrmr.jojojux.de")
print("-" * 20)


def quit_game():
    pygame.quit()  # pylint: disable=no-member
