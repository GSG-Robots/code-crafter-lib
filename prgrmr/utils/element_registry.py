import functools
from typing import Any, Union


class ElementRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, name, element):
        self._registry[name] = element

    def element(self, name):
        def __decorator__(element):
            self.register(name, element)
            return element

        return __decorator__

    def get(self, element_name):
        return self._registry[element_name]

    def __iter__(self):
        return iter(self._registry)

    def __getitem__(self, element_name):
        return self._registry[element_name]

    def __setitem__(self, element_name, element):
        self._registry[element_name] = element(self)

    def __delitem__(self, element_name):
        del self._registry[element_name]

    def __contains__(self, element_name):
        return element_name in self._registry

    def __call__(
        self, name: Union[str, None] = None, element: Union[Any, None] = None
    ) -> Any:
        if name == None:
            return self._registry
        elif element == None:
            return self._registry[name]
        else:
            self._registry[name] = element


element_registry = ElementRegistry()


register_element = element_registry.element
