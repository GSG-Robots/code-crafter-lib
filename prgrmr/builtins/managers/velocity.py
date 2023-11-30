from prgrmr.managers import Manager, register


@register("velocity")
class VelocityManager(Manager):
    def __init__(self, apply_to):
        super().__init__(apply_to)
        self.x_velocity = 0
        self.y_velocity = 0

    def apply(self):
        self.target.rect.x += self.x_velocity
        self.target.rect.y += self.y_velocity
