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
        screen_collision_manager = self.target.managers.get("screen_collision")

        self.on_ground = screen_collision_manager.left_screen_bottom
        self.on_ceiling = screen_collision_manager.left_screen_top

        for element in initialized_elements.values():
            if not element.has_flag(flags.OBSTRUCTS):
                continue
            if element == self.target:
                continue
            if not self.target.rect.colliderect(element.rect):
                continue
            
            
            if not (
                self.target.rect.left <= element.rect.right
                or self.target.rect.right >= element.rect.left 
            ):
                return
        
            if (
                self.target.velocity.y.value > 0
                and self.target.rect.bottom >= element.rect.top
            ):
                self.target.rect.bottom = element.rect.top
                self.target.velocity.y.set(0)
                self.on_ground = True
            if (
                self.target.velocity.y.value < 0
                and self.target.rect.top <= element.rect.bottom
            ):
                self.target.rect.top = element.rect.bottom
                self.target.velocity.y.set(0)
                self.on_ceiling = True
