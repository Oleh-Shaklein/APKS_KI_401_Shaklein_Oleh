import serial
import random
import configparser

# Define valid choices
choices = ['rock', 'paper', 'scissors']

def load_config(filename='config.ini'):
    """
    Loads the game configuration from a file.

    If the configuration file does not exist or lacks the necessary sections,
    a default configuration is created and returned.

    Args:
        filename (str): The name of the configuration file. Default is 'config.ini'.

    Returns:
        ConfigParser: The loaded configuration object.
    """
    config = configparser.ConfigParser()
    config.read(filename)

    # Ensure default sections and keys are present
    if 'game' not in config:
        config['game'] = {}
    if 'moves' not in config:
        config['moves'] = {}

    # Add missing keys with default values
    config['game'].setdefault('game_mode', 'man_vs_ai')
    config['game'].setdefault('player_score', '0')
    config['game'].setdefault('ai_score', '0')
    config['moves'].setdefault('player_moves', '')
    config['moves'].setdefault('ai_moves', '')

    return config



def save_config(config, filename='config.ini'):
    """
    Saves the current game configuration to a file.

    Args:
        config (ConfigParser): The game configuration object to save.
        filename (str): The name of the configuration file. Default is 'config.ini'.
    """
    with open(filename, 'w') as configfile:
        config.write(configfile)


def get_winner(player_choice, server_choice):
    """
    Determines the winner of a Rock-Paper-Scissors round.

    Args:
        player_choice (str): The player's move ('rock', 'paper', or 'scissors').
        server_choice (str): The server's move ('rock', 'paper', or 'scissors').

    Returns:
        str: The winner ('player', 'server', or 'draw').

    Raises:
        ValueError: If either player_choice or server_choice is invalid.
    """
    if player_choice not in ['rock', 'paper', 'scissors']:
        raise ValueError(f"Invalid player choice: {player_choice}")
    if server_choice not in ['rock', 'paper', 'scissors']:
        raise ValueError(f"Invalid server choice: {server_choice}")

    if player_choice == server_choice:
        return "draw"
    elif (player_choice == "rock" and server_choice == "scissors") or \
            (player_choice == "scissors" and server_choice == "paper") or \
            (player_choice == "paper" and server_choice == "rock"):
        return "player"
    else:
        return "server"



def run_server():
    """
    Runs the Rock-Paper-Scissors server.

    Initializes a serial connection, listens for commands from the client,
    processes the commands, and sends responses back to the client.

    Commands supported:
        - "new": Starts a new game.
        - "save": Saves the current game state.
        - "load": Loads a previously saved game state.
        - "play <choice>": Processes the player's choice (rock, paper, or scissors).

    Raises:
        KeyboardInterrupt: Handles graceful shutdown of the server when interrupted.
    """
    ser = serial.Serial('COM11', 9600, timeout=1)
    print("Rock-Paper-Scissors server is running on COM11...")

    config = load_config()

    try:
        while True:
            if ser.in_waiting > 0:
                command = ser.readline().decode().strip().lower()

                if command == "new":
                    config['game'] = {
                        'game_mode': 'man_vs_ai',
                        'player_score': '0',
                        'ai_score': '0'
                    }
                    config['moves'] = {
                        'player_moves': '',
                        'ai_moves': ''
                    }
                    ser.write("New game started.\n".encode())
                elif command == "save":
                    save_config(config)
                    ser.write("Game saved.\n".encode())
                elif command == "load":
                    config = load_config()
                    ser.write("Game loaded.\n".encode())
                elif command.startswith("play"):
                    _, player_choice = command.split()
                    if player_choice not in choices:
                        ser.write("Invalid choice. Choose rock, paper, or scissors.\n".encode())
                        continue

                    # AI makes a choice (random)
                    server_choice = random.choice(choices)

                    # Determine the winner
                    winner = get_winner(player_choice, server_choice)
                    if winner == "player":
                        config['game']['player_score'] = str(int(config['game']['player_score']) + 1)
                    elif winner == "server":
                        config['game']['ai_score'] = str(int(config['game']['ai_score']) + 1)

                    # Update moves in the config
                    player_moves = config['moves'].get('player_moves', '')
                    ai_moves = config['moves'].get('ai_moves', '')
                    config['moves']['player_moves'] = player_moves + player_choice + ','
                    config['moves']['ai_moves'] = ai_moves + server_choice + ','

                    # Prepare the response message
                    response = f"Player: {player_choice}, Server: {server_choice}, Result: {winner}, Scores - Player: {config['game']['player_score']}, Server: {config['game']['ai_score']}"
                    ser.write(f"{response}\n".encode())
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        ser.close()
        save_config(config)
if __name__ == "__main__":
    run_server()