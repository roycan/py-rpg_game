"""Tests for items.py — HealthPotion, ManaPotion, SpeedBoost."""

import pytest
from entities import Warrior, Mage, Archer, Boss
from items import HealthPotion, ManaPotion, SpeedBoost


class TestHealthPotion:
    def test_heals_target(self):
        warrior = Warrior("TestWarrior")
        warrior.hp -= 60  # Take damage: 150 → 90
        potion = HealthPotion(heal_amount=40)
        logs = potion.use(warrior, warrior)
        assert warrior.hp == 130  # 90 + 40

    def test_returns_log_strings(self):
        warrior = Warrior("TestWarrior")
        warrior.hp -= 20
        potion = HealthPotion()
        logs = potion.use(warrior, warrior)
        assert isinstance(logs, list)
        assert len(logs) == 1
        assert "Health Potion" in logs[0]
        assert "TestWarrior" in logs[0]

    def test_clamped_at_max_hp(self):
        warrior = Warrior("TestWarrior")
        # HP is already at max (150), healing should not exceed max
        potion = HealthPotion(heal_amount=40)
        potion.use(warrior, warrior)
        assert warrior.hp == warrior.max_hp  # Still 150

    def test_custom_heal_amount(self):
        warrior = Warrior("TestWarrior")
        warrior.hp -= 80
        potion = HealthPotion(heal_amount=100)
        potion.use(warrior, warrior)
        assert warrior.hp == 150  # 70 + 100 capped at 150


class TestManaPotion:
    def test_recharges_vehicle(self):
        archer = Archer("TestArcher")
        # Use the vehicle first
        assert archer.vehicle is not None
        archer.vehicle._mark_used()
        assert archer.vehicle.is_used is True

        potion = ManaPotion()
        logs = potion.use(archer, archer)
        assert archer.vehicle is not None
        assert archer.vehicle.is_used is False
        assert "recharged" in logs[0].lower()

    def test_returns_log_when_no_vehicle(self):
        warrior = Warrior("TestWarrior")
        warrior.vehicle = None
        potion = ManaPotion()
        logs = potion.use(warrior, warrior)
        assert "nothing happened" in logs[0].lower()


class TestSpeedBoost:
    def test_grants_speed_boost(self):
        mage = Mage("TestMage")
        assert mage.is_speed_boosted is False
        boost = SpeedBoost()
        logs = boost.use(mage, mage)
        assert mage.is_speed_boosted is True
        assert "3x damage" in logs[0]
        assert "immune" in logs[0].lower()

    def test_speed_boost_cleared_after_attack(self):
        hero = Warrior("Test")
        boss = Boss("TestBoss", hp=10000)
        boost = SpeedBoost()
        boost.use(hero, hero)
        assert hero.is_speed_boosted is True
        hero.take_turn(boss)  # Attack consumes the speed boost
        assert hero.is_speed_boosted is False
