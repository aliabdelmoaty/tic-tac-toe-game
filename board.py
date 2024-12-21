from typing import List
from player import Player
from move import Move

class Board:
    def __init__(self, size: int = 3):
        self.size = size
        self.clear()

    def make_move(self, move: Move, player: Player) -> bool:
        if self.grid[move.row][move.col] == Player.EMPTY:
            self.grid[move.row][move.col] = player
            return True
        return False

    def is_full(self) -> bool:
        return all(cell != Player.EMPTY for row in self.grid for cell in row)

    def clear(self):
        self.grid = [[Player.EMPTY for _ in range(self.size)] for _ in range(self.size)]

    def check_winner(self, player: Player) -> bool:
        for i in range(self.size):
            if all(self.grid[i][j] == player for j in range(self.size)) or \
                    all(self.grid[j][i] == player for j in range(self.size)):
                return True

        if all(self.grid[i][i] == player for i in range(self.size)) or \
                all(self.grid[i][self.size - 1 - i] == player for i in range(self.size)):
            return True
        return False