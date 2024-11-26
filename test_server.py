import unittest
from server import get_winner, load_config, save_config
import configparser
import os

class TestGameLogic(unittest.TestCase):
    def test_get_winner_draw(self):
        """
        Test that a draw is correctly identified.
        """
        self.assertEqual(get_winner('rock', 'rock'), 'draw')
        self.assertEqual(get_winner('paper', 'paper'), 'draw')
        self.assertEqual(get_winner('scissors', 'scissors'), 'draw')

    def test_get_winner_player_wins(self):
        """
        Test cases where the player wins.
        """
        self.assertEqual(get_winner('rock', 'scissors'), 'player')
        self.assertEqual(get_winner('scissors', 'paper'), 'player')
        self.assertEqual(get_winner('paper', 'rock'), 'player')

    def test_get_winner_server_wins(self):
        """
        Test cases where the server wins.
        """
        self.assertEqual(get_winner('rock', 'paper'), 'server')
        self.assertEqual(get_winner('scissors', 'rock'), 'server')
        self.assertEqual(get_winner('paper', 'scissors'), 'server')

    def test_invalid_choices(self):
        """
        Test invalid choices for get_winner.
        """
        with self.assertRaises(ValueError):
            get_winner('invalid', 'rock')
        with self.assertRaises(ValueError):
            get_winner('rock', 'invalid')

    def test_load_config_default(self):
        """
        Test loading configuration when the file does not exist.
        """
        config = load_config('nonexistent.ini')
        self.assertEqual(config['game']['game_mode'], 'man_vs_ai')
        self.assertEqual(config['game']['player_score'], '0')
        self.assertEqual(config['game']['ai_score'], '0')

    def test_save_and_load_config(self):
        """
        Test saving and then loading configuration.
        """
        config = configparser.ConfigParser()
        config['game'] = {
            'game_mode': 'man_vs_ai',
            'player_score': '3',
            'ai_score': '2'
        }
        save_config(config, 'test_config.ini')

        loaded_config = load_config('test_config.ini')
        self.assertEqual(loaded_config['game']['player_score'], '3')
        self.assertEqual(loaded_config['game']['ai_score'], '2')

        # Clean up
        os.remove('test_config.ini')

    def test_config_with_missing_keys(self):
        """
        Test loading a configuration with missing keys.
        """
        config = configparser.ConfigParser()
        config['game'] = {
            'player_score': '5'
        }
        save_config(config, 'test_missing_keys.ini')

        loaded_config = load_config('test_missing_keys.ini')
        self.assertEqual(loaded_config['game']['player_score'], '5')
        self.assertEqual(loaded_config['game']['ai_score'], '0')  # Default value
        self.assertEqual(loaded_config['game']['game_mode'], 'man_vs_ai')  # Default value

        # Clean up
        os.remove('test_missing_keys.ini')

    def test_empty_config(self):
        """
        Test loading an empty configuration file.
        """
        open('test_empty.ini', 'w').close()  # Create an empty file
        config = load_config('test_empty.ini')
        self.assertEqual(config['game']['game_mode'], 'man_vs_ai')
        self.assertEqual(config['game']['player_score'], '0')
        self.assertEqual(config['game']['ai_score'], '0')

        # Clean up
        os.remove('test_empty.ini')

    def test_play_command_logic(self):
        """
        Test full logic of play command with various player and server choices.
        """
        choices = ['rock', 'paper', 'scissors']

        for player_choice in choices:
            for server_choice in choices:
                result = get_winner(player_choice, server_choice)
                if player_choice == server_choice:
                    self.assertEqual(result, "draw")
                elif (player_choice == "rock" and server_choice == "scissors") or \
                     (player_choice == "scissors" and server_choice == "paper") or \
                     (player_choice == "paper" and server_choice == "rock"):
                    self.assertEqual(result, "player")
                else:
                    self.assertEqual(result, "server")
    def test_config_with_missing_moves(self):
        """
        Test loading a configuration where the 'moves' section is missing keys.
        """
        config = configparser.ConfigParser()
        config['game'] = {
            'game_mode': 'man_vs_ai',
            'player_score': '2',
            'ai_score': '3'
        }
        config['moves'] = {}  # Intentionally leave out keys
        save_config(config, 'test_missing_moves.ini')

        loaded_config = load_config('test_missing_moves.ini')

        # Verify that default values are added for missing keys
        self.assertEqual(loaded_config['moves']['player_moves'], '')  # Default value
        self.assertEqual(loaded_config['moves']['ai_moves'], '')  # Default value
        self.assertEqual(loaded_config['game']['player_score'], '2')
        self.assertEqual(loaded_config['game']['ai_score'], '3')

        # Clean up
        os.remove('test_missing_moves.ini')

if __name__ == '__main__':
    unittest.main()
