import pygame
from prgrmr import *

set_fps(60)
set_resolution(500, 500)
set_title("My Game")
set_icon("game.svg")

level = load_mapfile("level1.levelmap")
load_level(level)

# add_element("player", kwargs=settings["player_start_values"])

@events.every("quit")
def on_quit():
    pygame.quit()
    

try:
    run()
except:
    from prgrmr.engine import initialized_elements
    
    initialized_elements.clear()
    
    level = load_mapfile("level2.levelmap")
    load_level(level)
    run()
