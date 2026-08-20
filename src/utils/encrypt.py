from src.utils import chess
import os

class ChessEncrypter:
    def __init__(self, input_file, output_dir="examples/ex1_text/output"):
        self.input_file = input_file
        self.output_dir = output_dir
        self.game = chess.new_game()
        self.game_counter = 0

        # mkdir for output_dir if not exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def encrypt(self):
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

    def check_game_over(self):
        if chess.is_game_over(self.game):
            print(f"Game {self.game_counter} is over. Writing to file and starting a new game.")
            chess.write_game_to_file(self.game, os.path.join(self.output_dir, f"game_{self.game_counter}.pgn"))
            self.game = chess.new_game()
            self.game_counter += 1

    def forced_moves(self):
        possible_moves = chess.get_possible_moves(self.game)
        while len(possible_moves) < 2 and not chess.is_game_over(self.game):
            move = possible_moves[0]
            self.game = chess.make_move(self.game, move)
            possible_moves = chess.get_possible_moves(self.game)

    def store_zero(self):
        self.check_game_over()
        self.forced_moves()
        possible_moves = chess.get_possible_moves(self.game)
        move = possible_moves[0]
        self.game = chess.make_move(self.game, move)

    def store_one(self):
        self.check_game_over()
        self.forced_moves()
        possible_moves = chess.get_possible_moves(self.game)
        move = possible_moves[1]
        self.game = chess.make_move(self.game, move)
