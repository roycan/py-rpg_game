
from base import UsableItem

class HealthPotion(UsableItem):
    def __init__(self, heal_amount=40):
        self.heal_amount = heal_amount

    def use(self, user, target):
        old_hp = target.hp
        target.hp += self.heal_amount
        actual_heal = target.hp - old_hp
        print(f"{user.name} uses a Health Potion on {target.name}, restoring {actual_heal} HP!")
