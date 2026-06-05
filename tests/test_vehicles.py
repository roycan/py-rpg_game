"""Tests for vehicles.py — Car, Boat, Drone."""

import pytest
from entities import Warrior, Mage, Archer, Boss
from vehicles import Car, Boat, Drone


class TestCar:
    def test_heals_hero(self):
        warrior = Warrior("TestWarrior")
        warrior.hp -= 60  # 150 → 90
        car = Car()
        logs = car.use(warrior, None)
        assert warrior.hp == 120  # 90 + 30
        assert "Car" in logs[0]
        assert "30" in logs[0]

    def test_single_use(self):
        car = Car()
        assert car.is_used is False
        warrior = Warrior("TestWarrior")
        car.use(warrior, None)
        assert car.is_used is True

    def test_cannot_use_twice(self):
        car = Car()
        warrior = Warrior("TestWarrior")
        car.use(warrior, None)
        logs = car.use(warrior, None)
        assert "already been used" in logs[0]

    def test_recharge(self):
        car = Car()
        car._mark_used()
        assert car.is_used is True
        car.recharge()
        assert car.is_used is False


class TestBoat:
    def test_heals_hero(self):
        mage = Mage("TestMage")
        mage.hp -= 60  # 80 → 20
        boat = Boat()
        logs = boat.use(mage, None)
        assert mage.hp == 70  # 20 + 50
        assert "Boat" in logs[0]

    def test_single_use(self):
        boat = Boat()
        mage = Mage("TestMage")
        assert boat.is_used is False
        boat.use(mage, None)
        assert boat.is_used is True


class TestDrone:
    def test_deals_damage_to_boss(self):
        boss = Boss("TestBoss", hp=400)
        drone = Drone()
        archer = Archer("TestArcher")
        logs = drone.use(archer, boss)
        assert boss.hp == 340  # 400 - 60
        assert "60" in logs[0]
        assert "Drone" in logs[0]

    def test_single_use(self):
        drone = Drone()
        boss = Boss("TestBoss", hp=400)
        archer = Archer("TestArcher")
        assert drone.is_used is False
        drone.use(archer, boss)
        assert drone.is_used is True

    def test_cannot_use_twice(self):
        drone = Drone()
        boss = Boss("TestBoss", hp=400)
        archer = Archer("TestArcher")
        drone.use(archer, boss)
        logs = drone.use(archer, boss)
        assert "already been used" in logs[0]
