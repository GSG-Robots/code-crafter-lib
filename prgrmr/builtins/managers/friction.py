from prgrmr.managers import Manager, register


@register("friction")
class FrictionManager(Manager):
    def __init__(self, apply_to, friction_rate=0.8, min_speed=0.1):
        super().__init__(apply_to)
        self.friction_rate = friction_rate
        self.min_speed = min_speed

    def apply(self):
        velocity_manager = self.target.get_manager("velocity")
        velocity_manager.x_velocity *= self.friction_rate
        if abs(velocity_manager.x_velocity) < self.min_speed:
            velocity_manager.x_velocity = 0
