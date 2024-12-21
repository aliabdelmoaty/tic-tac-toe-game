import tkinter as tk
from tkinter import messagebox
from player import Player
from board import Board
from move import Move
from theme import Theme
from typing import Dict 
class BaseGameGUI:
    def __init__(self, window: tk.Tk, theme: Theme):
        self.window = window  # Store the main window
        self.current_theme = theme  # Store the current theme
        self.board = Board()  # Initialize the game board
        self.current_player = Player.X  # Set the starting player to X
        self.scores = {Player.X: 0, Player.O: 0}  # Initialize scores for both players
        self.on_back_to_menu = None  # Add this line

    def create_base_gui(self, title: str):
        self.main_container = self._create_container()  # Create the main container
        self._create_title(title)  # Create the title label
        self._create_scoreboard()  # Create the scoreboard
        self._create_game_board()  # Create the game board
        self._create_controls()  # Create control buttons
        self._create_turn_indicator()  # Create the turn indicator
        self.apply_theme()  # Apply the current theme to the GUI

    def _create_container(self) -> tk.Frame:
        container = tk.Frame(self.window, padx=20, pady=20)  # Create a frame with padding
        container.pack(expand=True, fill='both')  # Pack the frame to expand and fill the window
        return container  # Return the created frame

    def _create_title(self, title: str):
        self.title_label = tk.Label(
            self.main_container,
            text=title,
            font=('Helvetica', 24, 'bold'),
            pady=10
        )  # Create a label for the title with specified font and padding
        self.title_label.pack()  # Pack the title label

    def _create_scoreboard(self):
        self.score_frame = tk.Frame(self.main_container)  # Create a frame for the scoreboard
        self.score_frame.pack(pady=10)  # Pack the frame with padding

        self.score_labels = {}  # Initialize a dictionary to store score labels
        for player in [Player.X, Player.O]:
            self.score_labels[player] = tk.Label(
                self.score_frame,
                text=f"{'Player' if player == Player.X else 'AI/Player'} {player.value}: 0",
                font=('Helvetica', 12),
                padx=20
            )  # Create a label for each player's score
            self.score_labels[player].pack(side=tk.LEFT)  # Pack the score label to the left

    def _create_game_board(self):
        self.game_frame = tk.Frame(
            self.main_container,
            relief=tk.RIDGE,
            borderwidth=2
        )  # Create a frame for the game board with a ridge border
        self.game_frame.pack(pady=10)  # Pack the frame with padding
        self.buttons = self._create_board_buttons()  # Create buttons for the game board

    def _create_board_buttons(self):
        buttons = [[None for _ in range(self.board.size)]
                   for _ in range(self.board.size)]  # Initialize a 2D list for buttons

        for i in range(self.board.size):
            for j in range(self.board.size):
                buttons[i][j] = self._create_cell_button(i, j)  # Create a button for each cell

        return buttons  # Return the created buttons

    def _create_cell_button(self, row: int, col: int) -> tk.Button:
        button = tk.Button(
            self.game_frame,
            text='',
            font=('Helvetica', 24, 'bold'),
            width=3,
            height=1,
            relief=tk.FLAT,
            command=lambda: self._handle_move(row, col)
        )  # Create a button for a cell with specified properties and command
        button.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')  # Place the button in the grid
        button.bind('<Enter>', self._on_enter)  # Bind the enter event to change color on hover
        button.bind('<Leave>', self._on_leave)  # Bind the leave event to revert color on hover
        return button  # Return the created button

    def _create_controls(self):
        self.control_frame = tk.Frame(self.main_container)  # Create a frame for control buttons
        self.control_frame.pack(pady=10)  # Pack the frame with padding
        self._create_back_button()  # Create the back button
        self._create_theme_button()  # Create the theme toggle button
        self._create_reset_button()  # Create the reset button

    def _create_back_button(self):
        self.back_button = tk.Button(
            self.control_frame,
            text="↩ Back to Menu",
            command=self._back_to_menu,
            relief=tk.FLAT,
            font=('Helvetica', 10),
            padx=15,
            pady=5
        )  # Create a button to go back to the menu
        self.back_button.pack(side=tk.LEFT, padx=5)  # Pack the button to the left with padding
    def set_menu_callback(self, callback):
        self.on_back_to_menu = callback
    def _back_to_menu(self):
        if messagebox.askyesno("Confirm", "Return to main menu? Current game progress will be lost."):
            self.main_container.destroy()
            if self.on_back_to_menu:
                self.on_back_to_menu()

    def _create_theme_button(self):
        self.theme_button = tk.Button(
            self.control_frame,
            text=self._get_theme_button_text(),
            command=self._toggle_theme,
            relief=tk.FLAT,
            font=('Helvetica', 10),
            padx=15,
            pady=5
        )  # Create a button to toggle the theme
        self.theme_button.pack(side=tk.LEFT, padx=5)  # Pack the button to the left with padding

    def _create_reset_button(self):
        self.reset_button = tk.Button(
            self.control_frame,
            text="🔄 New Game",
            command=self.reset_game,
            relief=tk.FLAT,
            font=('Helvetica', 10),
            padx=15,
            pady=5
        )  # Create a button to reset the game
        self.reset_button.pack(side=tk.LEFT, padx=5)  # Pack the button to the left with padding

    def _create_turn_indicator(self):
        self.turn_indicator = tk.Label(
            self.main_container,
            text=self._get_turn_text(),
            font=('Helvetica', 12),
            pady=10
        )  # Create a label to indicate the current turn
        self.turn_indicator.pack()  # Pack the turn indicator

    def _get_theme_button_text(self) -> str:
        return "🌙 Dark Mode" if self.current_theme == Theme.LIGHT else "☀️ Light Mode"  # Return the appropriate text for the theme button

    def _get_turn_text(self) -> str:
        return f"Current Turn: {'Player' if self.current_player == Player.X else 'AI/Player'} {self.current_player.value}"  # Return the text indicating the current turn

    def _toggle_theme(self):
        self.current_theme = Theme.DARK if self.current_theme == Theme.LIGHT else Theme.LIGHT  # Toggle the theme
        self.theme_button.configure(text=self._get_theme_button_text())  # Update the theme button text
        self.apply_theme()  # Apply the new theme

    def apply_theme(self):
        colors = self.current_theme.value  # Get the colors for the current theme

        for widget, config in self._get_theme_configs(colors).items():
            widget.configure(**config)  # Apply the theme colors to each widget

        self._update_button_colors(colors)  # Update the colors of the buttons

    def _get_theme_configs(self, colors: Dict) -> Dict:
        return {
            self.main_container: {'bg': colors['background']},
            self.title_label: {'bg': colors['background'], 'fg': colors['button_fg']},
            self.score_frame: {'bg': colors['background']},
            **{label: {'bg': colors['background'], 'fg': colors['button_fg']}
               for label in self.score_labels.values()},
            self.game_frame: {'bg': colors['border']},
            self.control_frame: {'bg': colors['background']},
            self.theme_button: {'bg': colors['toggle_bg'], 'fg': colors['toggle_fg'],
                                'activebackground': colors['button_active']},
            self.reset_button: {'bg': colors['toggle_bg'], 'fg': colors['toggle_fg'],
                                'activebackground': colors['button_active']},
            self.back_button: {'bg': colors['toggle_bg'], 'fg': colors['toggle_fg'],
                               'activebackground': colors['button_active']},
            self.turn_indicator: {'bg': colors['background'], 'fg': colors['button_fg']}
        }  # Return a dictionary of theme configurations for each widget

    def _update_button_colors(self, colors: Dict):
        for i in range(self.board.size):
            for j in range(self.board.size):
                button = self.buttons[i][j]
                button.configure(
                    bg=colors['button_bg'],
                    fg=colors['button_fg'],
                    activebackground=colors['button_active']
                )  # Update the button colors based on the theme
                if button['text'] == 'X':
                    button.configure(fg=colors['x_color'])  # Set the color for X
                elif button['text'] == 'O':
                    button.configure(fg=colors['o_color'])  # Set the color for O

    def _on_enter(self, event):
        if event.widget['text'] == '':
            event.widget.configure(bg=self.current_theme.value['hover'])  # Change the button color on hover

    def _on_leave(self, event):
        if event.widget['text'] == '':
            event.widget.configure(bg=self.current_theme.value['button_bg'])  # Revert the button color on hover leave

    def update_scores(self, winner: Player):
        self.scores[winner] += 1  # Increment the score for the winner
        self.score_labels[winner].configure(
            text=f"{'Player' if winner == Player.X else 'AI/Player'} {winner.value}: {self.scores[winner]}"
        )  # Update the score label for the winner

    def reset_game(self):
        self.scores = {Player.X: 0, Player.O: 0}  # Reset the scores
        for player in [Player.X, Player.O]:
            self.score_labels[player].configure(
                text=f"{'Player' if player == Player.X else 'AI/Player'} {player.value}: 0"
            )  # Reset the score labels
        self.reset_board()  # Reset the game board

    def reset_board(self):
        self.board.clear()  # Clear the game board
        self.current_player = Player.X  # Set the starting player to X
        self.turn_indicator.configure(text=self._get_turn_text())  # Update the turn indicator
        for row in self.buttons:
            for button in row:
                button.configure(text='', fg=self.current_theme.value['button_fg'])  # Clear the button texts

    def _handle_move(self, row: int, col: int):
        raise NotImplementedError("Subclasses must implement _handle_move")  # Raise an error if not implemented in subclasses
  