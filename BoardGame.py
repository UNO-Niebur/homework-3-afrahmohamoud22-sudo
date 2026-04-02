# Homework 3 - Board Game System
# Name: Afrah Mohamoud
# Date: 03/28/2026


def load_game_data(filename):
    """Read game data from a file and return a structured state dictionary."""
    state = {"turn": None, "players": {}, "events": {}}

    with open(filename, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or ":" not in line:
                continue

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key.lower() == "turn":
                state["turn"] = value
                continue

            if not key.isdigit():
                continue

            position = int(key)
            if value.lower().startswith("player"):
                state["players"][value] = position
            else:
                state["events"][position] = value

    if state["players"] and state["turn"] not in state["players"]:
        state["turn"] = sorted(state["players"])[0]

    return state


def save_game_data(filename, state):
    """Save the current game state back to the file."""
    lines = []

    if state["turn"] is not None:
        lines.append(f"Turn: {state['turn']}")

    for player in sorted(state["players"]):
        lines.append(f"{state['players'][player]}: {player}")

    for position in sorted(state["events"]):
        lines.append(f"{position}: {state['events'][position]}")

    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def get_board_size(state):
    """Determine board size from farthest player or event."""
    farthest_player = max(state["players"].values(), default=1)
    farthest_event = max(state["events"].keys(), default=1)
    return max(farthest_player, farthest_event, 1)


def display_game_state(state):
    """Display board spaces, players, events, and whose turn it is."""
    board_size = get_board_size(state)

    print("\n===== Current Game State =====")
    print(f"Current turn: {state['turn']}")
    print("\nPlayers:")
    for player in sorted(state["players"]):
        print(f"- {player} is on space {state['players'][player]}")

    print("\nBoard:")
    for space in range(1, board_size + 1):
        players_here = [
            name for name, position in state["players"].items() if position == space
        ]
        event_here = state["events"].get(space)

        labels = []
        if players_here:
            labels.append("Players=" + ", ".join(sorted(players_here)))
        if event_here:
            labels.append("Event=" + event_here)

        if labels:
            print(f"{space:>2}: " + " | ".join(labels))


def switch_turn(state):
    """Switch turn to the next player in sorted order."""
    players = sorted(state["players"])
    if not players:
        return

    if state["turn"] not in players:
        state["turn"] = players[0]
        return

    current_index = players.index(state["turn"])
    next_index = (current_index + 1) % len(players)
    state["turn"] = players[next_index]


def trigger_event(state, player):
    """Apply event effects if the player lands on an event space."""
    position = state["players"][player]
    event = state["events"].get(position)

    if not event:
        print(f"{player} landed on space {position}. No event triggered.")
        return

    event_name = event.lower()
    print(f"{player} landed on {event} at space {position}!")

    if event_name in {"trap", "troll"}:
        state["players"][player] = max(1, position - 2)
        print(f"{player} moves back 2 spaces to {state['players'][player]}.")
    elif event_name == "heal":
        state["players"][player] = position + 1
        print(f"{player} moves forward 1 extra space to {state['players'][player]}.")
    elif event_name in {"treasure", "hotel"}:
        print(f"{player} receives the {event} bonus.")
    else:
        print(f"{event} has no custom effect configured.")


def move_current_player(state):
    """Prompt for movement value, update current player, and trigger events."""
    current_player = state["turn"]
    if current_player is None or current_player not in state["players"]:
        print("No valid current player found.")
        return

    while True:
        steps_text = input(f"How many spaces should {current_player} move? ").strip()
        if steps_text.isdigit():
            steps = int(steps_text)
            break
        print("Please enter a whole number (0 or more).")

    old_position = state["players"][current_player]
    new_position = old_position + steps
    state["players"][current_player] = new_position

    print(f"{current_player} moved from {old_position} to {new_position}.")
    trigger_event(state, current_player)


def print_menu():
    """Display available game actions."""
    print("\n===== Menu =====")
    print("1) Display board")
    print("2) Move current player")
    print("3) Switch turn")
    print("4) Save game")
    print("5) Save and quit")


def main():
    filename = "events.txt"

    state = load_game_data(filename)

    if not state["players"]:
        print("No players found in file. Add entries such as '3: Player1'.")
        return

    if state["turn"] is None:
        state["turn"] = sorted(state["players"])[0]

    print("Welcome to the Board Game System!")

    while True:
        print_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            display_game_state(state)
        elif choice == "2":
            move_current_player(state)
        elif choice == "3":
            switch_turn(state)
            print(f"Turn switched. It is now {state['turn']}'s turn.")
        elif choice == "4":
            save_game_data(filename, state)
            print("Game saved.")
        elif choice == "5":
            save_game_data(filename, state)
            print("Game saved. Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()
