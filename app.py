
import streamlit as st
from entities import Warrior, Mage, Archer, Boss
import random

st.set_page_config(page_title="⚔️ RPG Battle Arena", page_icon="⚔️", layout="wide")

# ─── Custom CSS for readable battle log ───
st.markdown("""
<style>
    /* Battle log: bright text on dark background, readable when disabled */
    .stTextArea textarea[disabled] {
        color: #e8e8e8 !important;
        -webkit-text-fill-color: #e8e8e8 !important;
        background-color: #1e1e2e !important;
        font-family: 'Source Code Pro', 'Fira Code', 'Consolas', monospace !important;
        font-size: 13px !important;
        line-height: 1.6 !important;
    }
    .stTextArea textarea[disabled]:focus {
        box-shadow: none !important;
    }
    /* Dark border to match the RPG theme */
    .stTextArea > div > div {
        border-color: #3a3a5c !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚔️ RPG Battle Arena")

# ─── Initialize game state ───
if 'game_initialized' not in st.session_state:
    st.session_state.heroes = [Warrior("Thorin"), Mage("Gandalf"), Archer("Legolas")]
    st.session_state.boss = Boss("Smaug", hp=600)
    st.session_state.logs = ["📜 The battle begins! Smaug the Dragon has appeared!"]
    st.session_state.game_initialized = True
    st.session_state.turn_number = 0

heroes = st.session_state.heroes
boss = st.session_state.boss
game_over = not boss.is_alive() or not any(h.is_alive() for h in heroes)

# ─── Helper functions ───

def add_logs(new_logs):
    """Add new log entries to the battle log."""
    for msg in new_logs:
        st.session_state.logs.append(msg)

def auto_pick_action(hero):
    """Simple AI decision tree for auto mode. Returns (action_type, action_arg)."""
    hp_ratio = hero.hp / hero.max_hp

    # 1. If low HP and has a Health Potion, use it
    if hp_ratio < 0.4:
        for i, item in enumerate(hero.inventory):
            if item.name == "Health Potion":
                return ("item", i)

    # 2. If vehicle available and HP is below 60%, use vehicle (heal or bomb)
    if hero.has_vehicle_available() and hp_ratio < 0.6:
        return ("vehicle", None)

    # 3. If has Speed Boost and boss is alive, use it for burst damage (25% chance)
    for i, item in enumerate(hero.inventory):
        if item.name == "Speed Boost" and random.random() < 0.25:
            return ("item", i)

    # 4. Default: attack
    return ("attack", None)

def execute_hero_action(hero, action, boss):
    """Execute a single hero action and return log messages."""
    logs = []
    logs.append(f"--- {hero.name}'s Turn ---")

    if action == "attack":
        logs.extend(hero.take_turn(boss))
    elif action.startswith("item_"):
        item_index = int(action.split("_")[1])
        logs.extend(hero.use_item(item_index, hero))
    elif action == "vehicle":
        logs.extend(hero.use_vehicle(boss))

    return logs

def hp_bar(current, maximum, width=10):
    """Return a compact text-based HP bar."""
    pct = max(0, min(1, current / maximum))
    filled = int(pct * width)
    empty = width - filled
    return f"{'█' * filled}{'░' * empty}"


# ─── Play Mode Toggle ───

if not game_over:
    mode = st.radio("🎮 Play Mode", ["🤖 Auto Battle", "🎮 Manual Battle"],
                     horizontal=True, key="play_mode",
                     help="Auto: AI picks actions. Manual: you choose!")
else:
    mode = "🤖 Auto Battle"

is_manual = "Manual" in mode


# ─── Three-Column Layout: Heroes | Boss + Actions | Battle Log ───

col_heroes, col_boss, col_log = st.columns([1, 1, 2])

# ─── Left Column: Heroes ───

with col_heroes:
    st.subheader("🛡️ Heroes")
    for hero in heroes:
        status = "🟢" if hero.is_alive() else "💀"
        bar = hp_bar(hero.hp, hero.max_hp)

        # Line 1: Name + class + HP bar
        st.markdown(f"**{status} {hero.name}** — *{hero.__class__.__name__}*")
        st.markdown(f"`{bar}` {hero.hp}/{hero.max_hp}")

        # Line 2: Items + Vehicle (compact)
        if hero.is_alive():
            parts = []
            if hero.inventory:
                items_str = " ".join(f"🧪{item.name}" for item in hero.inventory)
                parts.append(items_str)
            else:
                parts.append("*empty*")
            if hero.vehicle:
                v_name = hero.vehicle.__class__.__name__
                v_status = "✅" if not hero.vehicle.is_used else "❌"
                parts.append(f"🚗 {v_name} {v_status}")
            st.markdown(" | ".join(parts))
        st.write("")  # small spacer between heroes

# ─── Center Column: Boss + Actions ───

with col_boss:
    st.subheader("🐉 Boss")
    status = "🔥" if boss.is_alive() else "💎"
    bar = hp_bar(boss.hp, boss.max_hp)
    st.markdown(f"**{status} {boss.name}**")
    st.markdown(f"`{bar}` {boss.hp}/{boss.max_hp}")

    # Fire Breath warning
    if boss.is_alive():
        if boss.fire_breath_next:
            st.warning("⚠️ Fire Breath incoming!")
        else:
            st.info(f"🔥 Fire Breath in {boss.turns_until_fire} turn(s)")

    st.write("")  # small spacer

    if not game_over:

        if is_manual:
            # ─── Manual Mode: batch form ───
            with st.form("manual_turn"):
                actions = {}
                for hero in heroes:
                    if not hero.is_alive():
                        continue

                    # Build action options for this hero
                    options = ["⚔️ Attack"]
                    option_values = ["attack"]

                    for i, item in enumerate(hero.inventory):
                        options.append(f"🧪 {item.name}")
                        option_values.append(f"item_{i}")

                    if hero.has_vehicle_available():
                        v_name = hero.vehicle.__class__.__name__
                        options.append(f"🚗 {v_name}")
                        option_values.append("vehicle")

                    chosen = st.selectbox(
                        f"{hero.name}:",
                        options=options,
                        key=f"action_{hero.name}"
                    )
                    idx = options.index(chosen)
                    actions[hero.name] = option_values[idx]

                submitted = st.form_submit_button("▶️ Execute Turn", use_container_width=True)

                if submitted:
                    st.session_state.turn_number += 1
                    add_logs([f"\n🔄 === Turn {st.session_state.turn_number} ==="])

                    # Process all hero actions
                    for hero in heroes:
                        if hero.is_alive() and hero.name in actions:
                            logs = execute_hero_action(hero, actions[hero.name], boss)
                            add_logs(logs)

                    # Boss turn
                    if boss.is_alive():
                        add_logs([f"--- {boss.name}'s Turn ---"])
                        add_logs(boss.take_turn(heroes))

                    st.rerun()

        else:
            # ─── Auto Mode: single button ───
            if st.button("▶️ Next Turn", use_container_width=True):
                st.session_state.turn_number += 1
                add_logs([f"\n🔄 === Turn {st.session_state.turn_number} ==="])

                # All alive heroes take turns with AI
                for hero in heroes:
                    if hero.is_alive():
                        action_type, action_arg = auto_pick_action(hero)

                        if action_type == "attack":
                            logs = execute_hero_action(hero, "attack", boss)
                        elif action_type == "item":
                            logs = execute_hero_action(hero, f"item_{action_arg}", boss)
                        elif action_type == "vehicle":
                            logs = execute_hero_action(hero, "vehicle", boss)
                        else:
                            logs = execute_hero_action(hero, "attack", boss)

                        add_logs(logs)

                        if not boss.is_alive():
                            break

                # Boss turn
                if boss.is_alive():
                    add_logs([f"--- {boss.name}'s Turn ---"])
                    add_logs(boss.take_turn(heroes))

                st.rerun()

    else:
        # ─── Game Over ───
        if boss.hp <= 0:
            st.success("🎉 **VICTORY!** The Dragon is defeated!")
            add_logs(["\n🎉 === VICTORY! The party has triumphed! ==="])
        else:
            st.error("💀 **GAME OVER!** The party has fallen.")
            add_logs(["\n💀 === GAME OVER! The party has been wiped out. ==="])

        if st.button("🔄 Restart Game", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# ─── Right Column: Battle Log ───

with col_log:
    st.subheader("📜 Battle Log")

    # Show logs in reverse order (newest at top)
    log_text = "\n".join(reversed(st.session_state.logs))
    st.text_area("Battle Log", value=log_text, height=450, disabled=True,
                 label_visibility="collapsed")
