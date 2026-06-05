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
├── Hero → Warrior (150 HP, 15 ATK, Car, HealthPotion+SpeedBoost)
├── Hero → Mage (80 HP, 30 ATK, Boat, HealthPotion+ManaPotion)
├── Hero → Archer (100 HP, 20 ATK, Drone, ManaPotion+SpeedBoost)
└── Boss (600 HP, 30 ATK, Fire Breath every 2nd turn)

UsableItem (ABC)
├── HealthPotion (heal 40 HP)
├── ManaPotion (recharge vehicle)
└── SpeedBoost (3x damage next turn + immune to single-target this turn)

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
| `app.py` | ~190 | Streamlit web UI | Dual-mode (Auto/Manual), 3-column layout, battle log, session state |
| `main.py` | ~100 | CLI game loop | `play_rpg()`, `choose_action()`, `execute_hero_action()` |
| `tests/` | ~400 | pytest suite | 52 tests across 4 files |
| `requirements.txt` | 2 | Dependencies | streamlit, pytest |
| `README.md` | — | User documentation | Setup, OOP concepts, game mechanics |

---

## Game Balance

### Hero Party
- **Warrior**: 150 HP, 15 ATK, Car (heal 30), HealthPotion + SpeedBoost
- **Mage**: 80 HP, 30 ATK, Boat (heal 50), HealthPotion + ManaPotion
- **Archer**: 100 HP, 20 ATK, Drone (60 dmg), ManaPotion + SpeedBoost
- Combined DPR: ~78/round (with 20% crit averaging 1.2×), 20% crit chance for 2x damage
- Total HP pool: 330 + ~195 healing/dodge resources

### Boss — Smaug
- 600 HP, 30 ATK (single target, random hero)
- Fire Breath: every 2nd turn, 20 damage to ALL alive heroes
- `turns_until_fire` and `fire_breath_next` properties for UI warnings
- Average boss DPR: ~50/turn (mix of single target + AoE)
- Single-target attack **skips speed-boosted heroes** (they're too fast to hit)

### Expected Balance
- Heroes win ~75% in Manual mode (smart choices)
- Heroes win ~50-60% in Auto mode (AI decision tree)
- Bad item/vehicle usage → likely loss
- Fire Breath creates "tick-tock" tension every other turn
- SpeedBoost is a tactical burst item: sacrifice a turn for 3x damage next turn + immunity

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

### UI Layout (3-column, fits standard viewport)
- Uses `layout="wide"` in `set_page_config` for maximum horizontal space
- Radio toggle at top for play mode selection
- Three columns (`[1, 1, 2]` ratio): Heroes (left) | Boss + Actions (center) | Battle Log (right)
- Heroes show compact 2-line cards: name/class + text-based HP bar on line 1, items + vehicle on line 2
- Boss shows HP bar, Fire Breath countdown/warning, action button/form
- Battle log as `st.text_area` in right column (newest at top, height=450)
- No scrolling needed on 1366×768 viewport

---

## Key Design Decisions & Rationale

### Why `list[str]` return instead of `print()`
Both `app.py` (Streamlit) and `main.py` (CLI) consume the same game logic. `print()` is invisible in Streamlit. Returning strings lets each UI decide how to display them.

### Why vehicles are immediate effects (not state-based)
Original design had Car = dodge (state flag), Boat = retreat (skip turn). Simplified to immediate heals/damage to avoid cross-file state tracking. Still demonstrates composition and polymorphism.

### Why batch form for Manual mode
Streamlit reruns the entire script on every widget interaction. Sequential per-hero turns would require complex session state tracking. Batch form (pick all actions, then execute) avoids this entirely.

### Why Boss has 600 HP + Fire Breath every 2 turns
Original 400 HP boss was too easy (heroes won 100% in auto mode at 50%+ HP). Buffed to 600 HP / 30 ATK / 20 damage Fire Breath every 2nd turn to create real pressure and bring auto win rate to ~50-60%. Boss single-target skips speed-boosted heroes (too fast to hit).

### Why SpeedBoost is a delayed burst item
Original SpeedBoost granted an "extra action" that was consumed immediately — net result was identical to just attacking normally (wasted the item). Redesigned as a tactical trade-off: sacrifice this turn's attack for 3× damage next turn + immunity to boss single-target attack. This creates meaningful decisions (burst when boss is low? use defensively before Fire Breath?).

---

## Testing

```bash
pytest -v          # Run all 52 tests
pytest tests/test_items.py -v    # Just item tests
pytest tests/test_vehicles.py -v # Just vehicle tests
pytest tests/test_entities.py -v # Just entity tests
pytest tests/test_battle.py -v   # Just integration tests
```

### SpeedBoost Mechanic (Design)
1. **Turn N**: Hero uses SpeedBoost → `_speed_boost_active = True` → immune to boss single-target attack this turn
2. **Turn N boss phase**: Boss skips speed-boosted heroes for single-target (Fire Breath still hits)
3. **Turn N+1 hero phase**: Hero attacks with 3× damage → `_speed_boost_active` cleared
4. Crit + SpeedBoost: `attack_power × 2 × 3 = 6×` (rare but devastating)
5. Edge case: if ALL alive heroes are speed-boosted, boss wastes its single-target turn

### Test Coverage
- **test_items.py** (8 tests): HealthPotion healing/clamping, ManaPotion vehicle recharge, SpeedBoost flag + clearing
- **test_vehicles.py** (9 tests): Each vehicle's effect, single-use enforcement, recharge
- **test_entities.py** (26 tests): Hero creation/stats, attack/crit, speed boost 3× damage, boss immunity, items, vehicles, life/death, Boss Fire Breath timing
- **test_battle.py** (9 tests): Full battle simulation, Fire Breath timing, items/vehicles in battle, HP clamping, SpeedBoost in battle, boss immunity, Fire Breath vs boost

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
