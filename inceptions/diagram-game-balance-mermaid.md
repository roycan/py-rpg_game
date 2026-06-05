# Game Balance — Hero vs Boss Stats (Mermaid Backup)

> **Tool**: Mermaid
> **Purpose**: Mermaid version of the game balance comparison. Uses a combination of `pie` chart and `graph` for visual comparison.

## Diagram 1: HP Pool Comparison

```mermaid
pie title HP Pool Distribution
    "Warrior" : 150
    "Mage" : 80
    "Archer" : 100
    "Boss Smaug" : 600
```

## Diagram 2: Attack Power Comparison

```mermaid
pie title Attack Power Distribution
    "Warrior ATK 15" : 15
    "Mage ATK 30" : 30
    "Archer ATK 20" : 20
    "Boss ATK 30" : 30
```

## Stat Comparison Table

| Unit | HP | ATK | Vehicle Effect | Items |
|------|----|----|---------------|-------|
| **Warrior** | 150 `██████████░░░░░░░░░░` | 15 `██░░░░░░░░` | Car: heal 30 | HealthPotion, SpeedBoost |
| **Mage** | 80 `█████░░░░░░░░░░░░░░░` | 30 `████░░░░░░` | Boat: heal 50 | HealthPotion, ManaPotion |
| **Archer** | 100 `██████░░░░░░░░░░░░░░` | 20 `███░░░░░░░` | Drone: 60 dmg | ManaPotion, SpeedBoost |
| **Boss** | 600 `████████████████████` | 30 `████░░░░░░` | — | Fire Breath: 20 AoE / 2 turns |

## Balance Summary

```mermaid
graph LR
    subgraph Hero Party
        W[Warrior<br/>150 HP / 15 ATK]
        M[Mage<br/>80 HP / 30 ATK]
        A[Archer<br/>100 HP / 20 ATK]
    end

    subgraph Resources
        HP[Healing: ~195 total]
        SB[SpeedBoost: 3x burst]
        VH[Vehicles: 1-use each]
    end

    subgraph Boss
        B[Smaug<br/>600 HP / 30 ATK]
        FB[Fire Breath<br/>20 AoE every 2 turns]
    end

    W --> B
    M --> B
    A --> B
    HP --> W
    HP --> M
    SB --> W
    SB --> A
    VH --> W
    VH --> M
    VH --> A
    FB --> W
    FB --> M
    FB --> A

    classDef hero fill:#27ae60,stroke:#1e8449,color:#fff
    classDef boss fill:#c0392b,stroke:#922b21,color:#fff
    classDef resource fill:#2980b9,stroke:#1f618d,color:#fff

    class W,M,A hero
    class B,FB boss
    class HP,SB,VH resource
```

## Notes

- Mermaid `pie` charts are simple but effective for proportional comparison
- The `graph` provides a visual network of how resources flow
- The Unicode bar table provides exact numbers at a glance
- For the full Ditaa infographic version, see [diagram-game-balance.md](diagram-game-balance.md)
