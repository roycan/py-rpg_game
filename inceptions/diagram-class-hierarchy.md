# Class Hierarchy — UML Class Diagram

> **Tool**: PlantUML
> **Purpose**: Full UML class diagram showing all classes, their attributes, methods, inheritance (extends), and composition (has-a) relationships.

## How to Read This

- **Dashed arrows** (`..|>`) = inheritance (extends / "is-a")
- **Solid diamonds** (`*--`) = composition ("has-a", owned part)
- **«abstract»** = abstract base class, cannot be instantiated
- **`+`** = public, **`-`** = private, **`#`** = protected
- **Italic methods** = abstract methods (must be overridden)

## Diagram

```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam classFontSize 13
skinparam defaultFontSize 12
skinparam shadowing false
skinparam linetype ortho

title RPG Battle Arena — Class Hierarchy

' ─── Abstract Base Classes ───

abstract class GameEntity {
    - _name: str
    - _hp: int
    - _max_hp: int
    + name: str <<property>>
    + hp: int <<property>>
    + max_hp: int <<property>>
    + hp = value <<setter, clamped 0..max>>
    + {abstract} take_turn(targets) list[str]
    + is_alive() bool
}

abstract class UsableItem {
    + {abstract} name: str <<property>>
    + {abstract} use(user, target) list[str]
}

abstract class Vehicle {
    - _used: bool
    + is_used: bool <<property>>
    + {abstract} use(user, target) list[str]
    + recharge() void
    # _mark_used() void
}

' ─── Hero Classes ───

class Hero {
    - _speed_boost_active: bool
    + SPEED_BOOST_MULTIPLIER: int = 3
    + attack_power: int
    + inventory: list[UsableItem]
    + vehicle: Vehicle | None
    + is_speed_boosted: bool <<property>>
    + has_items() bool
    + has_vehicle_available() bool
    + take_turn(boss) list[str]
    + use_item(item_index, target) list[str]
    + use_vehicle(boss) list[str]
}

class Warrior {
    + __init__(name = "Warrior")
    ' hp=150, atk=15, Car, HealthPotion+SpeedBoost
}

class Mage {
    + __init__(name = "Mage")
    ' hp=80, atk=30, Boat, HealthPotion+ManaPotion
}

class Archer {
    + __init__(name = "Archer")
    ' hp=100, atk=20, Drone, ManaPotion+SpeedBoost
}

' ─── Boss ───

class Boss {
    - _turn_count: int = 0
    + FIRE_BREATH_INTERVAL: int = 2
    + FIRE_BREATH_DAMAGE: int = 20
    + attack_power: int
    + turns_until_fire: int <<property>>
    + fire_breath_next: bool <<property>>
    + take_turn(heroes) list[str]
}

' ─── Item Subclasses ───

class HealthPotion {
    - _heal_amount: int = 40
    + name: str <<property>>
    + use(user, target) list[str]
}

class ManaPotion {
    + name: str <<property>>
    + use(user, target) list[str]
}

class SpeedBoost {
    + name: str <<property>>
    + use(user, target) list[str]
}

' ─── Vehicle Subclasses ───

class Car {
    + use(user, target) list[str]
    ' heal 30 HP to user
}

class Boat {
    + use(user, target) list[str]
    ' heal 50 HP to user
}

class Drone {
    + use(user, target) list[str]
    ' deal 60 damage to target
}

' ─── Inheritance ───

GameEntity <|-- Hero
GameEntity <|-- Boss

Hero <|-- Warrior
Hero <|-- Mage
Hero <|-- Archer

UsableItem <|-- HealthPotion
UsableItem <|-- ManaPotion
UsableItem <|-- SpeedBoost

Vehicle <|-- Car
Vehicle <|-- Boat
Vehicle <|-- Drone

' ─── Composition ───

Hero *-- "0..1" Vehicle : has-a
Hero *-- "0..*" UsableItem : has-a inventory

' ─── Notes ───

note right of Warrior
    **HP**: 150
    **ATK**: 15
    **Vehicle**: Car (heal 30)
    **Items**: HealthPotion, SpeedBoost
end note

note right of Mage
    **HP**: 80
    **ATK**: 30
    **Vehicle**: Boat (heal 50)
    **Items**: HealthPotion, ManaPotion
end note

note right of Archer
    **HP**: 100
    **ATK**: 20
    **Vehicle**: Drone (60 dmg)
    **Items**: ManaPotion, SpeedBoost
end note

note right of Boss
    **HP**: 600
    **ATK**: 30
    **Fire Breath**: 20 dmg to ALL
    every 2nd turn
    Skips speed-boosted heroes
end note

@enduml
```

![](diagram-class-hierarchy.png)

## OOP Concepts Demonstrated

| Concept | Where to See It |
|---------|----------------|
| **Inheritance** | `Hero` and `Boss` extend `GameEntity`; `Warrior/Mage/Archer` extend `Hero` |
| **Abstract Base Class** | `GameEntity`, `UsableItem`, `Vehicle` define interfaces that subclasses must implement |
| **Composition** | `Hero` *has-a* `Vehicle` (0..1) and *has-a* inventory of `UsableItem` (0..*) |
| **Polymorphism** | All items share `.use()` interface but behave differently; all vehicles share `.use()` interface |
| **Encapsulation** | Private attributes (`_hp`, `_used`, `_speed_boost_active`) with public property getters |
| **Class Constants** | `SPEED_BOOST_MULTIPLIER`, `FIRE_BREATH_INTERVAL`, `FIRE_BREATH_DAMAGE` |
