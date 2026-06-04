
import random
from base import GameEntity
from items import HealthPotion

class Hero(GameEntity):
    def __init__(self, name, hp, attack_power):
        super().__init__(name, hp)
        self.attack_power = attack_power
        self.inventory = [HealthPotion()]

    def take_turn(self, boss):
        print(f"\n--- {self.name}'s Turn ---")
        is_crit = random.random() < 0.2
        damage = self.attack_power * 2 if is_crit else self.attack_power
        if is_crit: print("CRITICAL HIT!")
        boss.hp -= damage
        print(f"{self.name} deals {damage} damage to {boss.name}!")

class Warrior(Hero):
    def __init__(self, name="Warrior"): super().__init__(name, hp=150, attack_power=15)

class Mage(Hero):
    def __init__(self, name="Mage"): super().__init__(name, hp=80, attack_power=30)

class Archer(Hero):
    def __init__(self, name="Archer"): super().__init__(name, hp=100, attack_power=20)

class Boss(GameEntity):
    def __init__(self, name="Dragon", hp=350, attack_power=20):
        super().__init__(name, hp)
        self.attack_power = attack_power

    def take_turn(self, players):
        alive_players = [p for p in players if p.is_alive()]
        if alive_players:
            target = random.choice(alive_players)
            target.hp -= self.attack_power
            print(f"\n{self.name} strikes! {target.name} takes {self.attack_power} damage.")
