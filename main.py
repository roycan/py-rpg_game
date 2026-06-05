from entities import Warrior, Mage, Archer, Boss
import random


def print_logs(logs):
    """Helper to print a list of log strings."""
    for msg in logs:
        print(msg)


def choose_action(hero, boss):
    """Let the player choose an action for the given hero. Returns (action_type, action_arg)."""
    print(f"\n  {hero.name} (HP: {hero.hp}/{hero.max_hp})")

    options = ["⚔️ Attack"]
    option_values = ["attack"]

    for i, item in enumerate(hero.inventory):
        options.append(f"🧪 Use {item.name}")
        option_values.append(f"item_{i}")

    if hero.has_vehicle_available():
        v_name = hero.vehicle.__class__.__name__
        options.append(f"🚗 Use {v_name}")
        option_values.append("vehicle")

    print("  Choose an action:")
    for i, opt in enumerate(options):
        print(f"    [{i+1}] {opt}")

    while True:
        try:
            choice = int(input("  > ")) - 1
            if 0 <= choice < len(options):
                return option_values[choice]
            print("  Invalid choice. Try again.")
        except (ValueError, EOFError):
            print("  Enter a number.")

    return "attack"


def execute_hero_action(hero, action, boss):
    """Execute a single hero action and return log messages."""
    logs = []
    if action == "attack":
        logs.extend(hero.take_turn(boss))
    elif action.startswith("item_"):
        item_index = int(action.split("_")[1])
        logs.extend(hero.use_item(item_index, hero))
    elif action == "vehicle":
        logs.extend(hero.use_vehicle(boss))

    # Check for extra action from SpeedBoost
    if hero.has_extra_action:
        hero.clear_extra_action()
        logs.append(f"⚡ {hero.name} takes an extra turn!")
        logs.extend(hero.take_turn(boss))

    return logs


def play_rpg():
    """Main game loop for the CLI version."""
    players = [Warrior("Thorin"), Mage("Gandalf"), Archer("Legolas")]
    boss = Boss("Smaug", hp=400)

    print("=" * 50)
    print(f"🐉 {boss.name} has appeared! (HP: {boss.max_hp})")
    print("=" * 50)

    # Show party
    for p in players:
        vehicle_info = f" | Vehicle: {p.vehicle.__class__.__name__}" if p.vehicle else ""
        print(f"  {p.__class__.__name__} {p.name}: HP {p.hp}/{p.max_hp}{vehicle_info}")

    turn = 0

    while boss.is_alive() and any(p.is_alive() for p in players):
        turn += 1
        print(f"\n{'='*50}")
        print(f"🔄 Turn {turn}")
        print(f"{'='*50}")

        # Fire Breath warning
        if boss.fire_breath_next:
            print("⚠️  Smaug is charging Fire Breath!")

        # Each hero takes a turn
        for hero in players:
            if hero.is_alive() and boss.is_alive():
                action = choose_action(hero, boss)
                logs = execute_hero_action(hero, action, boss)
                print_logs(logs)

        # Boss turn
        if boss.is_alive():
            print(f"\n--- {boss.name}'s Turn ---")
            print_logs(boss.take_turn(players))

        # Show status
        print(f"\n📊 Status: {boss.name} HP: {boss.hp}/{boss.max_hp}")
        alive = [f"{h.name} ({h.hp}/{h.max_hp})" for h in players if h.is_alive()]
        print(f"   Heroes: {', '.join(alive) if alive else 'None surviving'}")

    # End result
    print(f"\n{'='*50}")
    if boss.hp <= 0:
        print("🎉 VICTORY! The party has triumphed!")
    else:
        print("💀 GAME OVER! The party has been wiped out.")
    print(f"{'='*50}")


if __name__ == "__main__":
    play_rpg()
