"""Unit tests for the ChessDecrypter class in src/utils/decrypt.py."""
import os

import chess
import chess.pgn
import pytest

from utils import chess as chess_utils
from utils.decrypt import ChessDecrypter


@pytest.fixture
def input_dir(tmp_path):
    """Create a temporary input directory."""
    return str(tmp_path / "input")


@pytest.fixture
def output_file(tmp_path):
    """Create a temporary output file path."""
    return str(tmp_path / "output.bin")


def write_pgn_game(input_dir, moves, filename="game_0.pgn"):
    """Write a PGN game file with the given moves."""
    os.makedirs(input_dir, exist_ok=True)
    board = chess_utils.new_game()
    game = chess.pgn.Game()
    node = game
    for move in moves:
        node = node.add_variation(chess.Move.from_uci(move))
        board = chess_utils.make_move(board, move)
    file_path = os.path.join(input_dir, filename)
    with open(file_path, "w") as f:
        f.write(str(game))
    return file_path


class TestInit:
    """Tests for the ChessDecrypter constructor."""

    def test_initializes_game(self, input_dir, output_file):
        """The constructor should initialize a new game."""
        decrypter = ChessDecrypter(
            input_dir=input_dir, output_file=output_file
        )
        assert isinstance(decrypter.game, type(chess_utils.new_game()))

    def test_bits_start_empty(self, input_dir, output_file):
        """The bits list should start empty."""
        decrypter = ChessDecrypter(
            input_dir=input_dir, output_file=output_file
        )
        assert decrypter.bits == []

    def test_decoded_bytes_start_empty(self, input_dir, output_file):
        """The decoded bytes list should start empty."""
        decrypter = ChessDecrypter(
            input_dir=input_dir, output_file=output_file
        )
        assert decrypter.decoded_bytes == []


class TestProcessMove:
    """Tests for the process_move method."""

    def test_decodes_zero_bit(self, input_dir, output_file):
        """process_move should decode a 0 bit from the first move."""
        decrypter = ChessDecrypter(
            input_dir=input_dir, output_file=output_file
        )
        possible_moves = chess_utils.get_possible_moves(decrypter.game)
        move = chess.Move.from_uci(possible_moves[0])
        decrypter.process_move(move)
        assert decrypter.bits == ["0"]

    def test_decodes_one_bit(self, input_dir, output_file):
        """process_move should decode a 1 bit from the second move."""
        decrypter = ChessDecrypter(
            input_dir=input_dir, output_file=output_file
        )
        possible_moves = chess_utils.get_possible_moves(decrypter.game)
        move = chess.Move.from_uci(possible_moves[1])
        decrypter.process_move(move)
        assert decrypter.bits == ["1"]

    def test_collects_full_byte(self, input_dir, output_file):
        """process_move should collect a full byte after 8 bits."""
        decrypter = ChessDecrypter(
            input_dir=input_dir, output_file=output_file
        )
        # Encode byte 0x00 (8 zero bits)
        for _ in range(8):
            possible_moves = chess_utils.get_possible_moves(decrypter.game)
            move = chess.Move.from_uci(possible_moves[0])
            decrypter.process_move(move)
        assert decrypter.decoded_bytes == [0]
        assert decrypter.bits == []

    def test_collects_byte_of_ones(self, input_dir, output_file):
        """process_move should collect a byte of all ones."""
        decrypter = ChessDecrypter(
            input_dir=input_dir, output_file=output_file
        )
        # Encode byte 0xFF (8 one bits)
        for _ in range(8):
            possible_moves = chess_utils.get_possible_moves(decrypter.game)
            move = chess.Move.from_uci(possible_moves[1])
            decrypter.process_move(move)
        assert decrypter.decoded_bytes == [255]
        assert decrypter.bits == []

    def test_raises_on_unexpected_move(self, input_dir, output_file):
        """process_move should raise on a move not in the first two."""
        decrypter = ChessDecrypter(
            input_dir=input_dir, output_file=output_file
        )
        possible_moves = chess_utils.get_possible_moves(decrypter.game)
        # Pick a move that is not the first or second possible move
        unexpected = possible_moves[2]
        move = chess.Move.from_uci(unexpected)
        with pytest.raises(ValueError):
            decrypter.process_move(move)

    def test_updates_board(self, input_dir, output_file):
        """process_move should update the board state."""
        decrypter = ChessDecrypter(
            input_dir=input_dir, output_file=output_file
        )
        possible_moves = chess_utils.get_possible_moves(decrypter.game)
        move = chess.Move.from_uci(possible_moves[0])
        before = decrypter.game.fen()
        decrypter.process_move(move)
        assert decrypter.game.fen() != before


class TestDecrypt:
    """Tests for the decrypt method."""

    def test_decrypts_single_game(self, input_dir, output_file):
        """decrypt should decode a single game file."""
        # Create a game that encodes byte 0x00 (8 zero bits)
        board = chess_utils.new_game()
        moves = []
        for _ in range(8):
            possible_moves = chess_utils.get_possible_moves(board)
            move = possible_moves[0]
            moves.append(move)
            board = chess_utils.make_move(board, move)
        write_pgn_game(input_dir, moves)

        decrypter = ChessDecrypter(
            input_dir=input_dir, output_file=output_file
        )
        decrypter.decrypt()
        assert os.path.exists(output_file)
        with open(output_file, "rb") as f:
            data = f.read()
        assert data == b"\x00"

    def test_decrypts_multiple_bytes(self, input_dir, output_file):
        """decrypt should decode multiple bytes."""
        # Create a game that encodes bytes 0x00 0xFF
        board = chess_utils.new_game()
        moves = []
        # Byte 0x00: 8 zero bits
        for _ in range(8):
            possible_moves = chess_utils.get_possible_moves(board)
            move = possible_moves[0]
            moves.append(move)
            board = chess_utils.make_move(board, move)
        # Byte 0xFF: 8 one bits
        for _ in range(8):
            possible_moves = chess_utils.get_possible_moves(board)
            move = possible_moves[1]
            moves.append(move)
            board = chess_utils.make_move(board, move)
        write_pgn_game(input_dir, moves)

        decrypter = ChessDecrypter(
            input_dir=input_dir, output_file=output_file
        )
        decrypter.decrypt()
        with open(output_file, "rb") as f:
            data = f.read()
        assert data == b"\x00\xff"

    def test_decrypts_multiple_games(self, input_dir, output_file):
        """decrypt should decode across multiple game files."""
        # Game 0 encodes byte 0x00
        board = chess_utils.new_game()
        moves = []
        for _ in range(8):
            possible_moves = chess_utils.get_possible_moves(board)
            move = possible_moves[0]
            moves.append(move)
            board = chess_utils.make_move(board, move)
        write_pgn_game(input_dir, moves, "game_0.pgn")

        # Game 1 encodes byte 0xFF
        board = chess_utils.new_game()
        moves = []
        for _ in range(8):
            possible_moves = chess_utils.get_possible_moves(board)
            move = possible_moves[1]
            moves.append(move)
            board = chess_utils.make_move(board, move)
        write_pgn_game(input_dir, moves, "game_1.pgn")

        decrypter = ChessDecrypter(
            input_dir=input_dir, output_file=output_file
        )
        decrypter.decrypt()
        with open(output_file, "rb") as f:
            data = f.read()
        assert data == b"\x00\xff"

    def test_round_trip(self, tmp_path):
        """Encrypt then decrypt should recover the original data."""
        from utils.encrypt import ChessEncrypter

        input_file = tmp_path / "input.bin"
        input_file.write_bytes(b"Hello, world!")
        output_dir = str(tmp_path / "output")
        decrypted_file = str(tmp_path / "decrypted.bin")

        # Encrypt
        encrypter = ChessEncrypter(
            input_file=str(input_file), output_dir=output_dir
        )
        encrypter.encrypt()

        # Decrypt
        decrypter = ChessDecrypter(
            input_dir=output_dir, output_file=decrypted_file
        )
        decrypter.decrypt()

        # Verify
        with open(decrypted_file, "rb") as f:
            data = f.read()
        assert data == b"Hello, world!"
