from typing import Any, Callable, Union
from .utils.bind_self import BoundCallable, bound, get_func, bind_self


class Events:
    def __init__(self) -> None:
        self.event_handlers = {}

    def will_listen(
        self, attrs_or_cls: Union[list[str], type]
    ) -> Union[type, callable]:
        def __decorator__(cls: type) -> type:
            class Wrapper(cls):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    if not isinstance(attrs_or_cls, type):
                        for attr in attrs_or_cls:
                            if isinstance(getattr(self, attr), BoundCallable):
                                continue
                            else:
                                if attr in attrs_or_cls:
                                    setattr(self, attr, bound(getattr(self, attr)))
                        bind_self(self, attrs_or_cls)
                    else:
                        bind_self(self)

            Wrapper.__name__ = cls.__name__
            return Wrapper

        if isinstance(attrs_or_cls, type):
            return __decorator__(attrs_or_cls)
        else:
            return __decorator__

    def will_raise_event(self, event: str) -> bool:
        self.register_event(event)

        def __decorator__(func: Callable) -> Callable:
            return func

        return __decorator__

    def register_event(self, event: str) -> None:
        self.event_handlers[event] = []

    def register_event_handler(self, event: str, handler: Callable) -> None:
        if event not in self.event_handlers:
            raise KeyError(f"Event '{event}' is not registered.")
        self.event_handlers[event].append(handler)

    def unregister_event_handler(self, event: str, handler: Callable) -> None:
        self.event_handlers[event].remove(handler)

    def unregister_event(self, event: str) -> None:
        del self.event_handlers[event]

    def every(self, event: str) -> Callable:
        def __decorator__(handler: Callable) -> Callable:
            handler = bound(handler)
            self.register_event_handler(event, handler)
            return handler

        return __decorator__

    def raise_event(self, event: str, *args, **kwargs) -> None:
        for handler in self.event_handlers[event]:
            get_func(handler)(*args, **kwargs)

    def __call__(
        self, event: Union[str, None] = None, handler: Union[Callable, None] = None
    ) -> Any:
        if event == None:
            return self.event_handlers
        elif handler == None:
            return self.event_handlers[event]
        else:
            self.register_event_handler(event, handler)


events = Events()
