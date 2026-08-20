from utils import chess
import os

class ChessEncrypter:
    """Encrypt a binary file into a set of chess games.

    Each byte of the input file is converted to an 8-bit binary string,
    and each bit is encoded as a chess move. Bit 0 is stored as the first
    possible move and bit 1 as the second possible move. When a game runs
    out of legal moves, it is written to a PGN file and a new game begins.
    """

    def __init__(self, input_file, output_dir="examples/ex1_text/output"):
        """Initialize the encrypter with an input file and output directory."""
        self.input_file = input_file
        self.output_dir = output_dir
        self.game = chess.new_game()
        self.game_counter = 0

        # mkdir for output_dir if not exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def encrypt(self):
        """Encrypt the input file into chess game PGN files."""
        # Read input file as binary
        with open(self.input_file, "rb") as f:
            byte = f.read(1)
            while byte:
                # Convert byte to int
                byte_int = int.from_bytes(byte, "big")
                # Convert int to binary string
                binary_str = format(byte_int, "08b")
                # Store each bit in the chess game
                for bit in binary_str:
                    if bit == "0":
                        self.store_zero()
                    else:
                        self.store_one()
                # Read next byte
                byte = f.read(1)

        # Write the final game to a file
        chess.write_game_to_file(self.game, os.path.join(self.output_dir, f"game_{self.game_counter}.pgn"))
        print(f"Game {self.game_counter} is over. Writing to file and starting a new game.")

    def check_game_over(self):
        """Write the current game to a file and start a new one if over."""
        if chess.is_game_over(self.game):
            print(f"Game {self.game_counter} is over. Writing to file and starting a new game.")
            chess.write_game_to_file(self.game, os.path.join(self.output_dir, f"game_{self.game_counter}.pgn"))
            self.game = chess.new_game()
            self.game_counter += 1

    def forced_moves(self):
        """Make forced moves until there are at least two legal moves."""
        possible_moves = chess.get_possible_moves(self.game)
        while len(possible_moves) < 2 and not chess.is_game_over(self.game):
            move = possible_moves[0]
            self.game = chess.make_move(self.game, move)
            possible_moves = chess.get_possible_moves(self.game)

    def store_zero(self):
        """Encode a 0 bit by making the first possible move."""
        self.check_game_over()
        self.forced_moves()
        possible_moves = chess.get_possible_moves(self.game)
        move = possible_moves[0]
        self.game = chess.make_move(self.game, move)

    def store_one(self):
        """Encode a 1 bit by making the second possible move."""
        self.check_game_over()
        self.forced_moves()
        possible_moves = chess.get_possible_moves(self.game)
        move = possible_moves[1]
        self.game = chess.make_move(self.game, move)
