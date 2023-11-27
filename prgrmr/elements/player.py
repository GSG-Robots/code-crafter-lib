import pygame

from ..settings import settings
from ..utils.managers import (
    FrictionManager,
    FallingManager,
    JumpingManager,
    MovementManager,
    ScreenCollisionManager,
    HorizontalCollisionManager,
    VerticalCollisionManager,
    VelocityManager,
    ScreenLockManager,
    Managers
)
from ..utils.element_types import PlayerElement
from ..utils.element_registry import register_element
from ..events import events


@register_element("player")
@events.will_listen(["update", "draw"])
class Player(PlayerElement, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed=5):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(settings["player_color"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        
        self.managers = Managers(self)
        vm = VelocityManager(self)
        self.managers.register(vm)
        self.managers.register(ScreenCollisionManager(self))
        self.managers.register(ScreenLockManager(self, allow_leaving_bottom=False, allow_leaving_left=False, allow_leaving_right=False))
        self.managers.register(HorizontalCollisionManager(self))
        self.managers.register(VerticalCollisionManager(self))
        self.managers.register(FallingManager(self))
        self.managers.register(JumpingManager(self))
        self.managers.register(FrictionManager(self))
        self.managers.register(MovementManager(self))
        
        events.register_event_handler("update", self.update)
        events.register_event_handler("draw", self.draw)
        
    # @events.every("update")
    def update(self):
        self.managers.apply()

    # @events.every("draw")
    def draw(self, screen):
        screen.blit(self.image, self.rect)
