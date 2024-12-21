import tkinter as tk
from typing import Callable
from theme import Theme
from ai_game import AIGame
from two_player_game import TwoPlayerGame
import webbrowser

class GameMenu:
    def __init__(self, window: tk.Tk):
        self.window = window  # Store the main window
        self.window.title("Tic Tac Toe")  # Set the window title
        self.window.resizable(False, False)  # Disable window resizing
        self.current_theme = Theme.DARK  # Set the initial theme to dark
        self._create_menu()  # Create the menu interface
        self._center_window()  # Center the window on the screen

    def _center_window(self):
        self.window.update_idletasks()  # Update window tasks to get correct dimensions
        width = self.window.winfo_width()  # Get the window width
        height = self.window.winfo_height()  # Get the window height
        x = (self.window.winfo_screenwidth() - width) // 2  # Calculate x position to center the window
        y = (self.window.winfo_screenheight() - height) // 2  # Calculate y position to center the window
        self.window.geometry(f'+{x}+{y}')  # Set the window position

    def _create_menu(self):
        self.menu_frame = tk.Frame(
            self.window,
            padx=20,
            pady=20,
            bg=self.current_theme.value['background']
        )  # Create a frame for the menu with padding and background color
        self.menu_frame.pack(expand=True, fill='both')  # Pack the frame to expand and fill the window

        # Title
        self.title = tk.Label(
            self.menu_frame,
            text="Tic Tac Toe",
            font=('Helvetica', 24, 'bold'),
            pady=10,
            bg=self.current_theme.value['background'],
            fg=self.current_theme.value['button_fg']
        )  # Create a label for the title with specified font, padding, and colors
        self.title.pack()  # Pack the title label

        # Game mode buttons
        self._create_menu_button("Play vs AI", self._start_ai_game)  # Create a button to start AI game
        self._create_menu_button("Play vs Friend", self._start_two_player_game)  # Create a button to start two-player game
        self._create_menu_button("Exit", self.window.quit)  # Create a button to exit the game
        # Theme toggle
        self.theme_button = self._create_menu_button(
            "🌙 Dark Mode" if self.current_theme == Theme.LIGHT else "☀️ Light Mode",
            self._toggle_theme
        )  # Create a button to toggle the theme with appropriate text
        self.social_frame = tk.Frame(
        self.menu_frame,
        bg=self.current_theme.value['background']
    )
        self.social_frame.pack(pady=10)

    # GitHub button
        self.github_button = tk.Button(
            self.social_frame,
            text="GitHub 🔗",
            command=self._open_github,
            font=('Helvetica', 12),
            bg=self.current_theme.value['toggle_bg'],
            fg=self.current_theme.value['toggle_fg'],
            activebackground=self.current_theme.value['button_active'],
            activeforeground=self.current_theme.value['toggle_fg'],
            padx=15,
            pady=5
        )
        self.github_button.pack(side=tk.LEFT)

        # LinkedIn button
        self.linkedin_button = tk.Button(
            self.social_frame,
            text="LinkedIn 🔗",
            command=self._open_linkedin,
            font=('Helvetica', 12),
            bg=self.current_theme.value['toggle_bg'],
            fg=self.current_theme.value['toggle_fg'],
            activebackground=self.current_theme.value['button_active'],
            activeforeground=self.current_theme.value['toggle_fg'],
            padx=15,
            pady=5
        )  # Create a button with specified text, command, font, colors, and padding
        self.linkedin_button.pack(side=tk.LEFT)

    def _create_menu_button(self, text: str, command: Callable) -> tk.Button:
        button = tk.Button(
            self.menu_frame,
            text=text,
            command=command,
            font=('Helvetica', 12),
            bg=self.current_theme.value['toggle_bg'],
            fg=self.current_theme.value['toggle_fg'],
            activebackground=self.current_theme.value['button_active'],
            activeforeground=self.current_theme.value['toggle_fg'],
            padx=15,
            pady=5
        )  # Create a button with specified text, command, font, colors, and padding
        button.pack(pady=10)  # Pack the button with padding
        return button  # Return the created button
    
    def _toggle_theme(self):
        self.current_theme = Theme.DARK if self.current_theme == Theme.LIGHT else Theme.LIGHT  # Toggle the theme
        self._update_menu_theme()  # Update the menu theme
    def _open_github(self):
    # Replace with your GitHub profile URL
        webbrowser.open('https://github.com/aliabdelmoaty')

    def _open_linkedin(self):
        webbrowser.open('https://www.linkedin.com/in/ali-abdelmoaty10')
    def _update_menu_theme(self):
        colors = self.current_theme.value  # Get the colors for the current theme
        self.menu_frame.configure(bg=colors['background'])  # Update the background color of the menu frame
        self.title.configure(
            bg=colors['background'],
            fg=colors['button_fg']
        )  # Update the background and foreground colors of the title
        self.github_button.configure(
            font=('Helvetica', 12),
            bg=self.current_theme.value['toggle_bg'],
            fg=self.current_theme.value['toggle_fg'],
            activebackground=self.current_theme.value['button_active'],
            activeforeground=self.current_theme.value['toggle_fg'],
            padx=15,
            pady=5
    )
        self.linkedin_button.configure(
            font=('Helvetica', 12),
            bg=self.current_theme.value['toggle_bg'],
            fg=self.current_theme.value['toggle_fg'],
            activebackground=self.current_theme.value['button_active'],
            activeforeground=self.current_theme.value['toggle_fg'],
            padx=15,
            pady=5
    )
        self.theme_button.configure(
            text="🌙 Dark Mode" if self.current_theme == Theme.LIGHT else "☀️ Light Mode",
            bg=colors['toggle_bg'],
            fg=colors['toggle_fg']
        )  # Update the text and colors of the theme button

        for widget in self.menu_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(
                    bg=colors['toggle_bg'],
                    fg=colors['toggle_fg'],
                    activebackground=colors['button_active'],
                    activeforeground=colors['toggle_fg']
                )  # Update the colors of all buttons in the menu frame

    def _start_ai_game(self):
        self.menu_frame.destroy()
        game = AIGame(self.window, self.current_theme)
        game.on_back_to_menu = lambda: GameMenu(self.window)

    def _start_two_player_game(self):
        self.menu_frame.destroy()
        game = TwoPlayerGame(self.window, self.current_theme)
        game.on_back_to_menu = lambda: GameMenu(self.window)
 
