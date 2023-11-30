from typing import Union

from .settings import settings
from .engine import elm

tiles = {
    "P": "player",
    " ": None,
    "W": "wall",
    "R": "respawn",
    "G": "goal"
}

def load_mapfile(path: str):
    """Load a mapfile from a path."""
    with open(path, "r") as f:
        data = f.read()
    
    map_data = []
    
    line_length = len(data.split("\n")[0])
    
    for line in data.split("\n"):
        if not line:
            continue
        
        if len(line) != line_length:
            raise ValueError(f"Line length mismatch: expected {line_length}, got {len(line)}")
        
        line_data = []
        for letter in line:
            line_data.append(tiles[letter])
        map_data.append(line_data)
        
    if len(map_data) == 1:
        map_data = map_data[0]
    
    return map_data

def load_level(level_data=list[list[str]], size = 50):
    """Load a level from a list of lists."""
    settings["resolution"] = (len(level_data[0])*size, len(level_data)*size)
    
    counter = 0
    
    for y, row in enumerate(level_data):
        for x, tile in enumerate(row):
            if tile == None:
                continue
            counter += 1
            elm(tile, counter, kwargs={
                "x": x*size,
                "y": y*size,
                "width": size,
                "height": size
            })
