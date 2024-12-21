# استيراد المكتبات والكلاسات اللازمة
from typing import List
from player import Player
from move import Move

class Board:
    # تهيئة لوحة اللعب بحجم محدد (الحجم الافتراضي 3×3)
    def __init__(self, size: int = 3):
        self.size = size
        self.clear()

    # دالة لتنفيذ حركة اللاعب على اللوحة
    # تقوم بوضع رمز اللاعب في المكان المحدد إذا كان فارغاً
    def make_move(self, move: Move, player: Player) -> bool:
        if self.grid[move.row][move.col] == Player.EMPTY:
            self.grid[move.row][move.col] = player
            return True
        return False

    # التحقق مما إذا كانت اللوحة ممتلئة بالكامل
    def is_full(self) -> bool:
        return all(cell != Player.EMPTY for row in self.grid for cell in row)

    # تنظيف اللوحة وإعادتها إلى الحالة الأولية
    # تقوم بإنشاء مصفوفة ثنائية الأبعاد وملئها بقيم فارغة
    def clear(self):
        self.grid = [[Player.EMPTY for _ in range(self.size)] for _ in range(self.size)]

    # التحقق من وجود فائز
    # تفحص جميع الصفوف والأعمدة والخطوط القطرية
    def check_winner(self, player: Player) -> bool:
        # فحص الصفوف والأعمدة
        for i in range(self.size):
            # فحص الصف الأفقي
            if all(self.grid[i][j] == player for j in range(self.size)) or \
                    all(self.grid[j][i] == player for j in range(self.size)):
                return True

        # فحص القطرين الرئيسي والثانوي
        if all(self.grid[i][i] == player for i in range(self.size)) or \
                all(self.grid[i][self.size - 1 - i] == player for i in range(self.size)):
            return True
        return False