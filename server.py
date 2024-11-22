import serial
import random
import configparser

# Define valid choices
choices = ['rock', 'paper', 'scissors']

# Load game configuration
def load_config(filename='config.ini'):
    """
    @brief Loads game configuration from an INI file.
    @param filename The name of the configuration file.
    @return A ConfigParser object with the loaded configuration.
    """
    config = configparser.ConfigParser()
    config.read(filename)
    if 'game' not in config:
        config['game'] = {
            'game_mode': 'man_vs_ai',
            'player_score': '0',
            'ai_score': '0'
        }
        config['moves'] = {
            'player_moves': '',
            'ai_moves': ''
        }
    return config

# Save game configuration
def save_config(config, filename='config.ini'):
    """
    @brief Saves game configuration to an INI file.
    @param config The ConfigParser object containing game state.
    @param filename The name of the configuration file.
    """
    with open(filename, 'w') as configfile:
        config.write(configfile)

def get_winner(player_choice, server_choice):
    """
    @brief Determines the winner between player and server choices.
    @param player_choice The choice made by the player.
    @param server_choice The choice made by the server.
    @return A string representing the result: "player", "server", or "draw".
    """
    if player_choice == server_choice:
        return "draw"
    elif (player_choice == "rock" and server_choice == "scissors") or \
         (player_choice == "scissors" and server_choice == "paper") or \
         (player_choice == "paper" and server_choice == "rock"):
        return "player"
    else:
        return "server"
