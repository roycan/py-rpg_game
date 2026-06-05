# RPG Battle Arena — Improvement Plan

## Goal
Integrate unused items and vehicle classes, add a battle log, add player choice to the Streamlit UI, balance the boss fight, and add automated tests — all while maintaining the CLI version and keeping OOP concepts clear for grade 9 students.

## Key Design Principle
**All game methods return `list[str]` log messages.** Neither `entities.py`, `items.py`, nor `vehicles.py` call `print()` directly. The caller (`app.py` or `main.py`) decides how to display them.

---

## Changes by File

### 1. `base.py` — Update Vehicle ABC
- Change `Vehicle.move()` to `Vehicle.use(self, user, target) -> list[str]`
- Matches the `UsableItem.use()` pattern — consistent interface

### 2. `items.py` — Return log strings
- `HealthPotion.use()` — heals target for 40 HP, returns log string
- `ManaPotion.use()` — recharges hero's vehicle ability, returns log string
- `SpeedBoost.use()` — grants hero an extra action this turn, returns log string

### 3. `vehicles.py` — Return log strings, accept context
- `Car.use(user, target)` — hero dodges the next boss attack
- `Boat.use(user, target)` — hero retreats for 1 turn and heals 50 HP
- `Drone.use(user, target)` — bombs boss for 60 bonus damage
- Each vehicle has `_used` flag — single-use per battle

### 4. `entities.py` — Add vehicle, return logs
- `Hero` gets `self.vehicle` attribute assigned at creation
- `Hero` gets methods: `use_item(item_index, target)`, `use_vehicle(target)`
- `take_turn()` returns `list[str]` instead of print
- `Boss.take_turn()` returns `list[str]`
- Hero assignments: Warrior → Car, Mage → Boat, Archer → Drone

### 5. `entities.py` — Boss Balance
- Boss HP: 300 → **400**
- Boss ATK: 20 (single target, unchanged)
- **Fire Breath**: Every 3rd boss turn, hits ALL alive heroes for 12 damage each
- Boss tracks turn counter internally
- Fire Breath creates "tick-tock" tension — players know big damage is coming

### 6. `app.py` — Dual-mode UI with battle log

**Top section:**
- Radio toggle: 🤖 Auto Battle / 🎮 Manual Battle

**Hero panel (left column):**
- Show HP bar, inventory items remaining, vehicle name + status (available/used)

**Boss panel (right column):**
- HP bar + status
- In Manual mode: show "⚠️ Boss is charging Fire Breath!" warning when next turn is AoE

**Battle log (below divider):**
- Scrollable text area showing all turn narration
- Newest entries at top
- Clear visual formatting per entry

**Auto Battle mode:**
- Single "Next Turn" button
- Weighted random AI: 70% attack, 15% use item, 15% use vehicle
- Processes all heroes then boss, appends all logs, rerun

**Manual Battle mode:**
- Show all alive heroes, each with action buttons: ⚔️ Attack / 🧪 Use Item / 🚗 Use Vehicle
- Item/Vehicle buttons disabled if none available
- After all heroes act, boss auto-attacks with Fire Breath logic
- All actions append to battle log

### 7. `main.py` — CLI with choices
- Consume returned `list[str]` with `print()`
- Simple `input()` prompt per hero turn: Attack / Use Item / Use Vehicle

### 8. `tests/` — pytest test suite
- `test_items.py` — HealthPotion heals, ManaPotion recharges vehicle, SpeedBoost grants extra turn, HP clamping
- `test_vehicles.py` — Each vehicle effect applies, single-use enforcement
- `test_entities.py` — Hero creation, damage, death, inventory, vehicle assignment, return types
- `test_battle.py` — Full battle simulation, Fire Breath timing, win/lose conditions

### 9. `requirements.txt` — Add pytest
### 10. `README.md` — Updated docs

---

## OOP Concepts Demonstrated

| Concept | Where |
|---------|-------|
| Inheritance | Hero → Warrior, Mage, Archer; Vehicle → Car, Boat, Drone |
| Abstract Base Classes | GameEntity, UsableItem, Vehicle |
| Properties & Setters | `hp` property with clamping |
| Composition | Hero *has-a* Vehicle, Hero *has-a* list of Items |
| Polymorphism | Different `.use()` for items and vehicles |
| Separation of Concerns | Game logic returns strings, UI decides display |
| Encapsulation | `_used` flag on vehicles, `_hp` with getter/setter |

---

## Game Balance Summary

| Stat | Heroes | Boss |
|------|--------|------|
| Total HP Pool | 330 + ~195 healing/dodge | 400 |
| DPR | ~65/round + 60 Drone burst | 20 single + 36 AoE every 3rd |
| Rounds to kill | Boss dies in ~5-6 rounds | Heroes win ~60% auto, ~80% manual |

Heroes usually win but feel the danger. Poor item/vehicle usage leads to losses.

---

## Run Tests

```bash
pip install pytest
pytest -v
```
