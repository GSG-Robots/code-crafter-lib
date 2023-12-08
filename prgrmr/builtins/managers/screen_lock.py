from prgrmr.managers import Manager, register
from prgrmr.settings import settings


@register("screen_lock")
class ScreenLockManager(Manager):
    def __init__(
        self,
        apply_to,
        allow_leaving_bottom=True,
        allow_leaving_top=True,
        allow_leaving_left=True,
        allow_leaving_right=True,
    ):
        super().__init__(apply_to)
        self.allow_leaving_bottom = allow_leaving_bottom
        self.allow_leaving_top = allow_leaving_top
        self.allow_leaving_left = allow_leaving_left
        self.allow_leaving_right = allow_leaving_right

    def apply(self):
        collision_manager = self.target.managers.get("screen_collision")

        if not self.allow_leaving_bottom and collision_manager.left_screen_bottom:
            if self.target.velocity.y.value > 0:
                self.target.velocity.y.set(0)
            self.target.rect.y = settings["resolution"][1] - self.target.rect.height
        if not self.allow_leaving_top and collision_manager.left_screen_top:
            if self.target.velocity.y.value < 0:
                self.target.velocity.y.set(0)
            self.target.rect.y = 0
        if not self.allow_leaving_left and collision_manager.left_screen_left:
            if self.target.velocity.x.value < 0:
                self.target.velocity.x.value = 0
            self.target.rect.x = 0
        if not self.allow_leaving_right and collision_manager.left_screen_right:
            if self.target.velocity.x.value > 0:
                self.target.velocity.x.value = 0
            self.target.rect.x = settings["resolution"][0] - self.target.rect.width
