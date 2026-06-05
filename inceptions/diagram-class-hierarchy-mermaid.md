# Class Hierarchy — UML Class Diagram (Mermaid Backup)

> **Tool**: Mermaid `classDiagram`
> **Purpose**: Mermaid version of the PlantUML class diagram. Slightly less detailed but renders natively in VS Code with the Mermaid extension.

## Diagram

```mermaid
classDiagram
    direction TB

    %% ─── Abstract Base Classes ───

    class GameEntity {
        <<abstract>>
        -_name: str
        -_hp: int
        -_max_hp: int
        +name: str*
        +hp: int*
        +max_hp: int*
        +take_turn(targets) list~str~*
        +is_alive() bool
    }

    class UsableItem {
        <<abstract>>
        +name: str*
        +use(user, target) list~str~*
    }

    class Vehicle {
        <<abstract>>
        -_used: bool
        +is_used: bool*
        +use(user, target) list~str~*
        +recharge()
        #_mark_used()
    }

    %% ─── Hero Classes ───

    class Hero {
        -_speed_boost_active: bool
        +SPEED_BOOST_MULTIPLIER: int = 3
        +attack_power: int
        +inventory: list~UsableItem~
        +vehicle: Vehicle or None
        +is_speed_boosted: bool*
        +has_items() bool
        +has_vehicle_available() bool
        +take_turn(boss) list~str~
        +use_item(item_index, target) list~str~
        +use_vehicle(boss) list~str~
    }

    class Warrior {
        +__init__(name)
        HP: 150, ATK: 15
        Vehicle: Car
        Items: HealthPotion + SpeedBoost
    }

    class Mage {
        +__init__(name)
        HP: 80, ATK: 30
        Vehicle: Boat
        Items: HealthPotion + ManaPotion
    }

    class Archer {
        +__init__(name)
        HP: 100, ATK: 20
        Vehicle: Drone
        Items: ManaPotion + SpeedBoost
    }

    %% ─── Boss ───

    class Boss {
        -_turn_count: int = 0
        +FIRE_BREATH_INTERVAL: int = 2
        +FIRE_BREATH_DAMAGE: int = 20
        +attack_power: int
        +turns_until_fire: int*
        +fire_breath_next: bool*
        +take_turn(heroes) list~str~
    }

    %% ─── Item Subclasses ───

    class HealthPotion {
        -_heal_amount: int = 40
        +name: str*
        +use(user, target) list~str~
    }

    class ManaPotion {
        +name: str*
        +use(user, target) list~str~
    }

    class SpeedBoost {
        +name: str*
        +use(user, target) list~str~
    }

    %% ─── Vehicle Subclasses ───

    class Car {
        +use(user, target) list~str~
    }

    class Boat {
        +use(user, target) list~str~
    }

    class Drone {
        +use(user, target) list~str~
    }

    %% ─── Inheritance ───

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

    %% ─── Composition ───

    Hero *-- Vehicle : has-a 0..1
    Hero *-- UsableItem : has-a 0..*
```

## Notes

- This Mermaid version lacks the `«abstract»` stereotype rendering and method-level visibility icons that PlantUML provides
- Composition arrows (`*--`) are supported but cardinality labels are less precise
- For the most detailed UML representation, prefer the [PlantUML version](diagram-class-hierarchy.md)
