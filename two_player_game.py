import tkinter as tk
from tkinter import messagebox
from base_game_gui import BaseGameGUI
from player import Player
from move import Move
from theme import Theme

class TwoPlayerGame(BaseGameGUI):
    def __init__(self, window: tk.Tk, theme: Theme):
        super().__init__(window, theme)
        self.create_base_gui("Tic Tac Toe - 2 Players")
        self.on_back_to_menu = None

    def _handle_move(self, row: int, col: int):
        if self.board.grid[row][col] == Player.EMPTY:
            move = Move(row, col)
            self._make_move(move)

    def _make_move(self, move: Move):
        if self.board.make_move(move, self.current_player):
            button = self.buttons[move.row][move.col]
            button.configure(
                text=self.current_player.value,
                fg=self.current_theme.value['x_color' if self.current_player == Player.X else 'o_color']
            )

            if not self._check_game_end():
                self.current_player = Player.O if self.current_player == Player.X else Player.X
                self.turn_indicator.configure(text=self._get_turn_text())

    def _check_game_end(self) -> bool:
        if self.board.check_winner(self.current_player):
            self.update_scores(self.current_player)
            messagebox.showinfo("Game Over", f"Player {self.current_player.value} wins!")
            self.reset_board()
            return True

        if self.board.is_full():
            messagebox.showinfo("Game Over", "It's a tie!")
            self.reset_board()
            return True

        return False
 