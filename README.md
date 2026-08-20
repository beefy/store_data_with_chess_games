## Overview

Convert data into chess games and vice versa!

Operation for encrypting into chess:
  1. New game.
  2. Get the list of possible moves - shuffled with a known seed.
  3. If you need to store a 0, play the first move.
  4. If you need to store a 1, play the second move.
  5. If there is only one possible move, skip the storage and play the move.
  6. If the game ends, start a new game.

## Usage

Convert a text file to chess games
```
PYTHONPATH=src python src/main.py --encrypt --input=examples/ex1_text/input.txt --output=examples/ex1_text/output
```

Convert chess games to a text file
```
PYTHONPATH=src python src/main.py --decrypt --input=examples/ex1_text/output --output=examples/ex1_text/input2.txt 
```
