from prgrmr.managers import Manager, register


@register("friction")
class FrictionManager(Manager):
    def __init__(self, apply_to, friction_rate=0.8, min_speed=0.1):
        super().__init__(apply_to)
        self.friction_rate = friction_rate
        self.min_speed = min_speed

    def apply(self):
        self.target.velocity.x.mul(self.friction_rate)
        if abs(self.target.velocity.x.value) < self.min_speed:
            self.target.velocity.x.set(0, self.target.velocity.prio.DEGRADED)
