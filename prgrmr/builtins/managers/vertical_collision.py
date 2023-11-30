from prgrmr.elements import flags
from prgrmr.engine import initialized_elements
from prgrmr.managers import Manager, register


@register("vertical_collision")
class VerticalCollisionManager(Manager):
    def __init__(self, apply_to):
        super().__init__(apply_to)

        self.on_ground = False
        self.on_ceiling = False

    def apply(self):
        velocity_manager = self.target.get_manager("velocity")
        screen_collision_manager = self.target.get_manager("screen_collision")

        self.on_ground = screen_collision_manager.left_screen_bottom
        self.on_ceiling = screen_collision_manager.left_screen_top

        for element in initialized_elements.values():
            if not element.has_flag(flags.OBSTRUCTS):
                continue
            if element == self.target:
                continue
            if not self.target.rect.colliderect(element.rect):
                continue

            if (
                velocity_manager.y_velocity > 0
                and self.target.rect.bottom >= element.rect.top
            ):
                self.target.rect.bottom = element.rect.top
                velocity_manager.y_velocity = 1
                self.on_ground = True
            if (
                velocity_manager.y_velocity < 0
                and self.target.rect.top <= element.rect.bottom
            ):
                self.target.rect.top = element.rect.bottom
                velocity_manager.y_velocity = -1
                self.on_ceiling = True
