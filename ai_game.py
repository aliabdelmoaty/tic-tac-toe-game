import tkinter as tk
from tkinter import messagebox
from typing import Optional, List, Dict, Set
from dataclasses import dataclass
from base_game_gui import BaseGameGUI
from player import Player
from move import Move
from game_state import GameState
from theme import Theme
import heapq

@dataclass
class Node:
    state: GameState
    move: Move
    g_cost: float  # Cost from start
    h_cost: float  # Heuristic cost
    parent: Optional['Node'] = None

    def f_cost(self) -> float:
        return self.g_cost + self.h_cost

    def __lt__(self, other):
        return self.f_cost() < other.f_cost()

class AIGame(BaseGameGUI):
    def __init__(self, window: tk.Tk, theme: Theme):
        super().__init__(window, theme)
        self.create_base_gui("Tic Tac Toe vs AI")
        self.on_back_to_menu = None

    def _handle_move(self, row: int, col: int):
        if self.board.grid[row][col] == Player.EMPTY and self.current_player == Player.X:
            move = Move(row, col)
            self._make_player_move(move)
            if not self._check_game_end(Player.X):
                self.current_player = Player.O
                self.turn_indicator.configure(text=self._get_turn_text())
                self.window.after(500, self._make_ai_move)

    def _make_player_move(self, move: Move):
        if self.board.make_move(move, Player.X):
            button = self.buttons[move.row][move.col]
            button.configure(
                text=Player.X.value,
                fg=self.current_theme.value['x_color']
            )

    def _make_ai_move(self):
        move = self._get_ai_move()
        if move:
            if self.board.make_move(move, Player.O):
                button = self.buttons[move.row][move.col]
                button.configure(
                    text=Player.O.value,
                    fg=self.current_theme.value['o_color']
                )
                if not self._check_game_end(Player.O):
                    self.current_player = Player.X
                    self.turn_indicator.configure(text=self._get_turn_text())

    def _get_ai_move(self) -> Optional[Move]:
        # Handle first move specially
        if all(cell == Player.EMPTY for row in self.board.grid for cell in row):
            if self.board.grid[1][1] == Player.EMPTY:
                return Move(1, 1)
            return Move(0, 0)

        initial_state = GameState([row.copy() for row in self.board.grid], Player.O)
        return self._a_star_search(initial_state)

    def _calculate_heuristic(self, state: GameState) -> float:
        # Heuristic function that evaluates board state
        score = 0.0
        
        # Check rows, columns, and diagonals
        for i in range(state.size):
            # Rows
            row = [state.grid[i][j] for j in range(state.size)]
            score += self._evaluate_line(row)
            
            # Columns
            col = [state.grid[j][i] for j in range(state.size)]
            score += self._evaluate_line(col)

        # Diagonals
        diag1 = [state.grid[i][i] for i in range(state.size)]
        diag2 = [state.grid[i][state.size-1-i] for i in range(state.size)]
        score += self._evaluate_line(diag1)
        score += self._evaluate_line(diag2)

        return score

    def _evaluate_line(self, line: List[Player]) -> float:
        o_count = line.count(Player.O)
        x_count = line.count(Player.X)
        empty_count = line.count(Player.EMPTY)

        if o_count == 3:
            return 100.0  # Win for O
        elif x_count == 3:
            return -100.0  # Win for X
        elif o_count == 2 and empty_count == 1:
            return 10.0  # Potential win for O
        elif x_count == 2 and empty_count == 1:
            return -10.0  # Potential win for X
        elif o_count == 1 and empty_count == 2:
            return 1.0  # Early advantage for O
        elif x_count == 1 and empty_count == 2:
            return -1.0  # Early advantage for X
        return 0.0

    def _a_star_search(self, initial_state: GameState) -> Optional[Move]:
        open_set: List[Node] = []
        closed_set: Set[str] = set()
        
        # Create start node
        start_node = Node(
            state=initial_state,
            move=None,
            g_cost=0,
            h_cost=self._calculate_heuristic(initial_state)
        )
        
        heapq.heappush(open_set, start_node)
        
        while open_set:
            current = heapq.heappop(open_set)
            
            # Skip if we've already explored this state
            state_hash = str([str(row) for row in current.state.grid])
            if state_hash in closed_set:
                continue
                
            closed_set.add(state_hash)
            
            # Check if this is a winning state
            if current.state.check_winner(Player.O):
                # Backtrack to get the initial move
                while current.parent and current.parent.parent:
                    current = current.parent
                return current.move
            
            # Generate successors
            for next_state, move in current.state.get_successors():
                if str([str(row) for row in next_state.grid]) in closed_set:
                    continue
                    
                g_cost = current.g_cost + 1
                h_cost = self._calculate_heuristic(next_state)
                
                successor = Node(
                    state=next_state,
                    move=move,
                    g_cost=g_cost,
                    h_cost=h_cost,
                    parent=current
                )
                
                heapq.heappush(open_set, successor)
        
        # If no winning path found, return the move with the best heuristic value
        best_move = None
        best_value = float('-inf')
        
        for next_state, move in initial_state.get_successors():
            value = self._calculate_heuristic(next_state)
            if value > best_value:
                best_value = value
                best_move = move
                
        return best_move

    def _check_game_end(self, player: Player) -> bool:
        if self.board.check_winner(player):
            self.update_scores(player)
            messagebox.showinfo("Game Over",
                              f"{'Player' if player == Player.X else 'AI'} {player.value} wins!")
            self.reset_board()
            return True

        if self.board.is_full():
            messagebox.showinfo("Game Over", "It's a tie!")
            self.reset_board()
            return True

        return False