# Main.py Flow — CLI Game Loop

> **Tool**: Mermaid `flowchart TD`
> **Purpose**: Shows the CLI game loop flow — a classic imperative turn-based game loop.

## How to Read This

This is a straightforward top-to-bottom game loop. Unlike the Streamlit version (`app.py`), this is a traditional `while` loop with sequential I/O.

## Diagram

```mermaid
flowchart TD
    START([play_rpg called]) --> INIT[Create party:<br/>Warrior Thorin, Mage Gandalf, Archer Legolas]
    INIT --> INIT_BOSS[Create Boss Smaug - 600 HP]
    INIT_BOSS --> SHOW_INTRO[Print boss appearance<br/>and party stats]

    SHOW_INTRO --> TURN_START[Increment turn counter]
    TURN_START --> TURN_HEADER[Print Turn N header]

    TURN_HEADER --> FIRE_WARN{Fire Breath<br/>next?}
    FIRE_WARN -- Yes --> WARN[Print Fire Breath warning]
    FIRE_WARN -- No --> HERO_LOOP
    WARN --> HERO_LOOP

    HERO_LOOP{For each alive hero<br/>and boss alive?}
    HERO_LOOP -- Next hero --> CHOOSE[choose_action - hero, boss]
    CHOOSE --> SHOW_OPTIONS[Show hero stats<br/>and action menu]
    SHOW_OPTIONS --> INPUT[Get player input<br/>attack / item_N / vehicle]

    INPUT --> EXEC{Action type?}
    EXEC -- attack --> DO_ATTACK[hero.take_turn - boss]
    EXEC -- item_N --> DO_ITEM[hero.use_item - N, hero]
    EXEC -- vehicle --> DO_VEHICLE[hero.use_vehicle - boss]

    DO_ATTACK --> PRINT_LOGS[print_logs - logs]
    DO_ITEM --> PRINT_LOGS
    DO_VEHICLE --> PRINT_LOGS

    PRINT_LOGS --> BOSS_CHECK1{Boss alive?}
    BOSS_CHECK1 -- No --> END_LOOP
    BOSS_CHECK1 -- Yes --> HERO_LOOP

    %% Boss turn
    HERO_LOOP -- All heroes done --> BOSS_ALIVE{Boss alive?}
    BOSS_ALIVE -- Yes --> BOSS_TURN[boss.take_turn - players]
    BOSS_TURN --> PRINT_BOSS[print_logs - boss logs]
    PRINT_BOSS --> STATUS[Print status:<br/>Boss HP + alive heroes]
    STATUS --> LOOP_CHECK

    BOSS_ALIVE -- No --> END_LOOP

    %% Loop continuation
    STATUS --> LOOP_CHECK{Boss alive AND<br/>any hero alive?}
    LOOP_CHECK -- Yes --> TURN_START
    LOOP_CHECK -- No --> END_LOOP

    %% End game
    END_LOOP{Who won?}
    END_LOOP -- Boss HP <= 0 --> VICTORY[Print VICTORY message]
    END_LOOP -- All heroes dead --> DEFEAT[Print GAME OVER message]

    VICTORY --> DONE([End])
    DEFEAT --> DONE

    %% Styling
    classDef startend fill:#4a90d9,stroke:#2c5f8a,color:#fff
    classDef decision fill:#f39c12,stroke:#b35c18,color:#fff
    classDef action fill:#6b8e23,stroke:#4a6318,color:#fff
    classDef io fill:#9b59b6,stroke:#6c3483,color:#fff

    class START,DONE,VICTORY,DEFEAT startend
    class HERO_LOOP,BOSS_ALIVE,LOOP_CHECK,END_LOOP,EXEC,FIRE_WARN,BOSS_CHECK1 decision
    class INIT,INIT_BOSS,TURN_START,DO_ATTACK,DO_ITEM,DO_VEHICLE,BOSS_TURN action
    class SHOW_INTRO,TURN_HEADER,WARN,CHOOSE,SHOW_OPTIONS,INPUT,PRINT_LOGS,PRINT_BOSS,STATUS io
```

## Key Differences from `app.py`

| Aspect | `main.py` CLI | `app.py` Streamlit |
|--------|--------------|-------------------|
| Loop model | `while` loop — runs continuously | Reactive — reruns on interaction |
| Action selection | Sequential per-hero `input()` prompts | Batch form (Manual) or AI (Auto) |
| Display | `print()` to stdout | `st.text_area` battle log |
| State | Local variables in function | `st.session_state` |
| Boss turn | Inline after hero loop | Same, but inside a rerun |
