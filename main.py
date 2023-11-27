from prgrmr import *

set_fps(60)
set_resolution(500, 500)
set_title("My Game")
set_icon("game.svg")

level = load_mapfile("level1.levelmap")
load_level(level)

# add_element("player", kwargs=settings("player_start_values"))

run()
