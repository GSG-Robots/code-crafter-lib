from collections import deque
import enum
from typing import Any
from prgrmr.managers import Manager, register


class Priorities:
    DEGRADED = 2.5
    DIRECT_INPUT = 5
    INVISIBLE_FORCE = 7.5
    COLLISION = 10
    EMERGENCY = 100


class Operation:
    def __init__(self, priority):
        self.priority = priority
        
    @staticmethod
    def sort_key(x):
        return x.priority

class SetOperation(Operation):
    def __init__(self, value, priority=5):
        super().__init__(priority)
        self.value = value
        
    def __call__(self, initial):
        return self.value

class AddOperation(Operation):
    def __init__(self, value, priority=5):
        super().__init__(priority)
        self.value = value
        
    def __call__(self, initial):
        return initial + self.value

class MulOperation(Operation):
    def __init__(self, value, priority=5):
        super().__init__(priority)
        self.value = value
        
    def __call__(self, initial):
        return initial * self.value

class CoordinatePart:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.calculations = deque()
    
    def apply_changes(self):
        for step in sorted(self.calculations, key=Operation.sort_key):
            self.value = step(self.value)
        return self.value
            
    def set(self, value, priority=5):
        self.calculations.append(SetOperation(value, priority))
        
    def add(self, value, priority=5):
        self.calculations.append(AddOperation(value, priority))
        
    def sub(self, value, priority=5):
        self.calculations.append(AddOperation(-value, priority))
        
    def mul(self, value, priority=5):
        self.calculations.append(MulOperation(value, priority))
        
    def div(self, value, priority=5):
        self.calculations.append(MulOperation(1/value, priority))
        
    def __repr__(self) -> str:
        return f"<{__name__}.CoordinatePart {self.name}={self.value} queued_operations={len(self.calculations)}>"
        


@register("velocity")
class VelocityManager(Manager):
    def __init__(self, apply_to):
        super().__init__(apply_to)
        self.x = CoordinatePart("x", 0)
        self.y = CoordinatePart("y", 0)
        self.prio = Priorities

    def apply(self):
        self.target.rect.x += self.x.apply_changes()
        self.target.rect.y += self.y.apply_changes()

        
