# استيراد المكتبات اللازمة للواجهة الرسومية وإدارة اللعبة
import tkinter as tk
from tkinter import messagebox
from base_game_gui import BaseGameGUI
from player import Player
from move import Move
from theme import Theme

class TwoPlayerGame(BaseGameGUI):
    # تهيئة اللعبة لاعبين
    def __init__(self, window: tk.Tk, theme: Theme):
        # استدعاء المُنشئ الأساسي للواجهة الرسومية
        super().__init__(window, theme)
        # إنشاء الواجهة الرسومية مع عنوان مناسب
        self.create_base_gui("Tic Tac Toe - 2 Players")
        # متغير للرجوع للقائمة الرئيسية
        self.on_back_to_menu = None

    # معالجة النقر على أحد المربعات في اللوحة
    def _handle_move(self, row: int, col: int):
        # التحقق من أن المربع فارغ
        if self.board.grid[row][col] == Player.EMPTY:
            # إنشاء حركة جديدة وتنفيذها
            move = Move(row, col)
            self._make_move(move)

    # تنفيذ حركة لاعب على اللوحة
    def _make_move(self, move: Move):
        # محاولة تنفيذ الحركة على اللوحة
        if self.board.make_move(move, self.current_player):
            # الحصول على الزر المقابل للحركة
            button = self.buttons[move.row][move.col]
            # تحديث شكل الزر بعلامة اللاعب ولونه
            button.configure(
                text=self.current_player.value,
                fg=self.current_theme.value['x_color' if self.current_player == Player.X else 'o_color']
            )

            # إذا لم تنته اللعبة، تبديل دور اللاعب
            if not self._check_game_end():
                self.current_player = Player.O if self.current_player == Player.X else Player.X
                self.turn_indicator.configure(text=self._get_turn_text())

    # التحقق من انتهاء اللعبة
    def _check_game_end(self) -> bool:
        # التحقق من وجود فائز
        if self.board.check_winner(self.current_player):
            # تحديث النتائج وإظهار رسالة الفوز
            self.update_scores(self.current_player)
            messagebox.showinfo("Game Over", f"Player {self.current_player.value} wins!")
            self.reset_board()
            return True

        # التحقق من تعادل (امتلاء اللوحة)
        if self.board.is_full():
            messagebox.showinfo("Game Over", "It's a tie!")
            self.reset_board()
            return True

        return False
