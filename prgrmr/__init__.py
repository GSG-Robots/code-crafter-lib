from .engine import run, elm as add_element
from .settings import settings
from .utils.direct_set_functions import *
from . import prepare_defaults as __PD__
from .utils.element_registry import register_element
from .utils import element_types as element_types
from .exceptions import *
from .events import events
from .map_manager import load_mapfile, load_level

def quit():
    import pygame
    pygame.quit()
