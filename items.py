
from base import UsableItem

# HealthPotion — restores HP to a target
# Demonstrates: inheritance (UsableItem), encapsulation (heal_amount is private)

class HealthPotion(UsableItem):
    def __init__(self, heal_amount=40):
        self._heal_amount = heal_amount

    @property
    def name(self):
        return "Health Potion"

    def use(self, user, target):
        old_hp = target.hp
        target.hp += self._heal_amount
        actual_heal = target.hp - old_hp
        return [f"🧪 {user.name} uses a {self.name} on {target.name}, restoring {actual_heal} HP! ({target.hp}/{target.max_hp})"]


# ManaPotion — recharges the user's vehicle ability
# Demonstrates: polymorphism (same .use() interface, different behavior)

class ManaPotion(UsableItem):
    @property
    def name(self):
        return "Mana Potion"

    def use(self, user, target):
        if hasattr(target, 'vehicle') and target.vehicle is not None:
            target.vehicle.recharge()
            return [f"🔮 {user.name} uses a {self.name} on {target.name} — {target.vehicle.__class__.__name__} recharged!"]
        return [f"🔮 {user.name} uses a {self.name}, but nothing happened."]


# SpeedBoost — grants an extra action this turn
# Demonstrates: polymorphism, game state change via method call

class SpeedBoost(UsableItem):
    @property
    def name(self):
        return "Speed Boost"

    def use(self, user, target):
        target._speed_boost_active = True
        return [f"⚡ {user.name} uses a {self.name} on {target.name} — 3x damage next turn, immune to attack this turn!"]
