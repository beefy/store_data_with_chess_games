import chess


def new_game() -> str:
    """Initialize a new chess game and return the board state"""
    return chess.STARTING_FEN


def get_possible_moves(board: str, position: str) -> list:
    """Get an ordered list of possible moves for a piece at a position"""

    b = chess.Board(board)
    square = chess.parse_square(position)
    moves = [m for m in b.legal_moves if m.from_square == square]
    return [chess.square_name(m.to_square) for m in moves]


def make_move(board: str, from_pos: str, to_pos: str) -> str:
    """Make a move on the board and return the new board state"""
    b = chess.Board(board)
    move = chess.Move.from_uci(from_pos + to_pos)
    b.push(move)
    return b.fen()


def is_game_over(board: str) -> bool:
    """Check if the game is over"""
    return chess.Board(board).is_game_over()
