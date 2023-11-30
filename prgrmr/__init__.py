import pygame

from prgrmr.engine import run
from prgrmr.events import events
from prgrmr.exceptions import *
from prgrmr.load_builtins import load_builtins
from prgrmr.map_manager import import_level, load_mapfile
from prgrmr.settings import settings
from prgrmr.utils.direct_set_functions import *

load_builtins()

print("-" * 20)
print("Welcome to prgrmr!")
print("prgrmr is an easy-to-use game engine written in Python, using pygame.")
print("For more information, visit https://prgrmr.jojojux.de")
print("-" * 20)


def quit_game():
    pygame.quit()  # pylint: disable=no-member
