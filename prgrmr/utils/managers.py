import pygame

from ..utils.element_types import ObstructingElement
from ..settings import settings
from ..engine import initialized_elements


class ScreenCollisionManager:
    def __init__(self, apply_to):
        self.target = apply_to
        self.left_screen_bottom = False
        self.left_screen_top = False
        self.left_screen_left = False
        self.left_screen_right = False

    def apply(self):
        self.left_screen_bottom = (
            self.target.rect.y >= settings["resolution"][1] - self.target.rect.height
        )
        self.left_screen_top = self.target.rect.y <= 0
        self.left_screen_left = self.target.rect.x <= 0
        self.left_screen_right = (
            self.target.rect.x >= settings["resolution"][0] - self.target.rect.width
        )


class HorizontalCollisionManager:
    def __init__(self, apply_to):
        self.target = apply_to

        self.hit_left_wall = False
        self.hit_right_wall = False

    def apply(self):
        velocity_manager = self.target.managers.get_manager("VelocityManager")
        screen_collision_manager = self.target.managers.get_manager(
            "ScreenCollisionManager"
        )

        self.hit_left_wall = screen_collision_manager.left_screen_left
        self.hit_right_wall = screen_collision_manager.left_screen_right

        for element in initialized_elements.values():
            if not isinstance(element, ObstructingElement):
                continue
            if element == self.target:
                continue
            if not self.target.rect.colliderect(element.rect):
                continue
            
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

class GeneralCollisionManager:
    def __init__(self, apply_to):
        self.target = apply_to

        self.collides_with = set()

    def apply(self):
        self.collides_with.clear()

        for element in initialized_elements.values():
            if not isinstance(element, ObstructingElement):
                continue
            if element == self.target:
                continue
            if not self.target.rect.colliderect(element.rect):
                continue
            
            self.collides_with.add(element)

class VerticalCollisionManager:
    def __init__(self, apply_to):
        self.target = apply_to

        self.on_ground = False
        self.on_ceiling = False

    def apply(self):
        velocity_manager = self.target.managers.get_manager("VelocityManager")
        screen_collision_manager = self.target.managers.get_manager(
            "ScreenCollisionManager"
        )

        self.on_ground = screen_collision_manager.left_screen_bottom
        self.on_ceiling = screen_collision_manager.left_screen_top

        for element in initialized_elements.values():
            if not isinstance(element, ObstructingElement):
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
                velocity_manager.y_velocity = 0
                self.on_ground = True
            if (
                velocity_manager.y_velocity < 0
                and self.target.rect.top <= element.rect.bottom
            ):
                self.target.rect.top = element.rect.bottom
                velocity_manager.y_velocity = 0
                self.on_ceiling = True


class ScreenLockManager:
    def __init__(
        self,
        apply_to,
        allow_leaving_bottom=True,
        allow_leaving_top=True,
        allow_leaving_left=True,
        allow_leaving_right=True,
    ):
        self.target = apply_to
        self.allow_leaving_bottom = allow_leaving_bottom
        self.allow_leaving_top = allow_leaving_top
        self.allow_leaving_left = allow_leaving_left
        self.allow_leaving_right = allow_leaving_right

    def apply(self):
        collision_manager = self.target.managers.get_manager("ScreenCollisionManager")
        velocity_manager = self.target.managers.get_manager("VelocityManager")

        if not self.allow_leaving_bottom and collision_manager.left_screen_bottom:
            if velocity_manager.y_velocity > 0:
                velocity_manager.y_velocity = 0
            self.target.rect.y = settings["resolution"][1] - self.target.rect.height
        if not self.allow_leaving_top and collision_manager.left_screen_top:
            if velocity_manager.y_velocity < 0:
                velocity_manager.y_velocity = 0
            self.target.rect.y = 0
        if not self.allow_leaving_left and collision_manager.left_screen_left:
            if velocity_manager.x_velocity < 0:
                velocity_manager.x_velocity = 0
            self.target.rect.x = 0
        if not self.allow_leaving_right and collision_manager.left_screen_right:
            if velocity_manager.x_velocity > 0:
                velocity_manager.x_velocity = 0
            self.target.rect.x = settings["resolution"][0] - self.target.rect.width


class VelocityManager:
    def __init__(self, apply_to):
        self.target = apply_to
        self.x_velocity = 0
        self.y_velocity = 0

    def apply(self):
        self.target.rect.x += self.x_velocity
        self.target.rect.y += self.y_velocity


class FallingManager:
    def __init__(self, apply_to, gravity_rate=0.2, allow_falling_off=False):
        self.target = apply_to
        self.gravity_rate = gravity_rate
        self.is_falling = True
        self.allow_falling_off = allow_falling_off

    def apply(self):
        if self.is_falling:
            self.target.managers.get_manager(
                "VelocityManager"
            ).y_velocity += self.gravity_rate
        if self.allow_falling_off:
            return

        if self.target.managers.get_manager("VerticalCollisionManager").on_ground:
            self.is_falling = False
        else:
            self.is_falling = True
            


class FrictionManager:
    def __init__(self, apply_to, friction_rate=0.8, min_speed=0.1):
        self.target = apply_to
        self.friction_rate = friction_rate
        self.min_speed = min_speed

    def apply(self):
        velocity_manager = self.target.managers.get_manager("VelocityManager")
        velocity_manager.x_velocity *= self.friction_rate
        if abs(velocity_manager.x_velocity) < self.min_speed:
            velocity_manager.x_velocity = 0


class MovementManager:
    def __init__(
        self,
        apply_to,
        speed=5,
        jump_height=20,
        allow_jumping=False,
        left_key=pygame.K_LEFT,
        right_key=pygame.K_RIGHT,
    ):
        self.target = apply_to
        self.speed = speed
        self.allow_jumping = allow_jumping
        self.is_jumping = False
        self.jump_height = jump_height
        self.left_key = left_key
        self.right_key = right_key

    def move(self, x):
        self.target.managers.get_manager("VelocityManager").x_velocity = x * self.speed

    def apply(self):
        keys = pygame.key.get_pressed()
        if keys[self.left_key]:
            self.move(-1)
        if keys[self.right_key]:
            self.move(1)


class JumpingManager:
    def __init__(
        self, apply_to, jump_speed=6, jump_movement_limit=0.5, key=pygame.K_UP
    ):
        self.target = apply_to
        self.jump_speed = jump_speed
        self.is_jumping = False
        self.jump_movement_limit = jump_movement_limit
        self.jump_key = key

    def jump(self):
        if self.is_jumping:
            return
        self.is_jumping = True
        self.target.managers.get_manager(
            "VelocityManager"
        ).y_velocity = -self.jump_speed

    def apply(self):
        keys = pygame.key.get_pressed()
        if keys[self.jump_key]:
            self.jump()
        if self.is_jumping:
            self.target.managers.get_manager(
                "VelocityManager"
            ).x_velocity *= self.jump_movement_limit
        if self.target.managers.get_manager("VerticalCollisionManager").on_ground:
            self.is_jumping = False


class ManagerCollection:
    def __init__(self, apply_to):
        self.target = apply_to
        self.managers = {}

    def register(self, manager):
        self.managers[manager.__class__.__name__] = manager

    def get_manager(self, name):
        return self.managers[name]

    def apply(self):
        for manager in self.managers.values():
            manager.apply()


class Managers(ManagerCollection):
    def __init__(self, apply_to):
        self.target = apply_to
        self.managers = {}

    def register(self, manager):
        self.managers[manager.__class__.__name__] = manager

    def get_manager(self, name):
        return self.managers[name]

    def apply(self):
        for manager in self.managers.values():
            manager.apply()
