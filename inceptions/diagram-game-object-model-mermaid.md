# Game Object Model — ERD (Mermaid Backup)

> **Tool**: Mermaid `erDiagram`
> **Purpose**: Mermaid version of the entity-relationship diagram. Focuses on how game objects connect to each other.

## Diagram

```mermaid
erDiagram
    GameEntity {
        string name
        int hp
        int max_hp
    }

    Hero {
        int attack_power
        bool speed_boost_active
    }

    Boss {
        int attack_power
        int turn_count
        int fire_breath_interval
    }

    Warrior {
        int HP_150
        int ATK_15
    }

    Mage {
        int HP_80
        int ATK_30
    }

    Archer {
        int HP_100
        int ATK_20
    }

    UsableItem {
        string name
    }

    HealthPotion {
        int heal_amount_40
    }

    ManaPotion {
        string recharges_vehicle
    }

    SpeedBoost {
        string _3x_damage_next_turn
    }

    Vehicle {
        bool used
    }

    Car {
        string heal_30_HP
    }

    Boat {
        string heal_50_HP
    }

    Drone {
        string deal_60_damage
    }

    %% Inheritance
    GameEntity ||--o| Hero : "extends"
    GameEntity ||--o| Boss : "extends"
    Hero ||--o| Warrior : "is-a"
    Hero ||--o| Mage : "is-a"
    Hero ||--o| Archer : "is-a"
    UsableItem ||--o| HealthPotion : "is-a"
    UsableItem ||--o| ManaPotion : "is-a"
    UsableItem ||--o| SpeedBoost : "is-a"
    Vehicle ||--o| Car : "is-a"
    Vehicle ||--o| Boat : "is-a"
    Vehicle ||--o| Drone : "is-a"

    %% Composition
    Hero ||--o| Vehicle : "has-a"
    Hero ||--o{ UsableItem : "inventory"

    %% Battle
    Hero }o--o{ Boss : "battles"
```

## Notes

- Mermaid ERD doesn't support the `0..1` cardinality notation as precisely as Kroki ERD
- Entity attributes in Mermaid ERD are simpler — they don't support type annotations
- For the most precise ERD, prefer the [Kroki ERD version](diagram-game-object-model.md)
