"""Unit tests for the chess utility functions in src/utils/chess.py."""
import chess

from utils import chess as chess_utils


class TestNewGame:
    """Tests for the new_game function."""

    def test_returns_board_object(self):
        """new_game should return a chess.Board instance."""
        board = chess_utils.new_game()
        assert isinstance(board, chess.Board)

    def test_starts_at_initial_position(self):
        """new_game should return a board at the starting position."""
        board = chess_utils.new_game()
        assert board.fen() == chess.STARTING_FEN

    def test_white_to_move(self):
        """new_game should have white to move."""
        board = chess_utils.new_game()
        assert board.turn == chess.WHITE


class TestGetPossibleMoves:
    """Tests for the get_possible_moves function."""

    def test_returns_list(self):
        """get_possible_moves should return a list."""
        board = chess_utils.new_game()
        moves = chess_utils.get_possible_moves(board)
        assert isinstance(moves, list)

    def test_returns_all_legal_moves(self):
        """get_possible_moves should return all legal moves."""
        board = chess_utils.new_game()
        moves = chess_utils.get_possible_moves(board)
        expected = sorted(m.uci() for m in board.legal_moves)
        assert sorted(moves) == expected

    def test_starting_position_has_20_moves(self):
        """The starting position should have 20 legal moves."""
        board = chess_utils.new_game()
        moves = chess_utils.get_possible_moves(board)
        assert len(moves) == 20

    def test_deterministic_with_same_seed(self):
        """Same seed should produce the same shuffled order."""
        board = chess_utils.new_game()
        moves1 = chess_utils.get_possible_moves(board, seed=42)
        moves2 = chess_utils.get_possible_moves(board, seed=42)
        assert moves1 == moves2

    def test_different_seed_produces_different_order(self):
        """Different seeds should produce different orders."""
        board = chess_utils.new_game()
        moves1 = chess_utils.get_possible_moves(board, seed=1)
        moves2 = chess_utils.get_possible_moves(board, seed=2)
        assert moves1 != moves2

    def test_seed_changes_with_move_number(self):
        """The shuffle should change as the move number changes."""
        board = chess_utils.new_game()
        moves1 = chess_utils.get_possible_moves(board, seed=42)
        board2 = chess_utils.make_move(board, moves1[0])
        moves2 = chess_utils.get_possible_moves(board2, seed=42)
        assert moves1 != moves2

    def test_default_seed_is_zero(self):
        """The default seed should be 0."""
        board = chess_utils.new_game()
        moves_default = chess_utils.get_possible_moves(board)
        moves_seed0 = chess_utils.get_possible_moves(board, seed=0)
        assert moves_default == moves_seed0


class TestMakeMove:
    """Tests for the make_move function."""

    def test_returns_board_object(self):
        """make_move should return a chess.Board instance."""
        board = chess_utils.new_game()
        new_board = chess_utils.make_move(board, "e2e4")
        assert isinstance(new_board, chess.Board)

    def test_makes_the_move(self):
        """make_move should apply the move to the board."""
        board = chess_utils.new_game()
        new_board = chess_utils.make_move(board, "e2e4")
        assert new_board.piece_at(chess.E4) == chess.Piece(
            chess.PAWN, chess.WHITE
        )

    def test_does_not_mutate_original(self):
        """make_move should not modify the original board."""
        board = chess_utils.new_game()
        original_fen = board.fen()
        chess_utils.make_move(board, "e2e4")
        assert board.fen() == original_fen

    def test_returns_new_board(self):
        """make_move should return a new board, not the same object."""
        board = chess_utils.new_game()
        new_board = chess_utils.make_move(board, "e2e4")
        assert new_board is not board

    def test_turn_changes(self):
        """After a move, it should be the other player's turn."""
        board = chess_utils.new_game()
        new_board = chess_utils.make_move(board, "e2e4")
        assert new_board.turn == chess.BLACK

    def test_applies_move_without_validation(self):
        """make_move applies the move even if it is not a legal chess move.

        The underlying chess.Board.push() does not validate moves, so
        make_move applies whatever UCI move string it is given.
        """
        board = chess_utils.new_game()
        new_board = chess_utils.make_move(board, "e2e5")
        assert new_board.piece_at(chess.E5) == chess.Piece(
            chess.PAWN, chess.WHITE
        )



class TestIsGameOver:
    """Tests for the is_game_over function."""

    def test_new_game_not_over(self):
        """A new game should not be over."""
        board = chess_utils.new_game()
        assert chess_utils.is_game_over(board) is False

    def test_returns_bool(self):
        """is_game_over should return a boolean."""
        board = chess_utils.new_game()
        result = chess_utils.is_game_over(board)
        assert isinstance(result, bool)


class TestWriteGameToFile:
    """Tests for the write_game_to_file function."""

    def test_writes_pgn_file(self, tmp_path):
        """write_game_to_file should create a PGN file."""
        board = chess_utils.new_game()
        board = chess_utils.make_move(board, "e2e4")
        board = chess_utils.make_move(board, "e7e5")
        file_path = tmp_path / "game.pgn"
        chess_utils.write_game_to_file(board, str(file_path))
        assert file_path.exists()

    def test_file_contains_moves(self, tmp_path):
        """The PGN file should contain the moves."""
        board = chess_utils.new_game()
        board = chess_utils.make_move(board, "e2e4")
        board = chess_utils.make_move(board, "e7e5")
        file_path = tmp_path / "game.pgn"
        chess_utils.write_game_to_file(board, str(file_path))
        content = file_path.read_text()
        assert "e4" in content
        assert "e5" in content

    def test_file_is_valid_pgn(self, tmp_path):
        """The written file should be readable as a PGN game."""
        board = chess_utils.new_game()
        board = chess_utils.make_move(board, "e2e4")
        file_path = tmp_path / "game.pgn"
        chess_utils.write_game_to_file(board, str(file_path))
        with open(file_path, "r") as f:
            game = chess.pgn.read_game(f)
        assert game is not None
