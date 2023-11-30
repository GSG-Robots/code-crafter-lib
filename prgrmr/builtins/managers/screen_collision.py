from prgrmr.settings import settings
from prgrmr.managers import Manager, register


@register("screen_collision")
class ScreenCollisionManager(Manager):
    def __init__(self, apply_to):
        super().__init__(apply_to)
        self.left_screen_bottom = False
        self.left_screen_top = False
        self.left_screen_left = False
        self.left_screen_right = False

    def apply(self):
        self.left_screen_bottom = (
            self.target.rect.y >= settings["resolution"][1] - self.target.rect.height
        )
        self.left_screen_top = self.target.rect.y <= 0
        self.left_screen_left = self.target.rect.x <= 0
        self.left_screen_right = (
            self.target.rect.x >= settings["resolution"][0] - self.target.rect.width
        )
