# Battle Turn Sequence — Sequence Diagram (Mermaid Backup)

> **Tool**: Mermaid `sequenceDiagram`
> **Purpose**: Mermaid version of the PlantUML sequence diagram. Simplified to fit Mermaid's capabilities.

## Diagram

```mermaid
sequenceDiagram
    autonumber
    participant P as Player/AI
    participant UI as UI Layer
    participant H as Hero
    participant B as Boss
    participant V as Vehicle
    participant I as Item

    rect rgb(230, 240, 255)
    Note over P,UI: Turn Start
    P->>UI: Trigger next turn
    UI->>UI: turn_number++
    end

    rect rgb(230, 255, 230)
    Note over H,B: Hero Phase - per alive hero

    alt Manual Mode
        P->>UI: Select action from form
    else Auto Mode
        UI->>UI: auto_pick_action - decision tree
    end

    alt Action: Attack
        UI->>H: take_turn - boss
        H->>H: roll crit + check speed boost
        H->>B: boss.hp -= damage
        H-->>UI: log messages
    else Action: Use Item
        UI->>H: use_item - index, hero
        H->>I: item.use - hero, hero
        I-->>H: log messages
        H-->>UI: log messages
    else Action: Use Vehicle
        UI->>H: use_vehicle - boss
        H->>V: vehicle.use - hero, boss
        V->>V: _mark_used
        V-->>H: log messages
        H-->>UI: log messages
    end
    end

    rect rgb(255, 230, 230)
    Note over B,H: Boss Phase
    alt Boss alive
        UI->>B: take_turn - heroes
        B->>B: _turn_count++
        alt Fire Breath Turn - every 2nd
            loop Each alive hero
                B->>H: hero.hp -= 20
            end
        else Normal Attack
            B->>H: target.hp -= 30
        end
        B-->>UI: log messages
    end
    end

    rect rgb(255, 255, 220)
    Note over P,UI: Turn End
    alt Boss dead
        UI-->>P: Victory screen
    else All heroes dead
        UI-->>P: Defeat screen
    else Battle continues
        UI-->>P: Render updated state
    end
    end
```

## Notes

- Mermaid sequence diagrams lack the detailed note formatting and autonumber features of PlantUML
- The `alt`/`loop` blocks work but are less visually distinct
- For the most detailed sequence diagram, prefer the [PlantUML version](diagram-battle-turn-sequence.md)
