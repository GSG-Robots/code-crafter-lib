import pygame

from prgrmr.settings import settings
from prgrmr.elements import Element, flags, register
from prgrmr.events import events


@register("wall", "W")
@events.will_listen(["update", "draw"])
class Wall(Element, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__(
            {
                flags.OBSTRUCTS,
            }
        )
        self.image = pygame.Surface([width, height])
        self.image.fill(settings["wall_color"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        events.register_event_handler("update", self.update)
        events.register_event_handler("draw", self.draw)

    def update(self):
        self.managers.apply()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
