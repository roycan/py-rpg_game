"""Tests for a full battle simulation — integration tests."""

import pytest
from entities import Warrior, Mage, Archer, Boss


class TestFullBattle:
    def test_battle_produces_logs(self):
        """A full battle should produce log messages from all actions."""
        heroes = [Warrior("A"), Mage("B"), Archer("C")]
        boss = Boss("Boss", hp=100)
        all_logs = []

        while boss.is_alive() and any(h.is_alive() for h in heroes):
            for hero in heroes:
                if hero.is_alive() and boss.is_alive():
                    all_logs.extend(hero.take_turn(boss))
            if boss.is_alive():
                all_logs.extend(boss.take_turn(heroes))

        assert len(all_logs) > 0
        assert any("attacks" in log for log in all_logs)

    def test_battle_ends_with_winner(self):
        """Battle should end with either heroes or boss victorious."""
        heroes = [Warrior("A"), Mage("B"), Archer("C")]
        boss = Boss("Boss", hp=100)
        turns = 0
        max_turns = 50  # Safety limit

        while boss.is_alive() and any(h.is_alive() for h in heroes) and turns < max_turns:
            turns += 1
            for hero in heroes:
                if hero.is_alive() and boss.is_alive():
                    hero.take_turn(boss)
            if boss.is_alive():
                boss.take_turn(heroes)

        # Exactly one side should be victorious
        boss_dead = not boss.is_alive()
        heroes_dead = not any(h.is_alive() for h in heroes)
        assert boss_dead or heroes_dead
        assert not (boss_dead and heroes_dead)  # Can't both be dead... usually

    def test_fire_breath_timing_in_battle(self):
        """Fire Breath should fire on turns 2, 4, 6, 8..."""
        boss = Boss("Boss", hp=10000)
        heroes = [Warrior("A"), Mage("B")]
        fire_breath_turns = []

        for turn in range(1, 9):
            for hero in heroes:
                if hero.is_alive():
                    hero.take_turn(boss)
            logs = boss.take_turn(heroes)
            if any("FIRE BREATH" in log for log in logs):
                fire_breath_turns.append(turn)

        assert fire_breath_turns == [2, 4, 6, 8]

    def test_heroes_can_use_items_in_battle(self):
        """Heroes should be able to use items during battle."""
        hero = Warrior("Test")
        boss = Boss("Boss", hp=10000)
        hero.hp -= 80  # Damage the hero

        initial_hp = hero.hp
        initial_items = len(hero.inventory)
        logs = hero.use_item(0, hero)  # Use first item (HealthPotion)

        assert hero.hp > initial_hp  # HP went up
        assert len(hero.inventory) == initial_items - 1  # Item consumed

    def test_heroes_can_use_vehicles_in_battle(self):
        """Heroes should be able to use vehicles during battle."""
        hero = Archer("Test")
        boss = Boss("Boss", hp=10000)

        initial_boss_hp = boss.hp
        logs = hero.use_vehicle(boss)  # Drone attack

        assert boss.hp < initial_boss_hp  # Boss took damage from Drone
        assert hero.vehicle.is_used is True

    def test_hp_property_clamping(self):
        """HP should never go below 0 or above max_hp."""
        hero = Warrior("Test")

        # Test upper clamp
        hero.hp += 100
        assert hero.hp == hero.max_hp

        # Test lower clamp
        hero.hp -= 9999
        assert hero.hp == 0
