from prgrmr.events import Events
from prgrmr.managers import Managers
from prgrmr.elements.flags import ElementFlags as flags


class Element:
    def __init__(self, flags_: set[flags] = None):
        super().__init__()
        self.flags = flags_ or set()
        self.managers = Managers(self)
        self.events = Events()

    def has_flag(self, flag: flags):
        return flag in self.flags

    def add_flag(self, flag: flags):
        self.flags.add(flag)

    def remove_flag(self, flag: flags):
        self.flags.remove(flag)

    def toggle_flag(self, flag: flags):
        if self.has_flag(flag):
            self.remove_flag(flag)
        else:
            self.add_flag(flag)

    def add_manager(self, name: str, *args, **kwargs):
        self.managers.add(name, *args, **kwargs)

    def get_manager(self, name: str):
        return self.managers.get(name)

    def remove_manager(self, name: str):
        self.managers.remove(name)

    def apply_managers(self):
        self.managers.apply()
        
    def update(self):
        self.apply_managers()


availible_elements = {}
short_to_long_name = {}


def register(name: str, one_letter_name: str):
    def decorator(cls):
        availible_elements[name] = cls
        short_to_long_name[one_letter_name] = name
        return cls

    return decorator


def get_element(name: str):
    if name in short_to_long_name:
        name = short_to_long_name[name]
    return availible_elements[name]
