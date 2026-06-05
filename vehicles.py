
from base import Vehicle

# Car — immediate heal (dodge recovery)
# Demonstrates: inheritance (Vehicle), single-use via _mark_used()

class Car(Vehicle):
    def use(self, user, target):
        if self._used:
            return [f"🚗 {user.name}'s Car has already been used this battle!"]
        heal = 30
        old_hp = user.hp
        user.hp += heal
        actual = user.hp - old_hp
        self._mark_used()
        return [f"🚗 {user.name} speeds away in the Car, recovering {actual} HP! ({user.hp}/{user.max_hp})"]


# Boat — retreat and heal
# Demonstrates: same interface as Car but different behavior (polymorphism)

class Boat(Vehicle):
    def use(self, user, target):
        if self._used:
            return [f"⛵ {user.name}'s Boat has already been used this battle!"]
        heal = 50
        old_hp = user.hp
        user.hp += heal
        actual = user.hp - old_hp
        self._mark_used()
        return [f"⛵ {user.name} sails away on the Boat, resting and recovering {actual} HP! ({user.hp}/{user.max_hp})"]


# Drone — bomb the enemy
# Demonstrates: same interface, offensive instead of defensive

class Drone(Vehicle):
    def use(self, user, target):
        if self._used:
            return [f"🛩️ {user.name}'s Drone has already been used this battle!"]
        damage = 60
        target.hp -= damage
        self._mark_used()
        return [f"🛩️ {user.name} launches the Drone — it bombs {target.name} for {damage} damage! ({target.name}: {target.hp}/{target.max_hp} HP)"]
