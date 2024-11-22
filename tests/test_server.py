import unittest
from server import get_winner, load_config, save_config
import configparser

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

if __name__ == '__main__':
    unittest.main()
