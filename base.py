
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


######
# UsableItem — abstract base for all consumable items
# Demonstrates: Abstract Base Class, polymorphism (different items, same .use() interface)

class UsableItem(ABC):
    @abstractmethod
    def use(self, user, target) -> list[str]: pass


##########
# Vehicle — abstract base for all vehicles
# Demonstrates: Abstract Base Class, composition (Hero *has-a* Vehicle)

class Vehicle(ABC):
    def __init__(self):
        self._used = False

    @property
    def is_used(self): return self._used

    @abstractmethod
    def use(self, user, target) -> list[str]:
        """Use the vehicle ability. Returns log messages."""
        pass

    def _mark_used(self):
        self._used = True

    def recharge(self):
        """Recharge the vehicle so it can be used again."""
        self._used = False
