import pygame

from ..settings import settings
from ..utils.managers import Managers
from ..utils.element_types import ObstructingElement
from ..utils.element_registry import register_element
from ..events import events


@register_element("wall")
@events.will_listen(["update", "draw"])
class Wall(ObstructingElement, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(settings["wall_color"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.managers = Managers(self)

        events.register_event_handler("update", self.update)
        events.register_event_handler("draw", self.draw)

    # @events.every("update")
    def update(self):
        self.managers.apply()

    # @events.every("draw")
    def draw(self, screen):
        screen.blit(self.image, self.rect)
