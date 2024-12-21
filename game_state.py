# استيراد المكتبات اللازمة للتعامل مع الأنواع والكلاسات المطلوبة
from typing import List, Tuple
from player import Player
from move import Move

class GameState:
    # دالة البناء: تأخذ حالة اللوحة الحالية واللاعب الحالي
    # grid: مصفوفة تمثل حالة اللوحة
    # player: اللاعب الحالي (X أو O)
    def __init__(self, grid: List[List[Player]], player: Player):
        self.grid = grid        # تخزين حالة اللوحة
        self.player = player    # تخزين اللاعب الحالي
        self.size = len(grid)   # تخزين حجم اللوحة

    # دالة لتوليد جميع الحركات الممكنة من الحالة الحالية
    # تُستخدم في خوارزمية A* للبحث عن أفضل حركة
    def get_successors(self) -> List[Tuple['GameState', Move]]:
        successors = []
        # البحث في كل خلية في اللوحة
        for i in range(self.size):
            for j in range(self.size):
                # إذا كانت الخلية فارغة، يمكن اللعب فيها
                if self.grid[i][j] == Player.EMPTY:
                    # نسخ اللوحة الحالية لإنشاء حالة جديدة
                    new_grid = [row.copy() for row in self.grid]
                    # وضع علامة اللاعب في الموقع المختار
                    new_grid[i][j] = self.player
                    # تبديل اللاعب للحركة التالية
                    next_player = Player.X if self.player == Player.O else Player.O
                    # إضافة الحالة الجديدة والحركة إلى قائمة الخيارات
                    successors.append(
                        (GameState(new_grid, next_player), Move(i, j))
                    )
        return successors

    # التحقق من انتهاء اللعبة
    # تُستخدم لمعرفة ما إذا وصلنا لنهاية المسار في شجرة البحث
    def is_terminal(self) -> bool:
        # اللعبة تنتهي إذا فاز أحد اللاعبين أو امتلأت اللوحة
        return self.check_winner(Player.X) or self.check_winner(Player.O) or \
               all(cell != Player.EMPTY for row in self.grid for cell in row)

    # التحقق من وجود فائز
    # تُستخدم للتحقق من فوز لاعب معين
    def check_winner(self, player: Player) -> bool:
        # فحص الصفوف والأعمدة
        for i in range(self.size):
            if all(self.grid[i][j] == player for j in range(self.size)) or \
               all(self.grid[j][i] == player for j in range(self.size)):
                return True

        # فحص القطرين
        if all(self.grid[i][i] == player for i in range(self.size)) or \
           all(self.grid[i][self.size - 1 - i] == player for i in range(self.size)):
            return True
        return False

    # تقييم الحالة الحالية
    # تُستخدم في خوارزمية A* لتقييم مدى جودة الحالة
    def evaluate(self) -> float:
        # إذا فاز O (الكمبيوتر)، نُرجع قيمة موجبة
        if self.check_winner(Player.O):
            return 1.0
        # إذا فاز X (اللاعب)، نُرجع قيمة سالبة
        elif self.check_winner(Player.X):
            return -1.0
        # إذا لم يفز أحد، نُرجع صفر
        return 0.0