import random
import chess
import chess.pgn


def new_game() -> chess.Board:
    """Initialize a new chess game and return the board state"""
    return chess.Board()


def get_possible_moves(board: chess.Board, seed: int = 0) -> list:
    """Get a shuffled list of all possible moves for a given position.

    The shuffle is deterministic: it uses the seed combined with the
    current move number (board.ply()) so that the same seed produces the
    same order at each move, allowing encryption and decryption to agree.
    """
    moves = sorted(m.uci() for m in board.legal_moves)
    rng = random.Random(seed + board.ply())
    rng.shuffle(moves)
    return moves


def make_move(board: chess.Board, move: str) -> chess.Board:
    """Make a move on the board and return the new board state"""
    new_board = board.copy()
    new_board.push(chess.Move.from_uci(move))
    return new_board


def is_game_over(board: chess.Board) -> bool:
    """Check if the game is over"""
    return board.is_game_over()


def write_game_to_file(board: chess.Board, file_path: str) -> None:
    """Write the game moves to a file in PGN format"""
    game = chess.pgn.Game.from_board(board)
    with open(file_path, "w") as f:
        f.write(str(game))
