from utils import chess as mychess
import os
import chess.pgn


class ChessDecrypter:
    def __init__(
        self,
        input_dir,
        output_file="examples/ex1_text/decrypted_output.txt",
    ):

        self.input_dir = input_dir
        self.output_file = output_file
        self.game = mychess.new_game()
        self.bits = []
        self.decoded_bytes = []

    def decrypt(self):
        # Read all game files in the input directory
        game_files = sorted(f for f in os.listdir(self.input_dir) if f.endswith(".pgn"))

        for game_file in game_files:
            file_path = os.path.join(self.input_dir, game_file)
            with open(file_path, "r") as f:
                game = chess.pgn.read_game(f)
            self.game = mychess.new_game()
            for move in game.mainline_moves():
                self.process_move(move)

        # Write the decoded bytes to the output file
        with open(self.output_file, "wb") as f:
            f.write(bytes(self.decoded_bytes))

        print(f"Decrypted {len(game_files)} games to {self.output_file}")

    def process_move(self, move):
        possible_moves = mychess.get_possible_moves(self.game)
        if len(possible_moves) >= 2:
            # Data move: decode the bit
            if move.uci() == possible_moves[0]:
                self.bits.append("0")
            elif move.uci() == possible_moves[1]:
                self.bits.append("1")
            else:
                raise ValueError(f"Unexpected move {move.uci()} not in possible moves")

            # Collect a full byte
            if len(self.bits) == 8:
                byte = int("".join(self.bits), 2)
                self.decoded_bytes.append(byte)
                self.bits = []

        # Make the move on the board (forced moves are padding, no bit)
        self.game = mychess.make_move(self.game, move.uci())
