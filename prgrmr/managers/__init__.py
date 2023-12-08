import pygame

# from prgrmr.elements import Element

availible_managers = {}


def register(name):
    def decorator(cls):
        availible_managers[name] = cls
        return cls

    return decorator


class Manager:
    def __init__(self, apply_to: "..elements.Element"):
        super().__init__()
        self.target: "..elements.Element" = apply_to

    def apply(self):
        raise NotImplementedError()


class Managers:
    def __init__(self, apply_to):
        self.target: "..elements.Element" = apply_to
        self.managers: dict[str, Manager] = {}

    def add(self, name: str, **kwargs):
        self.managers[name] = availible_managers[name](self.target, **kwargs)

    def get(self, name: str):
        return self.managers[name]

    def remove(self, name: str):
        del self.managers[name]

    def apply(self):
        for manager in self.managers.values():
            manager.apply()
