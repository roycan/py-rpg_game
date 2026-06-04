
from abc import ABC, abstractmethod

class GameEntity(ABC):
    def __init__(self, name, hp):
        self._name = name
        self._max_hp = hp
        self._hp = hp

    @property
    def name(self): return self._name

    @property
    def hp(self): return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, self._max_hp))

    @property
    def max_hp(self): return self._max_hp

    @abstractmethod
    def take_turn(self, targets): pass

    def is_alive(self): return self._hp > 0

class UsableItem(ABC):
    @abstractmethod
    def use(self, user, target): pass
