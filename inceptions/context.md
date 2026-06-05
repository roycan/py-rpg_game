# RPG Battle Arena — Project Context

> **Purpose**: This document serves as a "second brain" for AI-assisted coding sessions. Read this first to get full context on the project without needing to read every source file.

---

## Project Identity

- **Name**: RPG Battle Arena
- **Type**: Educational Python OOP project (grade 9 students)
- **Stack**: Python 3.10+, Streamlit (web UI), pytest (testing)
- **Repo**: `/home/sirroy/Documents/Git-projs/py-rpg_game`
- **Goal**: Teach Object-Oriented Programming through a fun turn-based RPG battle game

---

## Architecture Overview

### Design Pattern: Separation of Concerns

All game logic methods return `list[str]` log messages. They never call `print()` directly. The caller (`app.py` or `main.py`) decides how to display them.

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  base.py     │     │  items.py     │     │ vehicles.py   │
│  ABC classes │◄────│  UsableItem   │     │  Vehicle      │
│  GameEntity  │     │  subclasses   │     │  subclasses   │
│  UsableItem  │     └──────────────┘     └──────────────┘
│  Vehicle     │              ▲                    ▲
└──────┬───────┘              │                    │
       │                      │                    │
       ▼                      │                    │
┌─────────────────────────────┴────────────────────┴──┐
│  entities.py                                         │
│  Hero (base) → Warrior, Mage, Archer                 │
│  Boss (with Fire Breath mechanic)                    │
│  Hero has-a Vehicle, Hero has-a list[UsableItem]     │
└───────────────────────┬──────────────────────────────┘
                        │ returns list[str]
               ┌────────┴────────┐
               ▼                 ▼
       ┌──────────────┐  ┌──────────────┐
       │  app.py       │  │  main.py      │
       │  Streamlit UI │  │  CLI version  │
       │  session_state│  │  print/input  │
       └──────────────┘  └──────────────┘
```

### Class Hierarchy

```
GameEntity (ABC)
├── Hero → Warrior (150 HP, 15 ATK, Car, HealthPotion+ManaPotion)
├── Hero → Mage (80 HP, 30 ATK, Boat, HealthPotion+SpeedBoost)
├── Hero → Archer (100 HP, 20 ATK, Drone, ManaPotion+SpeedBoost)
└── Boss (400 HP, 20 ATK, Fire Breath every 3rd turn)

UsableItem (ABC)
├── HealthPotion (heal 40 HP)
├── ManaPotion (recharge vehicle)
└── SpeedBoost (grant extra action)

Vehicle (ABC, single-use per battle, rechargeable)
├── Car (heal 30 HP)
├── Boat (heal 50 HP)
└── Drone (60 damage to boss)
```

---

## File Guide

| File | Lines | Role | Key Classes/Functions |
|------|-------|------|----------------------|
| `base.py` | ~55 | Abstract base classes | `GameEntity`, `UsableItem`, `Vehicle` |
| `items.py` | ~48 | Consumable items | `HealthPotion`, `ManaPotion`, `SpeedBoost` |
| `vehicles.py` | ~35 | Vehicle abilities | `Car`, `Boat`, `Drone` |
| `entities.py` | ~85 | Game entities | `Hero`, `Warrior`, `Mage`, `Archer`, `Boss` |
| `app.py` | ~170 | Streamlit web UI | Dual-mode (Auto/Manual), battle log, session state |
| `main.py` | ~100 | CLI game loop | `play_rpg()`, `choose_action()`, `execute_hero_action()` |
| `tests/` | ~300 | pytest suite | 42 tests across 4 files |
| `requirements.txt` | 2 | Dependencies | streamlit, pytest |
| `README.md` | — | User documentation | Setup, OOP concepts, game mechanics |

---

## Game Balance

### Hero Party
- **Warrior**: 150 HP, 15 ATK, Car (heal 30), HealthPotion + ManaPotion
- **Mage**: 80 HP, 30 ATK, Boat (heal 50), HealthPotion + SpeedBoost
- **Archer**: 100 HP, 20 ATK, Drone (60 dmg), ManaPotion + SpeedBoost
- Combined DPR: ~65/round, 20% crit chance for 2x damage
- Total HP pool: 330 + ~195 healing/dodge resources

### Boss — Smaug
- 400 HP, 20 ATK (single target, random hero)
- Fire Breath: every 3rd turn, 12 damage to ALL alive heroes
- `turns_until_fire` and `fire_breath_next` properties for UI warnings

### Expected Balance
- Heroes win ~80% in Manual mode (smart choices)
- Heroes win ~50-60% in Auto mode (AI decision tree)
- Bad item/vehicle usage → likely loss
- Fire Breath creates "tick-tock" tension pattern

---

## Streamlit UI Details

### Session State Keys
- `game_initialized` — bool, prevents re-init on rerun
- `heroes` — list of Hero objects
- `boss` — Boss object
- `logs` — list of str, battle narration
- `turn_number` — int counter
- `play_mode` — radio widget value

### Two Play Modes
1. **Auto Battle** (`🤖 Auto Battle`): Single "Next Turn" button, AI uses decision tree (heal if low → use vehicle if hurt → attack)
2. **Manual Battle** (`🎮 Manual Battle`): `st.form` with `st.selectbox` per alive hero, batch "Execute Turn" button

### UI Layout
- Radio toggle at top
- Two columns: Heroes (left) | Boss (right)
- Heroes show HP bar, inventory items, vehicle name + status
- Boss shows HP bar, Fire Breath countdown/warning
- Battle log as `st.text_area` below divider (newest at top)

---

## Key Design Decisions & Rationale

### Why `list[str]` return instead of `print()`
Both `app.py` (Streamlit) and `main.py` (CLI) consume the same game logic. `print()` is invisible in Streamlit. Returning strings lets each UI decide how to display them.

### Why vehicles are immediate effects (not state-based)
Original design had Car = dodge (state flag), Boat = retreat (skip turn). Simplified to immediate heals/damage to avoid cross-file state tracking. Still demonstrates composition and polymorphism.

### Why batch form for Manual mode
Streamlit reruns the entire script on every widget interaction. Sequential per-hero turns would require complex session state tracking. Batch form (pick all actions, then execute) avoids this entirely.

### Why Boss has 400 HP + Fire Breath
Original 300 HP boss was too easy (heroes killed it in ~5 rounds). With items/vehicles, heroes are even stronger. 400 HP + AoE creates pressure to use healing strategically.

---

## Testing

```bash
pytest -v          # Run all 42 tests
pytest tests/test_items.py -v    # Just item tests
pytest tests/test_vehicles.py -v # Just vehicle tests
pytest tests/test_entities.py -v # Just entity tests
pytest tests/test_battle.py -v   # Just integration tests
```

### Test Coverage
- **test_items.py** (11 tests): HealthPotion healing/clamping, ManaPotion vehicle recharge, SpeedBoost extra action
- **test_vehicles.py** (10 tests): Each vehicle's effect, single-use enforcement, recharge
- **test_entities.py** (15 tests): Hero creation/stats, attack/crit, items, vehicles, life/death, Boss Fire Breath timing
- **test_battle.py** (6 tests): Full battle simulation, Fire Breath timing, items/vehicles in battle, HP clamping

---

## Potential Future Enhancements

These were discussed but scoped out of the initial implementation:

1. **Level-up system** — Heroes gain XP, level up with increased stats (demonstrates class methods, `@property`)
2. **Status effects** — Poison, burn, stun from boss attacks (demonstrates state patterns, enums)
3. **Equipment slots** — Heroes equip different weapons that change attack behavior
4. **Multiple bosses/stages** — A BossFactory that creates different bosses per stage
5. **Save/Load game** — Serialize game state to JSON (demonstrates `__str__`, `__repr__`)

---

## Common Commands

```bash
# Setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run web UI
streamlit run app.py

# Run CLI version
python3 main.py

# Run tests
pytest -v

# Run specific test
pytest tests/test_items.py::TestHealthPotion::test_heals_target -v
```
