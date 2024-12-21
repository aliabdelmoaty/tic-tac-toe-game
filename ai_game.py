# استيراد المكتبات اللازمة للعبة
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

# تعريف فئة Node لتمثيل حالة في شجرة البحث
@dataclass
class Node:
    # تخزين الحالة الحالية للعبة
    state: GameState  
    # تخزين الحركة التي أدت إلى هذه الحالة
    move: Move  
    # تخزين تكلفة المسار من البداية إلى هذه الحالة
    g_cost: float  
    # تخزين التكلفة التقديرية المتوقعة للوصول للهدف
    h_cost: float  
    # تخزين مرجع للعقدة الأب (الحالة السابقة)
    parent: Optional['Node'] = None  

    # حساب التكلفة الكلية (f = g + h)
    def f_cost(self) -> float:
        # حساب التكلفة الكلية بجمع تكلفة المسار والتكلفة التقديرية
        return self.g_cost + self.h_cost

    # تعريف عملية المقارنة بين العقد حسب التكلفة الكلية
    def __lt__(self, other):
        # تعريف كيفية مقارنة العقد مع بعضها البعض باستخدام التكلفة الكلية
        return self.f_cost() < other.f_cost()

# فئة اللعب ضد الذكاء الاصطناعي
class AIGame(BaseGameGUI):
    def __init__(self, window: tk.Tk, theme: Theme):
        # تهيئة الفئة الأساسية للواجهة الرسومية
        super().__init__(window, theme)
        # إنشاء الواجهة الرسومية الأساسية للعبة
        self.create_base_gui("Tic Tac Toe vs AI")
        # تهيئة متغير لتخزين دالة الرجوع للقائمة الرئيسية
        self.on_back_to_menu = None

    # معالجة حركة اللاعب
    def _handle_move(self, row: int, col: int):
        # التحقق من أن المربع فارغ وأنه دور اللاعب X
        if self.board.grid[row][col] == Player.EMPTY and self.current_player == Player.X:
            move = Move(row, col)  # إنشاء حركة جديدة
            self._make_player_move(move)  # تنفيذ حركة اللاعب
            # التحقق من انتهاء اللعبة بعد حركة اللاعب
            if not self._check_game_end(Player.X):
                self.current_player = Player.O  # تغيير الدور للكمبيوتر
                self.turn_indicator.configure(text=self._get_turn_text())  # تحديث مؤشر الدور
                self.window.after(500, self._make_ai_move)  # تنفيذ حركة الكمبيوتر بعد نصف ثانية

    # تنفيذ حركة اللاعب على اللوحة
    def _make_player_move(self, move: Move):
        if self.board.make_move(move, Player.X):  # إذا كانت الحركة صحيحة
            button = self.buttons[move.row][move.col]  # الحصول على الزر المناسب
            button.configure(  # تحديث شكل الزر
                text=Player.X.value,
                fg=self.current_theme.value['x_color']
            )

    # تنفيذ حركة الكمبيوتر
    def _make_ai_move(self):
        move = self._get_ai_move()  # الحصول على أفضل حركة من الخوارزمية
        if move:  # إذا وجدت حركة ممكنة
            if self.board.make_move(move, Player.O):  # تنفيذ الحركة
                button = self.buttons[move.row][move.col]  # تحديث الزر
                button.configure(
                    text=Player.O.value,
                    fg=self.current_theme.value['o_color']
                )
                # التحقق من انتهاء اللعبة والتغيير للاعب التالي
                if not self._check_game_end(Player.O):
                    self.current_player = Player.X
                    self.turn_indicator.configure(text=self._get_turn_text())

    # الحصول على أفضل حركة للكمبيوتر
    def _get_ai_move(self) -> Optional[Move]:
        # معالجة الحركة الأولى بشكل خاص
        if all(cell == Player.EMPTY for row in self.board.grid for cell in row):
            if self.board.grid[1][1] == Player.EMPTY:
                return Move(1, 1)  # اختيار المركز إذا كان متاحاً
            return Move(0, 0)  # اختيار الزاوية إذا كان المركز مشغولاً

        # إنشاء حالة أولية وتنفيذ خوارزمية A*
        initial_state = GameState([row.copy() for row in self.board.grid], Player.O)
        return self._a_star_search(initial_state)

    # حساب قيمة تقديرية لحالة اللعبة
    def _calculate_heuristic(self, state: GameState) -> float:
        # تهيئة متغير لتخزين النتيجة التقديرية
        score = 0.0
        
        # فحص الصفوف والأعمدة والأقطار
        for i in range(state.size):
            # استخراج الصف الحالي من اللوحة
            row = [state.grid[i][j] for j in range(state.size)]  # فحص الصف
            # إضافة تقييم الصف للنتيجة الكلية
            score += self._evaluate_line(row)
            
            # استخراج العمود الحالي من اللوحة
            col = [state.grid[j][i] for j in range(state.size)]  # فحص العمود
            # إضافة تقييم العمود للنتيجة الكلية
            score += self._evaluate_line(col)

        # فحص الأقطار
        # استخراج القطر الرئيسي
        diag1 = [state.grid[i][i] for i in range(state.size)]
        # استخراج القطر الثانوي
        diag2 = [state.grid[i][state.size-1-i] for i in range(state.size)]
        # إضافة تقييم القطرين للنتيجة الكلية
        score += self._evaluate_line(diag1)
        score += self._evaluate_line(diag2)

        return score

    # تقييم خط معين (صف، عمود، أو قطر)
    def _evaluate_line(self, line: List[Player]) -> float:
        o_count = line.count(Player.O)
        x_count = line.count(Player.X)
        empty_count = line.count(Player.EMPTY)

        if o_count == 3:
            return 100.0  # فوز للكمبيوتر
        elif x_count == 3:
            return -100.0  # فوز للاعب
        elif o_count == 2 and empty_count == 1:
            return 10.0  # فرصة فوز للكمبيوتر
        elif x_count == 2 and empty_count == 1:
            return -10.0  # فرصة فوز للاعب
        elif o_count == 1 and empty_count == 2:
            return 1.0  # أفضلية مبكرة للكمبيوتر
        elif x_count == 1 and empty_count == 2:
            return -1.0  # أفضلية مبكرة للاعب
        return 0.0

    # خوارزمية البحث A* للعثور على أفضل حركة
    def _a_star_search(self, initial_state: GameState) -> Optional[Move]:
        # إنشاء قائمة الحالات المفتوحة التي سيتم استكشافها
        open_set: List[Node] = []
        # إنشاء مجموعة الحالات المغلقة التي تم استكشافها
        closed_set: Set[str] = set()
        
        # إنشاء العقدة الأولية مع الحالة الابتدائية
        start_node = Node(
            state=initial_state,
            move=None,
            g_cost=0,
            h_cost=self._calculate_heuristic(initial_state)
        )
        
        # إضافة العقدة الأولية إلى قائمة الحالات المفتوحة
        heapq.heappush(open_set, start_node)
        
        while open_set:
            current = heapq.heappop(open_set)
            
            # تخطي إذا تم استكشاف هذه الحالة مسبقاً
            state_hash = str([str(row) for row in current.state.grid])
            if state_hash in closed_set:
                continue
                
            closed_set.add(state_hash)
            
            # التحقق مما إذا كانت هذه حالة فوز
            if current.state.check_winner(Player.O):
                # التراجع للحصول على الحركة الأولية
                while current.parent and current.parent.parent:
                    current = current.parent
                return current.move
            
            # توليد الخلفاء
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
        
        # إذا لم يتم العثور على مسار فوز، إرجاع الحركة ذات القيمة التقديرية الأفضل
        best_move = None
        best_value = float('-inf')
        
        for next_state, move in initial_state.get_successors():
            value = self._calculate_heuristic(next_state)
            if value > best_value:
                best_value = value
                best_move = move
                
        return best_move

    # التحقق من انتهاء اللعبة
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