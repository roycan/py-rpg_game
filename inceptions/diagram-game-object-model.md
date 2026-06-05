# Game Object Model — Entity Relationship Diagram

> **Tool**: Kroki ERD
> **Purpose**: Shows the composition and data relationships between game objects. Complements the class diagram by focusing on *what entities exist and how they connect* rather than class details.

## How to Read This

- Entity names match the Python class names
- Relationships use standard ERD notation:
  - `||--|{` = one-to-many (required)
  - `||--o{` = one-to-many (optional)
  - `||--o|` = one-to-one (optional)
- Attribute types match Python type hints

## Diagram

```erd
[GameEntity]
*name
hp
max_hp
take_turn
is_alive

[Hero]
*name
attack_power
speed_boost_active
has_items
has_vehicle_available
use_item
use_vehicle

[Boss]
*name
attack_power
turn_count
fire_breath_interval
fire_breath_damage
turns_until_fire
fire_breath_next

[Warrior]
*name
hp
atk

[Mage]
*name
hp
atk

[Archer]
*name
hp
atk

[UsableItem]
*name
use

[HealthPotion]
heal_amount

[ManaPotion]
recharges_vehicle

[SpeedBoost]
triple_damage
immune_to_attack

[Vehicle]
name
is_used
use
recharge

[Car]
heal_HP

[Boat]
heal_HP

[Drone]
deal_damage

# Inheritance
GameEntity 1--* Hero
GameEntity 1--1 Boss
Hero 1--* Warrior
Hero 1--* Mage
Hero 1--* Archer
UsableItem 1--* HealthPotion
UsableItem 1--* ManaPotion
UsableItem 1--* SpeedBoost
Vehicle 1--* Car
Vehicle 1--* Boat
Vehicle 1--* Drone

# Composition
Hero *--1 Vehicle
Hero 1--* UsableItem

# Battle
Hero *--1 Boss
```

## Relationship Summary

| Relationship | Type | Description |
|-------------|------|-------------|
| Hero → Vehicle | Composition (0..1) | Each hero may have one vehicle, owned exclusively |
| Hero → UsableItem | Composition (0..*) | Each hero has an inventory of consumable items |
| Hero → GameEntity | Inheritance | Hero is a GameEntity |
| Boss → GameEntity | Inheritance | Boss is a GameEntity |
| Warrior/Mage/Archer → Hero | Inheritance | Each is a specialized Hero |
| HealthPotion/ManaPotion/SpeedBoost → UsableItem | Inheritance | Each is a specialized item |
| Car/Boat/Drone → Vehicle | Inheritance | Each is a specialized vehicle |
| Hero ↔ Boss | Battle | Heroes fight the boss (runtime interaction, not ownership) |

## Default Loadouts

| Hero | HP | ATK | Vehicle | Items |
|------|----|----|---------|-------|
| Warrior | 150 | 15 | Car (heal 30) | HealthPotion, SpeedBoost |
| Mage | 80 | 30 | Boat (heal 50) | HealthPotion, ManaPotion |
| Archer | 100 | 20 | Drone (60 dmg) | ManaPotion, SpeedBoost |
| **Boss** | **600** | **30** | — | — |
