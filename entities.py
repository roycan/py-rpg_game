
import random
from base import GameEntity
from items import HealthPotion, ManaPotion, SpeedBoost
from vehicles import Car, Boat, Drone


# ─── Hero (base class for all heroes) ───
# Demonstrates: inheritance (GameEntity), composition (has-a Vehicle, has-a inventory)

class Hero(GameEntity):
    def __init__(self, name, hp, attack_power):
        super().__init__(name, hp)
        self.attack_power = attack_power
        self.inventory = []
        self.vehicle = None
        self._extra_action = False

    @property
    def has_extra_action(self):
        return self._extra_action

    def clear_extra_action(self):
        self._extra_action = False

    def has_items(self):
        return len(self.inventory) > 0

    def has_vehicle_available(self):
        return self.vehicle is not None and not self.vehicle.is_used

    def take_turn(self, boss):
        """Default attack action. Returns list of log strings."""
        logs = []
        is_crit = random.random() < 0.2
        damage = self.attack_power * 2 if is_crit else self.attack_power
        boss.hp -= damage
        if is_crit:
            logs.append(f"💥 CRITICAL HIT!")
        logs.append(f"⚔️ {self.name} attacks {boss.name} for {damage} damage! ({boss.name}: {boss.hp}/{boss.max_hp} HP)")
        return logs

    def use_item(self, item_index, target):
        """Use an item from inventory. Returns list of log strings."""
        if item_index < 0 or item_index >= len(self.inventory):
            return [f"❌ {self.name} has no item in that slot!"]
        item = self.inventory.pop(item_index)
        return item.use(self, target)

    def use_vehicle(self, boss):
        """Use the hero's vehicle ability. Returns list of log strings."""
        if self.vehicle is None:
            return [f"❌ {self.name} has no vehicle!"]
        return self.vehicle.use(self, boss)


# ─── Hero subclasses ───
# Demonstrates: inheritance, each subclass customizes __init__ with different stats

class Warrior(Hero):
    def __init__(self, name="Warrior"):
        super().__init__(name, hp=150, attack_power=15)
        self.inventory = [HealthPotion(), ManaPotion()]
        self.vehicle = Car()


class Mage(Hero):
    def __init__(self, name="Mage"):
        super().__init__(name, hp=80, attack_power=30)
        self.inventory = [HealthPotion(), SpeedBoost()]
        self.vehicle = Boat()


class Archer(Hero):
    def __init__(self, name="Archer"):
        super().__init__(name, hp=100, attack_power=20)
        self.inventory = [ManaPotion(), SpeedBoost()]
        self.vehicle = Drone()


# ─── Boss ───
# Demonstrates: inheritance (GameEntity), internal state tracking (_turn_count)

class Boss(GameEntity):
    FIRE_BREATH_INTERVAL = 3  # every 3rd turn
    FIRE_BREATH_DAMAGE = 12

    def __init__(self, name="Dragon", hp=400, attack_power=20):
        super().__init__(name, hp)
        self.attack_power = attack_power
        self._turn_count = 0

    @property
    def turns_until_fire(self):
        """How many turns until the next Fire Breath."""
        return self.FIRE_BREATH_INTERVAL - (self._turn_count % self.FIRE_BREATH_INTERVAL)

    @property
    def fire_breath_next(self):
        """True if Fire Breath will happen on the next boss turn."""
        return self.turns_until_fire == 1

    def take_turn(self, heroes):
        """Boss attacks. Returns list of log strings."""
        logs = []
        self._turn_count += 1
        alive_heroes = [h for h in heroes if h.is_alive()]

        if not alive_heroes:
            return logs

        # Fire Breath every N turns
        if self._turn_count % self.FIRE_BREATH_INTERVAL == 0:
            logs.append(f"🔥 {self.name} unleashes FIRE BREATH!")
            for hero in alive_heroes:
                hero.hp -= self.FIRE_BREATH_DAMAGE
                logs.append(f"🔥 {hero.name} takes {self.FIRE_BREATH_DAMAGE} fire damage! ({hero.hp}/{hero.max_hp} HP)")
        else:
            # Normal single-target attack
            target = random.choice(alive_heroes)
            target.hp -= self.attack_power
            logs.append(f"🐉 {self.name} strikes {target.name} for {self.attack_power} damage! ({target.hp}/{target.max_hp} HP)")

        return logs
