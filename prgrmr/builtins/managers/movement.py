import pygame

from prgrmr.managers import Manager, register


@register("movement")
class MovementManager(Manager):
    def __init__(
        self,
        apply_to,
        speed=5,
        jump_height=20,
        allow_jumping=False,
        left_key=pygame.K_LEFT,  # pylint: disable=no-member
        right_key=pygame.K_RIGHT,  # pylint: disable=no-member
    ):
        self.target = apply_to
        self.speed = speed
        self.allow_jumping = allow_jumping
        self.is_jumping = False
        self.jump_height = jump_height
        self.left_key = left_key
        self.right_key = right_key

    def move(self, x):
        self.target.get_manager("velocity").x_velocity = x * self.speed

    def apply(self):
        keys = pygame.key.get_pressed()
        if keys[self.left_key]:
            self.move(-1)
        if keys[self.right_key]:
            self.move(1)
