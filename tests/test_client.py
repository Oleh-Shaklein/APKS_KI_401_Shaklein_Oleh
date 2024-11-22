import unittest
from unittest.mock import patch, MagicMock
from client import run_client, display_menu


class TestClient(unittest.TestCase):
    @patch('builtins.input', side_effect=['4', 'rock', '5'])
    def test_menu_play_move(self, mock_input):
        """
        Test that choosing '4' for playing a move sends the correct command.
        """
        with patch('client.serial.Serial') as mock_serial:
            mock_serial_instance = mock_serial.return_value
            mock_serial_instance.readline.return_value = b'Player: rock, Server: scissors, Result: player wins\n'

            try:
                run_client()
            except SystemExit:
                pass  # Expected behavior when exiting the client.

            # Verify that the 'play' command was sent to the server
            mock_serial_instance.write.assert_any_call(b'play rock\n')

    @patch('builtins.input', side_effect=['5'])
    def test_menu_exit(self, mock_input):
        """
        Test that choosing '5' for exiting does not raise an error.
        """
        with patch('client.serial.Serial') as mock_serial:
            mock_serial_instance = mock_serial.return_value
            mock_serial_instance.readline.return_value = b'Exiting game.\n'
            try:
                run_client()
            except SystemExit:
                pass


if __name__ == '__main__':
    unittest.main()
