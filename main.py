import tkinter as tk
from game_menu import GameMenu

def main():
    window = tk.Tk()
    game_menu = GameMenu(window)
    window.mainloop()

if __name__ == "__main__":
    main()