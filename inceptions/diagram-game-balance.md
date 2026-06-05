# Game Balance — Hero vs Boss Stats Comparison

> **Tool**: Ditaa (ASCII art → SVG)
> **Purpose**: Visual infographic comparing hero party stats against the boss. Shows HP pools, damage output, and resource balance at a glance.

## How to Read This

- This diagram uses Ditaa to convert ASCII art into a styled SVG
- Boxes and arrows show the stat relationships
- Colors indicate team alignment (green = heroes, red = boss)

## Diagram

```ditaa
+-------------------------------------------------------+
|          RPG BATTLE ARENA — GAME BALANCE              |
|                                                       |
|  +-------------------------+  +-------------------+   |
|  | HERO PARTY    {s}       |  | BOSS        {eso} |   |
|  |                         |  |                   |   |
|  | Warrior   HP: 150       |  | Smaug   HP: 600   |   |
|  |  ██████████░░░░░░░░░░   |  |  ████████████████ |   |
|  |  ATK: 15    Crit: 20%   |  |  ████████████░░░░ |   |
|  |  Car: heal 30           |  |  ATK: 30          |   |
|  |  Items: HealthPot,      |  |                   |   |
|  |         SpeedBoost      |  |  Fire Breath:     |   |
|  |                         |  |  20 dmg to ALL    |   |
|  | Mage      HP: 80        |  |  every 2 turns    |   |
|  |  █████░░░░░░░░░░░░░░░   |  |                   |   |
|  |  ATK: 30    Crit: 20%   |  +-------------------+   |
|  |  Boat: heal 50          |                          |
|  |  Items: HealthPot,      |                          |
|  |         ManaPot         |                          |
|  |                         |                          |
|  | Archer    HP: 100       |                          |
|  |  ██████░░░░░░░░░░░░░░   |                          |
|  |  ATK: 20    Crit: 20%   |                          |
|  |  Drone: 60 dmg          |                          |
|  |  Items: ManaPot,        |                          |
|  |         SpeedBoost      |                          |
|  +-------------------------+                          |
|                                                       |
|  +------------------------------------------------+   |
|  | STAT SUMMARY                              {io} |   |
|  |                                                |   |
|  | Total Hero HP:     330                         |   |
|  | Total Healing:     +30 Car +50 Boat +40 x2 Pot |   |
|  |                    = ~195 recovery resources   |   |
|  | Combined DPR:      ~78/turn (with crit avg)    |   |
|  |                                                |   |
|  | Boss HP:           600                         |   |
|  | Boss DPR:          ~50/turn (single + AoE mix) |   |
|  | Turns to kill boss: ~8 turns at full DPR       |   |
|  +------------------------------------------------+   |
|                                                       |
|  +------------------------------------------------+   |
|  | WIN RATES                                  {io}|   |
|  |                                                |   |
|  | Manual mode:  ~75%  (smart item usage wins)    |   |
|  | Auto mode:    ~50-60%  (AI decision tree)      |   |
|  +------------------------------------------------+   |
+-------------------------------------------------------+
```

## Stat Comparison Table

| Metric | Hero Party | Boss (Smaug) |
|--------|-----------|--------------|
| **Total HP** | 330 | 600 |
| **Single-target ATK** | 15 / 30 / 20 | 30 |
| **AoE Damage** | — | 20 to ALL (every 2nd turn) |
| **Crit Chance** | 20% for 2× | — |
| **Burst Potential** | SpeedBoost = 3× (6× with crit) | — |
| **Healing** | Car 30 + Boat 50 + HealthPotions 80 | None |
| **Utility** | ManaPotion (recharge vehicle) | — |
| **Average DPR** | ~78/turn | ~50/turn |

## Balance Philosophy

1. **Boss has nearly 2× the hero HP pool** — creates pressure
2. **Boss attacks every turn** — consistent damage that adds up
3. **Fire Breath creates a "tick-tock" rhythm** — heroes must plan around it
4. **Items are limited** — bad usage = likely loss
5. **SpeedBoost is a tactical nuke** — 3× damage + immunity, but costs a turn
6. **Vehicle abilities are one-use** — timing matters
7. **Auto mode trades intelligence for convenience** — lower win rate reflects this
