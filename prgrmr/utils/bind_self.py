import functools


class BoundCallable:
    def __init__(self, func):
        self._func = func
        self._bound = func

    def bind(self, __bind_to):
        self._bound = functools.partial(self._func, __bind_to)

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)


def bound(func):
    class Wrapper(BoundCallable):
        pass

    Wrapper.__name__ = func.__name__
    return Wrapper(func)


def bind_self(self, attrs=None):
    for attr in attrs or dir(self):
        if attr.startswith("__") and attr.endswith("__"):
            continue
        if isinstance(getattr(self, attr), BoundCallable):
            getattr(self, attr).bind(self)
    return self


def get_func(func):
    return func._bound if isinstance(func, BoundCallable) else func
