"""Unit tests for the CLI functions in src/main.py."""
from unittest import mock

import main


class TestEncryptFunction:
    """Tests for the encrypt function in main.py."""

    @mock.patch("main.ChessEncrypter")
    def test_calls_encrypter(self, mock_encrypter):
        """encrypt should create a ChessEncrypter and call encrypt."""
        main.encrypt("input.txt", "output_dir")
        mock_encrypter.assert_called_once_with(
            input_file="input.txt", output_dir="output_dir"
        )
        mock_encrypter.return_value.encrypt.assert_called_once()

    @mock.patch("main.ChessEncrypter")
    def test_returns_none(self, mock_encrypter):
        """encrypt should return None."""
        result = main.encrypt("input.txt", "output_dir")
        assert result is None


class TestDecryptFunction:
    """Tests for the decrypt function in main.py."""

    @mock.patch("main.ChessDecrypter")
    def test_calls_decrypter(self, mock_decrypter):
        """decrypt should create a ChessDecrypter and call decrypt."""
        main.decrypt("input_dir", "output.txt")
        mock_decrypter.assert_called_once_with(
            input_dir="input_dir", output_file="output.txt"
        )
        mock_decrypter.return_value.decrypt.assert_called_once()

    @mock.patch("main.ChessDecrypter")
    def test_returns_none(self, mock_decrypter):
        """decrypt should return None."""
        result = main.decrypt("input_dir", "output.txt")
        assert result is None
