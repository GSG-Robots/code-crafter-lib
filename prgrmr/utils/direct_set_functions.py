from ..settings import settings

def set_resolution(width: int, height: int):
    """Set the resolution of the window."""
    settings("resolution", (width, height))
    return settings("resolution")

def set_fps(fps: int):
    """Set the FPS of the game."""
    settings("fps", fps)
    return settings("fps")

def set_title(title: str):
    """Set the title of the window."""
    settings("title", title)
    return settings("title")

def set_icon(icon: str):
    """Set the icon of the window."""
    settings("icon", icon)
    return settings("icon")
