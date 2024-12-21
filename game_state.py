from typing import List, Tuple
from player import Player
from move import Move

class GameState:
    def __init__(self, grid: List[List[Player]], player: Player):
        self.grid = grid
        self.player = player
        self.size = len(grid)

    def get_successors(self) -> List[Tuple['GameState', Move]]:
        successors = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == Player.EMPTY:
                    new_grid = [row.copy() for row in self.grid]
                    new_grid[i][j] = self.player
                    next_player = Player.X if self.player == Player.O else Player.O
                    successors.append(
                        (GameState(new_grid, next_player), Move(i, j))
                    )
        return successors

    def is_terminal(self) -> bool:
        return self.check_winner(Player.X) or self.check_winner(Player.O) or \
               all(cell != Player.EMPTY for row in self.grid for cell in row)

    def check_winner(self, player: Player) -> bool:
        for i in range(self.size):
            if all(self.grid[i][j] == player for j in range(self.size)) or \
               all(self.grid[j][i] == player for j in range(self.size)):
                return True

        if all(self.grid[i][i] == player for i in range(self.size)) or \
           all(self.grid[i][self.size - 1 - i] == player for i in range(self.size)):
            return True
        return False

    def evaluate(self) -> float:
        if self.check_winner(Player.O):
            return 1.0
        elif self.check_winner(Player.X):
            return -1.0
        return 0.0