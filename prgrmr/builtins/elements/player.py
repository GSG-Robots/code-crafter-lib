import pygame

from prgrmr import settings

from prgrmr.elements import register, Element, flags
from prgrmr.events import events


@register("player", "P")
class Player(Element, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed=5):
        super().__init__(
            {
                flags.PLAYER,
                flags.OBSTRUCTS,
            }
        )
        self.image = pygame.Surface([width, height])
        self.image.fill(settings["player_color"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

        self.add_manager("velocity")
        self.add_manager("screen_collision")
        self.add_manager(
            "screen_lock",
            allow_leaving_bottom=False,
            allow_leaving_left=False,
            allow_leaving_right=False,
        )
        self.add_manager("vertical_collision")
        self.add_manager("horizontal_collision")
        self.add_manager("gravity")
        self.add_manager("jumping")
        self.add_manager("friction")
        self.add_manager("movement")

        events.register_event_handler("update", self.update)
        events.register_event_handler("draw", self.draw)

    def on_collision(self, other_element):
        print(other_element)

    # @events.every("draw")
    def draw(self, screen):
        screen.blit(self.image, self.rect)
