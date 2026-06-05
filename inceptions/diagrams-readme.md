# 📊 Diagrams Index — RPG Battle Arena

> This directory contains architectural diagrams and flowcharts that describe the RPG Battle Arena web application. Each file is a standalone diagram that can be rendered independently.

---

## Quick Reference

| # | File | Diagram Type | Tool | Description |
|---|------|-------------|------|-------------|
| 1 | [diagram-architecture.md](diagram-architecture.md) | Dependency Graph | Mermaid | How all `.py` modules import and depend on each other |
| 2 | [diagram-class-hierarchy.md](diagram-class-hierarchy.md) | UML Class Diagram | PlantUML | All classes with attributes, methods, inheritance, and composition |
| 2b | [diagram-class-hierarchy-mermaid.md](diagram-class-hierarchy-mermaid.md) | UML Class Diagram | Mermaid | Backup of #2 in Mermaid format |
| 3 | [diagram-app-flow.md](diagram-app-flow.md) | Flowchart (×2) | Mermaid | Streamlit web UI flow: page lifecycle + turn execution |
| 4 | [diagram-main-flow.md](diagram-main-flow.md) | Flowchart | Mermaid | CLI game loop flow |
| 5 | [diagram-battle-turn-sequence.md](diagram-battle-turn-sequence.md) | Sequence Diagram | PlantUML | Method call chain during a battle turn |
| 5b | [diagram-battle-turn-sequence-mermaid.md](diagram-battle-turn-sequence-mermaid.md) | Sequence Diagram | Mermaid | Backup of #5 in Mermaid format |
| 6 | [diagram-game-object-model.md](diagram-game-object-model.md) | ERD | Kroki ERD | Entity relationships and composition between game objects |
| 6b | [diagram-game-object-model-mermaid.md](diagram-game-object-model-mermaid.md) | ERD | Mermaid | Backup of #6 in Mermaid format |
| 7 | [diagram-speedboost-state.md](diagram-speedboost-state.md) | State Diagram | Mermaid | SpeedBoost mechanic state transitions across turns |
| 8 | [diagram-game-balance.md](diagram-game-balance.md) | Infographic | Ditaa | Hero stats vs Boss stats comparison |
| 8b | [diagram-game-balance-mermaid.md](diagram-game-balance-mermaid.md) | Charts | Mermaid | Backup of #8 using pie charts and graph |

---

## Tools Used

| Tool | File Tag | Best For | Used In |
|------|----------|----------|---------|
| **Mermaid** | ` ```mermaid ` | Flowcharts, state diagrams, simple ERDs | #1, #2b, #3, #4, #5b, #6b, #7, #8b |
| **PlantUML** | ` ```plantuml ` | UML class diagrams, sequence diagrams | #2, #5 |
| **Kroki ERD** | ` ```erd ` | Entity-relationship diagrams | #6 |
| **Ditaa** | ` ```ditaa ` | ASCII-art infographics → SVG | #8 |

---

## How to Render

### VS Code (Mermaid only)
1. Install the **Mermaid Preview** extension (`bierner.markdown-mermaid`)
2. Open any `.md` file with a ` ```mermaid ` block
3. Open preview (Ctrl+Shift+V) — Mermaid diagrams render inline

### External App (all formats)
If you have a diagram rendering app (e.g., Kroki, Mermaid Live Editor, PlantUML server):
- Copy the code block content
- Paste into the renderer
- Each file uses the correct language tag for detection

---

## Diagram Relationships

```
Start here → diagram-architecture.md (big picture)
                    ↓
     diagram-class-hierarchy.md (class structure)
                    ↓
     ┌──────────────┼──────────────┐
     ↓              ↓              ↓
diagram-game-    diagram-app-   diagram-main-
object-model.md  flow.md        flow.md
(ERD)            (Streamlit)    (CLI)
     ↓
diagram-battle-turn-sequence.md
(how objects interact at runtime)
     ↓
diagram-speedboost-state.md
(most complex mechanic)
     ↓
diagram-game-balance.md
(balance design decisions)
```

---

## Naming Convention

- **Primary diagrams**: `diagram-{topic}.md`
- **Mermaid backups**: `diagram-{topic}-mermaid.md`
- Primary uses the optimal tool; backup uses Mermaid for VS Code native rendering
- After evaluating, delete the backup files you don't need

---

## Maintenance Tips

1. **When adding a new class**: Update `diagram-class-hierarchy.md` and `diagram-game-object-model.md`
2. **When changing game flow**: Update `diagram-app-flow.md` and/or `diagram-main-flow.md`
3. **When changing game balance**: Update `diagram-game-balance.md` and `inceptions/context.md`
4. **When adding new items/vehicles**: Update class hierarchy, ERD, and balance diagrams
5. **Keep diagrams in sync** with `inceptions/context.md` — the single source of truth
