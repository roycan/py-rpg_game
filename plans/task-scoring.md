# Task Scoring Assessment

Each task gets two scores:
- **Feasibility** — How likely we can implement this correctly given the codebase
- **Confidence** — How sure we are the approach will work without major rework

Both scored 0-100%.

---

## Scoring Breakdown

### ✅ Task 3: Refactor base.py — Vehicle ABC
- **Feasibility: 98%** — Trivial change, just renaming a method signature
- **Confidence: 98%** — Zero risk, single file, no downstream surprises
- **Risk**: None

### ✅ Task 4: Refactor items.py — Return list[str]
- **Feasibility: 95%** — Straightforward string replacement
- **Confidence: 90%** — SpeedBoost's "extra turn" needs game state tracking. How do we signal the caller that a hero gets another action? Need a clear contract.
- **Risk**: SpeedBoost return value design

### ✅ Task 5: Refactor vehicles.py — use(user, target)
- **Feasibility: 95%** — Clear pattern to follow
- **Confidence: 88%** — Boat's "retreat for 1 turn" means the hero needs a "dodging" state that the boss respects. Car's "dodge next attack" is similar. This state needs to live on the Hero and be checked in Boss.take_turn().
- **Risk**: Dodge/retreat state management

### ⚠️ Task 6: Refactor entities.py — Vehicle + return logs
- **Feasibility: 90%** — Multiple interconnected changes in one file
- **Confidence: 82%** — Biggest refactoring task. Hero needs vehicle assignment, use_item(), use_vehicle(), and all return types change. Also needs to integrate with dodge/retreat states from vehicles. If any part is wrong, it cascades.
- **Risk**: Complexity, cascading changes

### ✅ Task 7: Balance boss — 400 HP + Fire Breath
- **Feasibility: 95%** — Simple stat change + turn counter + AoE logic
- **Confidence: 90%** — Turn counter in Boss is straightforward. AoE targeting needs to hit all alive heroes. Need to decide: does Fire Breath replace the single-target attack or happen in addition?
- **Risk**: Design decision on Fire Breath timing

### ✅ Task 8: app.py — Play mode toggle
- **Feasibility: 98%** — Single st.radio() widget
- **Confidence: 98%** — Trivial Streamlit element
- **Risk**: None

### ⚠️ Task 9: app.py — Auto mode with weighted random AI
- **Feasibility: 90%** — Random choices with weights, straightforward
- **Confidence: 83%** — Need to handle edge cases: what if hero has no items? No vehicle? Vehicle already used? Each hero needs independent AI decisions per turn. State updates in session_state need to be atomic.
- **Risk**: Edge case handling in AI logic

### ⚠️ Task 10: app.py — Manual mode with hero action buttons
- **Feasibility: 78%** — Most complex UI task
- **Confidence: 72%** — Streamlit's rerun model makes sequential turn-based UI tricky. Each button click causes a full rerun. Need to track: current hero index, which heroes have acted, has boss gone, is round over. All via session_state. Streamlit buttons also have a quirk where every button on the page fires on the same script run.
- **Risk**: Streamlit state management, button click handling

### ✅ Task 11: app.py — Battle log
- **Feasibility: 98%** — Simple text_area or expander
- **Confidence: 98%** — Read from session_state.logs, display
- **Risk**: None

### ✅ Task 12: app.py — Hero info panel
- **Feasibility: 95%** — Display inventory + vehicle status
- **Confidence: 93%** — Depends on entity refactoring being done. Format the display.
- **Risk**: Minor dependency on Task 6

### ✅ Task 13: app.py — Boss Fire Breath warning
- **Feasibility: 95%** — Check boss turn counter, show warning text
- **Confidence: 92%** — Depends on boss turn tracking from Task 7
- **Risk**: Minor dependency on Task 7

### ✅ Task 14: Update main.py — CLI version
- **Feasibility: 92%** — Standard input/print loop
- **Confidence: 88%** — Need to handle same edge cases as Streamlit but with input(). Also need to integrate item/vehicle choices.
- **Risk**: Input validation for grade 9 students

### ✅ Task 15: pytest test suite
- **Feasibility: 92%** — Standard pytest patterns
- **Confidence: 85%** — Tests need to match final entity/item/vehicle API. If API changes during implementation, tests need updating. Writing tests before finalizing API is risky.
- **Risk**: API stability during implementation

### ✅ Task 16: requirements.txt — Add pytest
- **Feasibility: 100%** — One line addition
- **Confidence: 100%** — Trivial
- **Risk**: None

### ✅ Task 17: README.md — Update docs
- **Feasibility: 100%** — Documentation only
- **Confidence: 95%** — Needs accurate description of final state
- **Risk**: None

### ✅ Task 18: Final review
- **Feasibility: 100%** — Manual testing
- **Confidence: 90%** — Balance might need tuning after playtesting
- **Risk**: Minor balance tweaks needed

---

## Tasks Scoring ≤ 90% — Review & Simplification

| Task | Feasibility | Confidence | Main Risk |
|------|-------------|------------|-----------|
| Task 6: entities.py refactor | 90% | 82% | Cascading changes, dodge state |
| Task 9: Auto mode AI | 90% | 83% | Edge cases in AI logic |
| Task 10: Manual mode UI | 78% | 72% | Streamlit rerun complexity |
| Task 14: main.py CLI | 92% | 88% | Input validation |
| Task 15: pytest suite | 92% | 85% | API stability |

---

## Simplification Proposals

### Task 10 (Manual mode UI) — 78%/72% → Simplify to 92%/90%

**Problem**: Tracking sequential hero turns with Streamlit's rerun model is the hardest part. Each button click reruns the whole script.

**Simplification**: Instead of sequential "hero 1 acts, then hero 2, then hero 3", use a **batch approach**:
- Show ALL alive heroes at once, each with their own set of action buttons
- Player picks actions for all heroes simultaneously
- One "Execute Turn" button processes all hero actions, then boss acts
- This avoids tracking hero turn index entirely

This is simpler because:
- No sequential turn tracking in session_state
- One form submission instead of 3 sequential button clicks
- Uses st.form() to batch inputs

### Task 6 (entities.py refactor) — 90%/82% → Simplify to 93%/88%

**Problem**: Dodge/retreat state from vehicles adds complexity.

**Simplification**: Simplify vehicle effects to immediate one-time effects:
- Car: Immediately heals 30 HP (dodge = you recovered)
- Boat: Immediately heals 50 HP (retreat = you rested)
- Drone: Immediately deals 60 damage to boss

This removes the need for state flags like "is_dodging" or "is_retreating" that would need to be checked in Boss.take_turn(). Simpler to implement, still demonstrates composition and polymorphism.

### Task 9 (Auto mode AI) — 90%/83% → Simplify to 93%/88%

**Problem**: Weighted random with item/vehicle availability checks.

**Simplification**: Simple decision tree instead of weighted random:
1. If hero has a vehicle available AND HP < 50% → use vehicle
2. If hero has a HealthPotion AND HP < 40% → use item
3. Otherwise → attack

This is more predictable, easier to test, and actually demonstrates better AI logic than random weights.

### Task 5 (vehicles.py) — 95%/88% → Simplify to 95%/93%

Same as Task 6 simplification — if vehicles are immediate effects instead of state-based, confidence jumps.

---

## Final Scoring After Simplification

| Task | Feasibility | Confidence | Change |
|------|-------------|------------|--------|
| Task 3: base.py | 98% | 98% | — |
| Task 4: items.py | 95% | 92% | ↑ SpeedBoost simplified |
| Task 5: vehicles.py | 95% | 93% | ↑ Immediate effects |
| Task 6: entities.py | 93% | 88% | ↑ Simpler vehicle integration |
| Task 7: boss balance | 95% | 90% | — |
| Task 8: mode toggle | 98% | 98% | — |
| Task 9: auto mode | 93% | 88% | ↑ Simple decision tree AI |
| Task 10: manual mode | 92% | 90% | ↑ Batch approach |
| Task 11: battle log | 98% | 98% | — |
| Task 12: hero panel | 95% | 93% | — |
| Task 13: boss warning | 95% | 92% | — |
| Task 14: main.py | 92% | 88% | — |
| Task 15: tests | 92% | 88% | ↑ Simpler API to test |
| Task 16: requirements.txt | 100% | 100% | — |
| Task 17: README | 100% | 95% | — |
| Task 18: final review | 100% | 90% | — |
