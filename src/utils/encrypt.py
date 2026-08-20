from src.utils import chess
import os

class ChessEncrypter:
    def __init__(self, data, output_dir="examples/ex1_text/output"):
        self.data = data
        self.output_dir = output_dir
        self.game = chess.new_game()
        self.game_counter = 0

        # mkdir for output_dir if not exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def encrypt(self):
        pass

    def check_game_over(self):
        if self.game.is_game_over():
            chess.write_game_to_file(self.game, os.path.join(self.output_dir, f"game_{self.game_counter}.pgn"))
            self.game = chess.new_game()
            self.game_counter += 1

    def store_zero(self):
        self.check_game_over()

        possible_moves = chess.get_possible_moves(self.game)
        while len(possible_moves) < 2:
            # WIP
            # chess.make_move(self.game, )
            # self.check_game_over()
            # possible_moves = chess.get_possible_moves(self.game)


