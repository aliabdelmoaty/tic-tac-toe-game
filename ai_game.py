import tkinter as tk
from tkinter import messagebox
from typing import Optional  # Add this import
from base_game_gui import BaseGameGUI
from player import Player
from move import Move
from game_state import GameState
from theme import Theme

class AIGame(BaseGameGUI):  # Define a class AIGame that inherits from BaseGameGUI for AI vs Player game
    def __init__(self, window: tk.Tk, theme: Theme):
        super().__init__(window, theme)  # Initialize the base class
        self.create_base_gui("Tic Tac Toe vs AI")  # Create the base GUI with the title
        self.on_back_to_menu = None
    def _handle_move(self, row: int, col: int):
        if self.board.grid[row][col] == Player.EMPTY and self.current_player == Player.X:  # Check if the cell is empty and it's the player's turn
            move = Move(row, col)  # Create a move object
            self._make_player_move(move)  # Make the player's move
            if not self._check_game_end(Player.X):  # Check if the game has ended after the player's move
                self.current_player = Player.O  # Switch to AI's turn
                self.turn_indicator.configure(text=self._get_turn_text())  # Update the turn indicator
                self.window.after(500, self._make_ai_move)  # Schedule the AI move after a delay

    def _make_player_move(self, move: Move):
        if self.board.make_move(move, Player.X):  # Make the move on the board
            button = self.buttons[move.row][move.col]  # Get the button for the move
            button.configure(
                text=Player.X.value,  # Set the button text to 'X'
                fg=self.current_theme.value['x_color']  # Set the button color for 'X'
            )

    def _make_ai_move(self):
        move = self._get_ai_move()  # Get the best move for the AI
        if move:
            if self.board.make_move(move, Player.O):  # Make the move on the board
                button = self.buttons[move.row][move.col]  # Get the button for the move
                button.configure(
                    text=Player.O.value,  # Set the button text to 'O'
                    fg=self.current_theme.value['o_color']  # Set the button color for 'O'
                )
                if not self._check_game_end(Player.O):  # Check if the game has ended after the AI's move
                    self.current_player = Player.X  # Switch to player's turn
                    self.turn_indicator.configure(text=self._get_turn_text())  # Update the turn indicator

    def _get_ai_move(self) -> Optional[Move]:
        initial_state = GameState([row.copy() for row in self.board.grid], Player.O)  # Create the initial game state for the AI
        
        if all(cell == Player.EMPTY for row in self.board.grid for cell in row):  # Check if the board is empty
            if self.board.grid[1][1] == Player.EMPTY:  # If the center is empty, take it
                return Move(1, 1)
            return Move(0, 0)  # Otherwise, take a corner
            
        best_score = float('-inf')  # Initialize the best score to negative infinity
        best_move = None  # Initialize the best move to None
        alpha = float('-inf')  # Initialize alpha for alpha-beta pruning
        beta = float('inf')  # Initialize beta for alpha-beta pruning
        
        for successor, move in initial_state.get_successors():  # Iterate over all possible moves
            score = self._minimax(successor, 5, False, alpha, beta)  # Evaluate the move using minimax algorithm
            if score > best_score:  # If the score is better than the best score
                best_score = score  # Update the best score
                best_move = move  # Update the best move
            alpha = max(alpha, best_score)  # Update alpha
            
        return best_move  # Return the best move

    def _minimax(self, state: GameState, depth: int, is_maximizing: bool, alpha: float, beta: float) -> float:
        if depth == 0 or state.is_terminal():  # Check if the maximum depth is reached or the state is terminal
            return state.evaluate()  # Return the evaluation of the state
            
        if is_maximizing:  # If the current player is maximizing
            max_eval = float('-inf')  # Initialize the maximum evaluation to negative infinity
            for successor, _ in state.get_successors():  # Iterate over all possible moves
                eval = self._minimax(successor, depth - 1, False, alpha, beta)  # Recursively evaluate the move
                max_eval = max(max_eval, eval)  # Update the maximum evaluation
                alpha = max(alpha, eval)  # Update alpha
                if beta <= alpha:  # If beta is less than or equal to alpha, prune the branch
                    break
            return max_eval  # Return the maximum evaluation
        else:  # If the current player is minimizing
            min_eval = float('inf')  # Initialize the minimum evaluation to infinity
            for successor, _ in state.get_successors():  # Iterate over all possible moves
                eval = self._minimax(successor, depth - 1, True, alpha, beta)  # Recursively evaluate the move
                min_eval = min(min_eval, eval)  # Update the minimum evaluation
                beta = min(beta, eval)  # Update beta
                if beta <= alpha:  # If beta is less than or equal to alpha, prune the branch
                    break
            return min_eval  # Return the minimum evaluation

    def _check_game_end(self, player: Player) -> bool:
        if self.board.check_winner(player):  # Check if the player has won
            self.update_scores(player)  # Update the scores
            messagebox.showinfo("Game Over",
                              f"{'Player' if player == Player.X else 'AI'} {player.value} wins!")  # Show a message box with the winner
            self.reset_board()  # Reset the board
            return True

        if self.board.is_full():  # Check if the board is full
            messagebox.showinfo("Game Over", "It's a tie!")  # Show a message box for a tie
            self.reset_board()  # Reset the board
            return True

        return False  # Return False if the game is not over
 