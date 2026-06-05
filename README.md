# RPG Battle Arena

A turn-based RPG battle simulator built in Python 3 to demonstrate **Object-Oriented Programming (OOP)** concepts in a fun, interactive way. Includes both a **Streamlit web UI** and a **command-line** version.

## Overview

A party of three heroes (Warrior, Mage, Archer) battles a dragon boss in turn-based combat. Each hero has unique stats, inventory items, and a vehicle with a special ability. The boss has a devastating Fire Breath attack that hits all heroes every 3rd turn.

Choose between **Auto Battle** (AI picks actions) or **Manual Battle** (you choose each hero's action).

## OOP Concepts Demonstrated

| Concept | Where to Find It |
|---------|-----------------|
| **Inheritance** | `Hero` → `Warrior`, `Mage`, `Archer`; `Vehicle` → `Car`, `Boat`, `Drone` |
| **Abstract Base Classes** | `GameEntity`, `UsableItem`, `Vehicle` in `base.py` |
| **Properties & Setters** | `hp` property with clamping (can't go below 0 or above max) |
| **Composition** | Hero *has-a* Vehicle, Hero *has-a* inventory of Items |
| **Polymorphism** | Different `.use()` for each item and vehicle type |
| **Encapsulation** | `_used` flag on vehicles, `_hp` with getter/setter |
| **Separation of Concerns** | Game logic returns `list[str]`, UI decides how to display |

## Requirements

- Python 3.10+
- Streamlit
- pytest (for running tests)

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

### Streamlit Web UI

```bash
streamlit run app.py
```

Then open the URL shown in your terminal.

### Command-Line Version

```bash
python3 main.py
```

## Run Tests

```bash
pytest -v
```

This runs the test suite in the `tests/` directory covering items, vehicles, entities, and full battle simulation.

## Project Files

| File | Description |
|------|-------------|
| `app.py` | Streamlit web UI — dual-mode battle (Auto / Manual) |
| `main.py` | Command-line battle — interactive hero choices |
| `base.py` | Abstract base classes: `GameEntity`, `UsableItem`, `Vehicle` |
| `entities.py` | Hero subclasses (`Warrior`, `Mage`, `Archer`) and `Boss` |
| `items.py` | Item classes: `HealthPotion`, `ManaPotion`, `SpeedBoost` |
| `vehicles.py` | Vehicle classes: `Car`, `Boat`, `Drone` |
| `tests/` | pytest test suite |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Ignored local files |

## Game Mechanics

### Heroes

| Hero | HP | ATK | Vehicle | Vehicle Effect | Inventory |
|------|-----|-----|---------|----------------|-----------|
| Warrior | 150 | 15 | Car 🚗 | Heal 30 HP | Health Potion, Mana Potion |
| Mage | 80 | 30 | Boat ⛵ | Heal 50 HP | Health Potion, Speed Boost |
| Archer | 100 | 20 | Drone 🛩️ | 60 damage to boss | Mana Potion, Speed Boost |

### Items

- **Health Potion** 🧪 — Restore 40 HP
- **Mana Potion** 🔮 — Recharge your vehicle ability
- **Speed Boost** ⚡ — Take an extra action this turn

### Boss — Smaug the Dragon 🐉

- **HP**: 400
- **Attack**: 20 damage to a random hero
- **Fire Breath**: Every 3rd turn, deals 12 damage to **all** heroes

### How to Win

Use your items and vehicles wisely! The boss deals heavy damage, especially with Fire Breath. Time your heals and vehicle abilities to keep the party alive while dealing enough damage to bring Smaug down.

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Select your repository.
4. Set the app file path to `app.py`.
5. Deploy.
