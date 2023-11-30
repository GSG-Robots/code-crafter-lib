from prgrmr.managers import Manager, register


@register("gravity")
class GravityManager(Manager):
    def __init__(self, apply_to, gravity_rate=0.2, allow_falling_off=False):
        super().__init__(apply_to)
        self.gravity_rate = gravity_rate
        self.is_falling = True
        self.allow_falling_off = allow_falling_off

    def apply(self):
        if self.is_falling:
            self.target.get_manager("velocity").y_velocity += self.gravity_rate
        if self.allow_falling_off:
            return

        if self.target.get_manager("vertical_collision").on_ground:
            self.is_falling = False
        else:
            self.is_falling = True
