import chess


def new_game() -> str:
    """Initialize a new chess game and return the board state"""
    return chess.STARTING_FEN


def get_possible_moves(board: str) -> list:
    """Get an ordered list of all possible moves for a given position"""
    b = chess.Board(board)
    return sorted(m.uci() for m in b.legal_moves)


def make_move(board: str, from_pos: str, to_pos: str) -> str:
    """Make a move on the board and return the new board state"""
    b = chess.Board(board)
    move = chess.Move.from_uci(from_pos + to_pos)
    b.push(move)
    return b.fen()


def is_game_over(board: str) -> bool:
    """Check if the game is over"""
    return chess.Board(board).is_game_over()


def write_game_to_file(board: str, file_path: str) -> None:
    """Write the game moves to a file in PGN format"""
    b = chess.Board(board)
    game = chess.pgn.Game.from_board(b)
    with open(file_path, "w") as f:
        f.write(str(game))
