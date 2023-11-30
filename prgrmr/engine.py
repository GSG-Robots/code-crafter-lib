import pygame
from typing import Callable
from .settings import settings
from .events import events
from .utils.conditions import INFINITE, NEVER
from .exceptions import MissingElementError
from prgrmr.elements import availible_elements

initialized_elements = {}


def elm(name: str, nid: int = 0, args: tuple = (), kwargs: dict = {}):
    if name not in availible_elements:
        raise MissingElementError(name)
    exact_name = f"{name}:{nid}"
    if exact_name not in initialized_elements:
        initialized_elements[exact_name] = availible_elements[name](*args, **kwargs)
    return initialized_elements[exact_name]


@events.will_raise_event("update")
@events.will_raise_event("draw")
@events.will_raise_event("quit")
def run(ending_condition: Callable = INFINITE):
    screen = pygame.display.set_mode(settings("resolution"))
    pygame.display.set_caption(settings("title"))
    pygame.display.set_icon(pygame.image.load(settings("icon")))

    clock = pygame.time.Clock()

    while ending_condition():
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # pylint: disable=no-member
                ending_condition = NEVER
        screen.fill((255, 255, 255))
        events.raise_event("update")
        events.raise_event("draw", screen)
        pygame.display.flip()
        clock.tick(settings("fps"))
    events.raise_event("quit")
