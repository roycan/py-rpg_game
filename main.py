from entities import Warrior, Mage, Archer, Boss
import random

def play_rpg():
    players = [Warrior("Thorin"), Mage("Gandalf"), Archer("Legolas")]
    boss = Boss("Smaug", hp=300)

    print(f"--- {boss.name} has appeared! ---")

    while boss.is_alive() and any(p.is_alive() for p in players):
        # Sort players by current HP for turn order
        turn_order = sorted([p for p in players if p.is_alive()], key=lambda x: x.hp)

        for hero in turn_order:
            if boss.is_alive():
                hero.take_turn(boss)

        if boss.is_alive():
            boss.take_turn(players)

    if boss.hp <= 0:
        print("\nVICTORY! The party has triumphed!")
    else:
        print("\nGAME OVER! The party has been wiped out.")

if __name__ == "__main__":
    play_rpg()
