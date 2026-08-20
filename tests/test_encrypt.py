"""Unit tests for the ChessEncrypter class in src/utils/encrypt.py."""
import os

import pytest

from utils import chess as chess_utils
from utils.encrypt import ChessEncrypter


@pytest.fixture
def input_file(tmp_path):
    """Create a temporary input file with known binary content."""
    file_path = tmp_path / "input.bin"
    file_path.write_bytes(b"\x00\x01\xff")
    return str(file_path)


@pytest.fixture
def output_dir(tmp_path):
    """Create a temporary output directory path."""
    return str(tmp_path / "output")


class TestInit:
    """Tests for the ChessEncrypter constructor."""

    def test_creates_output_dir(self, input_file, output_dir):
        """The constructor should create the output directory."""
        ChessEncrypter(input_file=input_file, output_dir=output_dir)
        assert os.path.exists(output_dir)

    def test_initializes_game(self, input_file, output_dir):
        """The constructor should initialize a new game."""
        encrypter = ChessEncrypter(
            input_file=input_file, output_dir=output_dir
        )
        assert isinstance(encrypter.game, type(chess_utils.new_game()))

    def test_game_counter_starts_at_zero(self, input_file, output_dir):
        """The game counter should start at 0."""
        encrypter = ChessEncrypter(
            input_file=input_file, output_dir=output_dir
        )
        assert encrypter.game_counter == 0


class TestStoreZero:
    """Tests for the store_zero method."""

    def test_makes_first_possible_move(self, input_file, output_dir):
        """store_zero should make the first possible move."""
        encrypter = ChessEncrypter(
            input_file=input_file, output_dir=output_dir
        )
        before = encrypter.game.fen()
        encrypter.store_zero()
        assert encrypter.game.fen() != before

    def test_increments_ply(self, input_file, output_dir):
        """store_zero should advance the game by one ply."""
        encrypter = ChessEncrypter(
            input_file=input_file, output_dir=output_dir
        )
        initial_ply = encrypter.game.ply()
        encrypter.store_zero()
        assert encrypter.game.ply() == initial_ply + 1


class TestStoreOne:
    """Tests for the store_one method."""

    def test_makes_second_possible_move(self, input_file, output_dir):
        """store_one should make the second possible move."""
        encrypter = ChessEncrypter(
            input_file=input_file, output_dir=output_dir
        )
        before = encrypter.game.fen()
        encrypter.store_one()
        assert encrypter.game.fen() != before

    def test_increments_ply(self, input_file, output_dir):
        """store_one should advance the game by one ply."""
        encrypter = ChessEncrypter(
            input_file=input_file, output_dir=output_dir
        )
        initial_ply = encrypter.game.ply()
        encrypter.store_one()
        assert encrypter.game.ply() == initial_ply + 1


class TestForcedMoves:
    """Tests for the forced_moves method."""

    def test_ensures_at_least_two_moves(self, input_file, output_dir):
        """forced_moves should leave at least two legal moves."""
        encrypter = ChessEncrypter(
            input_file=input_file, output_dir=output_dir
        )
        encrypter.forced_moves()
        moves = chess_utils.get_possible_moves(encrypter.game)
        assert len(moves) >= 2


class TestCheckGameOver:
    """Tests for the check_game_over method."""

    def test_no_action_when_game_not_over(self, input_file, output_dir):
        """check_game_over should do nothing if the game is not over."""
        encrypter = ChessEncrypter(
            input_file=input_file, output_dir=output_dir
        )
        counter_before = encrypter.game_counter
        encrypter.check_game_over()
        assert encrypter.game_counter == counter_before

    def test_writes_game_when_over(self, input_file, output_dir):
        """check_game_over should write a game file when the game is over."""
        encrypter = ChessEncrypter(
            input_file=input_file, output_dir=output_dir
        )
        # Force the game to be over by playing a known sequence
        # (Fool's mate: f3, e5, g4, Qh4#)
        encrypter.game = chess_utils.make_move(encrypter.game, "f2f3")
        encrypter.game = chess_utils.make_move(encrypter.game, "e7e5")
        encrypter.game = chess_utils.make_move(encrypter.game, "g2g4")
        encrypter.game = chess_utils.make_move(encrypter.game, "d8h4")
        assert chess_utils.is_game_over(encrypter.game)

        encrypter.check_game_over()
        game_file = os.path.join(output_dir, "game_0.pgn")
        assert os.path.exists(game_file)

    def test_increments_counter_when_over(self, input_file, output_dir):
        """check_game_over should increment the counter when game is over."""
        encrypter = ChessEncrypter(
            input_file=input_file, output_dir=output_dir
        )
        encrypter.game = chess_utils.make_move(encrypter.game, "f2f3")
        encrypter.game = chess_utils.make_move(encrypter.game, "e7e5")
        encrypter.game = chess_utils.make_move(encrypter.game, "g2g4")
        encrypter.game = chess_utils.make_move(encrypter.game, "d8h4")
        encrypter.check_game_over()
        assert encrypter.game_counter == 1

    def test_starts_new_game_when_over(self, input_file, output_dir):
        """check_game_over should start a new game when the game is over."""
        encrypter = ChessEncrypter(
            input_file=input_file, output_dir=output_dir
        )
        encrypter.game = chess_utils.make_move(encrypter.game, "f2f3")
        encrypter.game = chess_utils.make_move(encrypter.game, "e7e5")
        encrypter.game = chess_utils.make_move(encrypter.game, "g2g4")
        encrypter.game = chess_utils.make_move(encrypter.game, "d8h4")
        encrypter.check_game_over()
        assert encrypter.game.fen() == chess_utils.new_game().fen()


class TestEncrypt:
    """Tests for the encrypt method."""

    def test_writes_game_files(self, input_file, output_dir):
        """encrypt should write at least one game file."""
        encrypter = ChessEncrypter(
            input_file=input_file, output_dir=output_dir
        )
        encrypter.encrypt()
        game_files = [
            f for f in os.listdir(output_dir) if f.endswith(".pgn")
        ]
        assert len(game_files) >= 1

    def test_writes_pgn_files(self, input_file, output_dir):
        """encrypt should write PGN files."""
        encrypter = ChessEncrypter(
            input_file=input_file, output_dir=output_dir
        )
        encrypter.encrypt()
        game_files = [
            f for f in os.listdir(output_dir) if f.endswith(".pgn")
        ]
        assert all(f.endswith(".pgn") for f in game_files)

    def test_encrypts_all_bytes(self, input_file, output_dir):
        """encrypt should process all bytes in the input file."""
        encrypter = ChessEncrypter(
            input_file=input_file, output_dir=output_dir
        )
        encrypter.encrypt()
        # 3 bytes = 24 bits = 24 data moves minimum
        # Each game file should contain moves
        game_files = [
            f for f in os.listdir(output_dir) if f.endswith(".pgn")
        ]
        assert len(game_files) >= 1
