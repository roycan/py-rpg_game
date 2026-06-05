# Module Architecture — Dependency Graph

> **Tool**: Mermaid `graph TD`
> **Purpose**: Shows how all Python modules import and depend on each other. This is the "big picture" of the project structure.

## How to Read This

- Arrows point **from importer → imported** (e.g. `entities.py → base.py` means entities imports from base)
- The two entry points (`app.py` and `main.py`) sit at the top
- Abstract base classes (`base.py`) sit at the bottom — everything depends on them
- `tests/` imports all game modules but is not imported by anything

## Diagram

```mermaid
graph TD
    %% Entry Points
    app["app.py<br/><i>Streamlit Web UI</i>"]
    main["main.py<br/><i>CLI Game Loop</i>"]

    %% Core Game Logic
    entities["entities.py<br/><i>Hero, Warrior, Mage, Archer, Boss</i>"]
    items["items.py<br/><i>HealthPotion, ManaPotion, SpeedBoost</i>"]
    vehicles["vehicles.py<br/><i>Car, Boat, Drone</i>"]
    base["base.py<br/><i>GameEntity, UsableItem, Vehicle — ABCs</i>"]

    %% Tests
    tests["tests/<br/><i>52 pytest tests</i>"]

    %% Dependencies
    app --> entities
    main --> entities

    entities --> base
    entities --> items
    entities --> vehicles

    items --> base
    vehicles --> base

    tests -.-> entities
    tests -.-> items
    tests -.-> vehicles
    tests -.-> base

    %% Styling
    classDef entry fill:#4a90d9,stroke:#2c5f8a,color:#fff
    classDef core fill:#6b8e23,stroke:#4a6318,color:#fff
    classDef base fill:#9b59b6,stroke:#6c3483,color:#fff
    classDef test fill:#e67e22,stroke:#b35c18,color:#fff

    class app,main entry
    class entities,items,vehicles core
    class base base
    class tests test
```

## Key Takeaways

1. **`base.py` is the foundation** — all game logic depends on its ABCs
2. **`entities.py` is the central hub** — it imports from all three base modules
3. **`items.py` and `vehicles.py` are independent** — they only depend on `base.py`, not on each other
4. **`app.py` and `main.py` are interchangeable UIs** — both depend only on `entities.py`
5. **Separation of concerns** — UI layer → game logic layer → abstract base layer
