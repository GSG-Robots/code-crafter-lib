from prgrmr.managers import Manager, register
import pygame


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
        self.target.get_manager("velocity").y_velocity = -self.jump_speed

    def apply(self):
        keys = pygame.key.get_pressed()
        if keys[self.jump_key]:
            self.jump()
        if self.is_jumping:
            self.target.get_manager("velocity").x_velocity *= self.jump_movement_limit
        if self.target.get_manager("vertical_collision").on_ground:
            self.is_jumping = False
