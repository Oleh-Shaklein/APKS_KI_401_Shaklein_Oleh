import unittest
from unittest.mock import patch, MagicMock
from client import run_client

class TestClient(unittest.TestCase):
    @patch("serial.Serial")
    def test_client_new_command(self, mock_serial):
        """
        Test sending the 'new' command from the client.
        """
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.write = MagicMock()
        mock_serial_instance.readline.return_value = b"New game started.\n"

        with patch("builtins.input", side_effect=["1", "5"]):  # New game and then exit
            run_client()

        mock_serial_instance.write.assert_any_call(b"new\n")

    @patch("serial.Serial")
    def test_client_save_command(self, mock_serial):
        """
        Test sending the 'save' command from the client.
        """
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.write = MagicMock()
        mock_serial_instance.readline.return_value = b"Game saved.\n"

        with patch("builtins.input", side_effect=["2", "5"]):  # Save game and then exit
            run_client()

        mock_serial_instance.write.assert_any_call(b"save\n")

    @patch("serial.Serial")
    def test_client_load_command(self, mock_serial):
        """
        Test sending the 'load' command from the client.
        """
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.write = MagicMock()
        mock_serial_instance.readline.return_value = b"Game loaded.\n"

        with patch("builtins.input", side_effect=["3", "5"]):  # Load game and then exit
            run_client()

        mock_serial_instance.write.assert_any_call(b"load\n")

    @patch("serial.Serial")
    def test_invalid_command(self, mock_serial):
        """
        Test invalid command input in the client.
        """
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.write = MagicMock()
        mock_serial_instance.readline.return_value = b"Invalid command.\n"

        with patch("builtins.input", side_effect=["6", "5"]):  # Invalid command and then exit
            run_client()

        # Ensure no unexpected write occurred for invalid command
        mock_serial_instance.write.assert_not_called()

if __name__ == "__main__":
    unittest.main()
