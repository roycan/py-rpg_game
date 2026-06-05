# Battle Turn Sequence — Sequence Diagram

> **Tool**: PlantUML
> **Purpose**: Shows the method call chain and message flow during a single canonical battle turn. Demonstrates how objects interact at runtime.

## How to Read This

- **Participants** (top boxes) = the objects involved
- **Solid arrows** = method calls
- **Dashed arrows** = return values
- **`alt`/`opt`/`loop` blocks** = conditional branches
- This diagram shows a canonical turn: one hero attacks, then boss responds

## Diagram

```plantuml
@startuml
title Battle Turn — Sequence Diagram\n(Canonical: Hero Attacks, Boss Responds)

autonumber

participant "Player / AI" as Player
participant "UI Layer\n(app.py / main.py)" as UI
participant "Hero\n(e.g. Warrior)" as Hero
participant "Boss\n(Smaug)" as Boss
participant "Hero's Vehicle" as Vehicle
participant "Hero's Item" as Item

== Turn Start ==

Player -> UI : Trigger next turn
UI -> UI : turn_number++
UI -> UI : Log "=== Turn N ==="

== Hero Phase (per alive hero) ==

alt Manual Mode
    Player -> UI : Select action for hero
    UI -> UI : Read form selectbox
else Auto Mode
    UI -> UI : auto_pick_action(hero)
    note right of UI
        Decision tree:
        1. HP < 40% + has HealthPotion → use item
        2. HP < 60% + vehicle ready → use vehicle
        3. Has SpeedBoost + 25% chance → use item
        4. Default → attack
    end note
end

alt Action: Attack
    UI -> Hero : take_turn(boss)
    Hero -> Hero : roll crit (20% chance)
    Hero -> Hero : check _speed_boost_active
    alt Speed Boost Active
        Hero -> Hero : damage *= 3
        Hero -> Hero : _speed_boost_active = False
    end
    Hero -> Boss : boss.hp -= damage
    Hero --> UI : [crit msg, attack msg]

else Action: Use Item
    UI -> Hero : use_item(index, hero)
    Hero -> Hero : inventory.pop(index)
    Hero -> Item : item.use(hero, hero)
    note right of Item
        HealthPotion → heal 40 HP
        ManaPotion → recharge vehicle
        SpeedBoost → set _speed_boost_active
    end note
    Item --> Hero : [log messages]
    Hero --> UI : [log messages]

else Action: Use Vehicle
    UI -> Hero : use_vehicle(boss)
    Hero -> Vehicle : vehicle.use(hero, boss)
    note right of Vehicle
        Car → heal 30 HP to hero
        Boat → heal 50 HP to hero
        Drone → deal 60 dmg to boss
    end note
    Vehicle -> Vehicle : _mark_used()
    Vehicle --> Hero : [log messages]
    Hero --> UI : [log messages]
end

UI -> UI : add_logs(messages)

== Boss Phase ==

alt Boss is Alive
    UI -> Boss : take_turn(heroes)
    Boss -> Boss : _turn_count++
    Boss -> Boss : Filter alive heroes

    alt Fire Breath Turn (every 2nd)
        Boss -> Boss : AoE: 20 dmg to ALL alive heroes
        loop Each alive hero
            Boss -> Hero : hero.hp -= 20
        end
        Boss --> UI : [Fire Breath messages]
    else Normal Attack
        Boss -> Boss : Filter non-speed-boosted heroes
        alt Valid targets exist
            Boss -> Boss : random.choice(valid_targets)
            Boss -> Hero : target.hp -= 30
            Boss --> UI : [attack message]
        else All heroes boosted
            Boss --> UI : ["all heroes too fast!"]
        end
    end

    UI -> UI : add_logs(boss_messages)
end

== Turn End ==

UI -> UI : Check game over
alt Boss dead
    UI --> Player : Victory screen
else All heroes dead
    UI --> Player : Defeat screen
else Battle continues
    UI -> Player : Render updated state
end

@enduml
```

![alt text](diagram-battle-turn-sequence.png)

## Key Interactions

| From | To | Method | Returns |
|------|----|--------|---------|
| UI | Hero | `take_turn(boss)` | `list[str]` — log messages |
| UI | Hero | `use_item(index, hero)` | `list[str]` — log messages |
| UI | Hero | `use_vehicle(boss)` | `list[str]` — log messages |
| UI | Boss | `take_turn(heroes)` | `list[str]` — log messages |
| Hero | Item | `item.use(hero, hero)` | `list[str]` — log messages |
| Hero | Vehicle | `vehicle.use(hero, boss)` | `list[str]` — log messages |

## Design Pattern: `list[str]` Return

Every game logic method returns `list[str]` instead of calling `print()` directly. This is the **Separation of Concerns** pattern:

- **Game logic** (entities, items, vehicles) produces messages
- **UI layer** (app.py, main.py) decides how to display them
- Same logic works in both Streamlit and CLI
