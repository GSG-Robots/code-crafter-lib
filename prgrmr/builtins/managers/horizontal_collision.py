from prgrmr.elements.flags import ElementFlags
from prgrmr.engine import initialized_elements
from prgrmr.managers import Manager, register


@register("horizontal_collision")
class HorizontalCollisionManager(Manager):
    def __init__(self, apply_to):
        super().__init__(apply_to)

        self.hit_left_wall = False
        self.hit_right_wall = False

    def apply(self):
        velocity_manager = self.target.get_manager("velocity")
        screen_collision_manager = self.target.get_manager("screen_collision")

        self.hit_left_wall = screen_collision_manager.left_screen_left
        self.hit_right_wall = screen_collision_manager.left_screen_right

        for element in initialized_elements.values():
            if not self.target.rect.colliderect(element.rect):
                continue
            if not element.has_flag(ElementFlags.OBSTRUCTS):
                continue
            if element == self.target:
                continue
            
            
            if (
                self.target.rect.top >= element.rect.bottom
                or self.target.rect.bottom <= element.rect.top 
            ):
                return
            
            if (
                velocity_manager.x_velocity > 0
                and self.target.rect.right >= element.rect.left
            ):
                self.target.rect.right = element.rect.left
                velocity_manager.x_velocity = 0
                self.hit_right_wall = True
            if (
                velocity_manager.x_velocity < 0
                and self.target.rect.left <= element.rect.right
            ):
                self.target.rect.left = element.rect.right
                velocity_manager.x_velocity = 0
                self.hit_left_wall = True
