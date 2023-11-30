import pygame
from prgrmr import *

set_fps(60)
set_resolution(500, 500)
set_title("My Game")
set_icon("game.svg")

level = load_mapfile("level1.levelmap")
load_level(level)

# add_element("player", kwargs=settings["player_start_values"])

level_ = 0

@events.every("quit")
def on_quit():
    global level_
    level_ += 1
    
    if level_ > 1:
        print("You Won!")
        pygame.quit()
        return
    
    from prgrmr.engine import initialized_elements
    
    for element in initialized_elements.values():
        element.unregister_events()
        
    initialized_elements.clear()
    
    level = load_mapfile("level2.levelmap")
    load_level(level)
    run()
    

run()
