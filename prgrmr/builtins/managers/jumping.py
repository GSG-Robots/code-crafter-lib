import pygame

from prgrmr.managers import Manager, register


@register("jumping")
class JumpingManager(Manager):
    def __init__(
        self,
        apply_to,
        jump_speed=6,
        jump_movement_limit=0.5,
        key=pygame.K_UP,  # pylint: disable=no-member
    ):
        super().__init__(apply_to)
        self.jump_speed = jump_speed
        self.is_jumping = False
        self.jump_movement_limit = jump_movement_limit
        self.jump_key = key

    def jump(self):
        if self.is_jumping:
            return
        self.is_jumping = True
        self.target.velocity.y.set(-self.jump_speed, self.target.velocity.prio.DIRECT_INPUT)

    def apply(self):
        keys = pygame.key.get_pressed()
        if keys[self.jump_key]:
            self.jump()
        print(self.is_jumping)
        if self.is_jumping:
            self.target.velocity.x.mul(self.jump_movement_limit)
        if self.target.managers.get("vertical_collision").on_ground:
            self.is_jumping = False
