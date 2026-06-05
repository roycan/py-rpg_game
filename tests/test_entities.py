"""Tests for entities.py — Hero subclasses and Boss."""

import pytest
from entities import Warrior, Mage, Archer, Boss, Hero
from base import GameEntity


class TestHeroCreation:
    def test_warrior_stats(self):
        w = Warrior("Thorin")
        assert w.name == "Thorin"
        assert w.max_hp == 150
        assert w.hp == 150
        assert w.attack_power == 15
        assert len(w.inventory) == 2
        assert w.vehicle is not None

    def test_mage_stats(self):
        m = Mage("Gandalf")
        assert m.name == "Gandalf"
        assert m.max_hp == 80
        assert m.attack_power == 30
        assert len(m.inventory) == 2
        assert m.vehicle is not None

    def test_archer_stats(self):
        a = Archer("Legolas")
        assert a.name == "Legolas"
        assert a.max_hp == 100
        assert a.attack_power == 20
        assert len(a.inventory) == 2
        assert a.vehicle is not None

    def test_default_names(self):
        assert Warrior().name == "Warrior"
        assert Mage().name == "Mage"
        assert Archer().name == "Archer"


class TestHeroActions:
    def test_attack_returns_logs(self):
        hero = Warrior("Test")
        boss = Boss("TestBoss", hp=550)
        logs = hero.take_turn(boss)
        assert isinstance(logs, list)
        assert len(logs) >= 1
        assert "Test" in logs[-1]
        assert boss.hp < 550  # Boss took damage

    def test_critical_hit_does_double_damage(self):
        hero = Warrior("Test")
        boss = Boss("TestBoss", hp=1000)

        # Force a crit by checking many turns
        found_crit = False
        for _ in range(200):
            boss.hp = 1000
            logs = hero.take_turn(boss)
            if "CRITICAL" in logs[0]:
                assert boss.hp == 1000 - 30  # 15 * 2
                found_crit = True
                break
        assert found_crit, "Should get at least one critical hit in 200 tries"

    def test_use_item_removes_from_inventory(self):
        hero = Warrior("Test")
        initial_count = len(hero.inventory)
        logs = hero.use_item(0, hero)
        assert len(hero.inventory) == initial_count - 1
        assert isinstance(logs, list)

    def test_use_invalid_item_index(self):
        hero = Warrior("Test")
        logs = hero.use_item(99, hero)
        assert "no item" in logs[0].lower()

    def test_use_vehicle(self):
        hero = Archer("Test")
        boss = Boss("TestBoss", hp=550)
        logs = hero.use_vehicle(boss)
        assert isinstance(logs, list)
        assert len(logs) >= 1
        assert hero.vehicle.is_used is True

    def test_has_vehicle_available(self):
        hero = Warrior("Test")
        assert hero.has_vehicle_available() is True
        hero.vehicle._mark_used()
        assert hero.has_vehicle_available() is False


class TestHeroLifeDeath:
    def test_is_alive(self):
        hero = Warrior("Test")
        assert hero.is_alive() is True

    def test_dies_at_zero_hp(self):
        hero = Warrior("Test")
        hero.hp -= 200
        assert hero.hp == 0
        assert hero.is_alive() is False

    def test_hp_clamped_at_zero(self):
        hero = Warrior("Test")
        hero.hp -= 9999
        assert hero.hp == 0


class TestBoss:
    def test_boss_creation(self):
        boss = Boss("Smaug", hp=550)
        assert boss.name == "Smaug"
        assert boss.hp == 550
        assert boss.attack_power == 25

    def test_boss_single_attack(self):
        boss = Boss("TestBoss", hp=550)
        heroes = [Warrior("A"), Mage("B"), Archer("C")]
        logs = boss.take_turn(heroes)
        assert isinstance(logs, list)
        assert len(logs) >= 1
        # At least one hero took damage
        total_damage = sum(h.max_hp - h.hp for h in heroes)
        assert total_damage > 0

    def test_fire_breath_every_second_turn(self):
        boss = Boss("TestBoss", hp=550)
        heroes = [Warrior("A"), Mage("B"), Archer("C")]

        # Turn 1: normal
        logs1 = boss.take_turn(heroes)
        assert not any("FIRE BREATH" in log for log in logs1)

        # Turn 2: Fire Breath!
        logs2 = boss.take_turn(heroes)
        assert any("FIRE BREATH" in log for log in logs2)

        # Turn 3: normal
        logs3 = boss.take_turn(heroes)
        assert not any("FIRE BREATH" in log for log in logs3)

        # Turn 4: Fire Breath!
        logs4 = boss.take_turn(heroes)
        assert any("FIRE BREATH" in log for log in logs4)

    def test_fire_breath_hits_all_alive(self):
        boss = Boss("TestBoss", hp=550)
        heroes = [Warrior("A"), Mage("B")]

        # Do 1 normal turn
        boss.take_turn(heroes)

        # Reset HP to known values
        heroes[0].hp = 150
        heroes[1].hp = 80

        # Turn 2: Fire Breath
        logs = boss.take_turn(heroes)
        assert heroes[0].hp == 150 - 20  # 130
        assert heroes[1].hp == 80 - 20   # 60

    def test_fire_breath_timing_property(self):
        boss = Boss("TestBoss", hp=550)
        assert boss.turns_until_fire == 2
        assert boss.fire_breath_next is False

        boss.take_turn([Warrior("A")])  # Turn 1
        assert boss.turns_until_fire == 1
        assert boss.fire_breath_next is True

        boss.take_turn([Warrior("A")])  # Turn 2 (Fire Breath)
        assert boss.turns_until_fire == 2
        assert boss.fire_breath_next is False

    def test_boss_skips_dead_heroes(self):
        boss = Boss("TestBoss", hp=550)
        heroes = [Warrior("A")]
        heroes[0].hp = 0  # Dead
        logs = boss.take_turn(heroes)
        assert len(logs) == 0  # No action when all dead
