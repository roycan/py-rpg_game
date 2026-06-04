
import streamlit as st
from entities import Warrior, Mage, Archer, Boss
import random

st.title("⚔️ RPG Battle Arena")

# Initialize game state
if 'game_initialized' not in st.session_state:
    st.session_state.warrior = Warrior("Thorin")
    st.session_state.mage = Mage("Gandalf")
    st.session_state.archer = Archer("Legolas")
    st.session_state.boss = Boss("Smaug", hp=300)
    st.session_state.logs = ["The battle begins!"]
    st.session_state.game_initialized = True

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Heroes")
    for hero in [st.session_state.warrior, st.session_state.mage, st.session_state.archer]:
        status = "🟢" if hero.is_alive() else "💀"
        st.write(f"{status} **{hero.name}**: {hero.hp}/{hero.max_hp} HP")

with col2:
    st.subheader("Boss")
    boss = st.session_state.boss
    status = "🔥" if boss.is_alive() else "💎"
    st.write(f"{status} **{boss.name}**: {boss.hp}/{boss.max_hp} HP")
    st.progress(max(0, boss.hp / boss.max_hp))

st.divider()

# Battle Actions
if boss.is_alive() and any(h.is_alive() for h in [st.session_state.warrior, st.session_state.mage, st.session_state.archer]):
    if st.button("Next Turn"):
        # Simple turn simulation for now
        hero = random.choice([h for h in [st.session_state.warrior, st.session_state.mage, st.session_state.archer] if h.is_alive()])
        hero.take_turn(boss)
        if boss.is_alive():
            boss.take_turn([st.session_state.warrior, st.session_state.mage, st.session_state.archer])
        st.rerun()
else:
    if boss.hp <= 0:
        st.success("VICTORY! The Dragon is defeated!")
    else:
        st.error("GAME OVER! The party has fallen.")
    
    if st.button("Restart Game"):
        del st.session_state.game_initialized
        st.rerun()
