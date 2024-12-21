import tkinter as tk
from typing import Callable
from theme import Theme
from ai_game import AIGame
from two_player_game import TwoPlayerGame
import webbrowser

# فئة القائمة الرئيسية للعبة
class GameMenu:
    # دالة البداية - تهيئة النافذة الرئيسية
    def __init__(self, window: tk.Tk):
        self.window = window  # تخزين النافذة الرئيسية
        self.window.title("Tic Tac Toe")  # تعيين عنوان النافذة
        self.window.resizable(False, False)  # تعطيل إمكانية تغيير حجم النافذة
        self.current_theme = Theme.DARK  # تعيين النمط المظلم كنمط افتراضي
        self._create_menu()  # إنشاء واجهة القائمة
        self._center_window()  # توسيط النافذة على الشاشة

    # دالة لتوسيط النافذة على الشاشة
    def _center_window(self):
        self.window.update_idletasks()  # تحديث مهام النافذة للحصول على الأبعاد الصحيحة
        width = self.window.winfo_width()  # الحصول على عرض النافذة
        height = self.window.winfo_height()  # الحصول على ارتفاع النافذة
        x = (self.window.winfo_screenwidth() - width) // 2  # حساب الموقع الأفقي لتوسيط النافذة
        y = (self.window.winfo_screenheight() - height) // 2  # حساب الموقع الرأسي لتوسيط النافذة
        self.window.geometry(f'+{x}+{y}')  # تعيين موقع النافذة

    # دالة إنشاء القائمة الرئيسية
    def _create_menu(self):
        # إنشاء إطار القائمة مع التنسيق واللون الخلفي
        self.menu_frame = tk.Frame(
            self.window,
            padx=20,
            pady=20,
            bg=self.current_theme.value['background']
        )
        self.menu_frame.pack(expand=True, fill='both')

        # إنشاء عنوان اللعبة
        self.title = tk.Label(
            self.menu_frame,
            text="Tic Tac Toe",
            font=('Helvetica', 24, 'bold'),
            pady=10,
            bg=self.current_theme.value['background'],
            fg=self.current_theme.value['button_fg']
        )
        self.title.pack()

        # إنشاء أزرار وضع اللعب
        self._create_menu_button("Play vs AI", self._start_ai_game)  # زر اللعب ضد الكمبيوتر
        self._create_menu_button("Play vs Friend", self._start_two_player_game)  # زر اللعب ضد صديق
        self._create_menu_button("Exit", self.window.quit)  # زر الخروج من اللعبة

        # زر تغيير النمط (مظلم/مضيء)
        self.theme_button = self._create_menu_button(
            "🌙 Dark Mode" if self.current_theme == Theme.LIGHT else "☀️ Light Mode",
            self._toggle_theme
        )

        # إطار لأزرار التواصل الاجتماعي في أسفل القائمة
        self.social_frame = tk.Frame(
            self.menu_frame,
            bg=self.current_theme.value['background']  # تعيين لون خلفية الإطار حسب النمط الحالي
        )
        self.social_frame.pack(pady=10)  # وضع الإطار في النافذة مع هامش علوي وسفلي

        # إنشاء زر GitHub مع التنسيق المناسب
        self.github_button = tk.Button(
            self.social_frame,  # وضع الزر في إطار وسائل التواصل
            text="GitHub 🔗",  # نص الزر مع أيقونة الرابط
            command=self._open_github,  # تعيين الدالة التي ستنفذ عند الضغط
            font=('Helvetica', 12),  # نوع وحجم الخط
            bg=self.current_theme.value['toggle_bg'],  # لون خلفية الزر
            fg=self.current_theme.value['toggle_fg'],  # لون النص
            activebackground=self.current_theme.value['button_active'],  # لون الخلفية عند الضغط
            activeforeground=self.current_theme.value['toggle_fg'],  # لون النص عند الضغط
            padx=15,  # الهامش الأفقي
            pady=5    # الهامش الرأسي
        )
        self.github_button.pack(side=tk.LEFT)  # وضع الزر في يسار الإطار

        # إنشاء زر LinkedIn بنفس تنسيق زر GitHub
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
        )
        self.linkedin_button.pack(side=tk.LEFT)  # وضع الزر بجانب زر GitHub

    def _create_menu_button(self, text: str, command: Callable) -> tk.Button:
        # دالة مساعدة لإنشاء أزرار القائمة بتنسيق موحد
        button = tk.Button(
            self.menu_frame,  # وضع الزر في إطار القائمة الرئيسية
            text=text,  # النص المعروض على الزر
            command=command,  # الدالة التي ستنفذ عند الضغط
            font=('Helvetica', 12),  # تنسيق الخط
            bg=self.current_theme.value['toggle_bg'],  # لون خلفية الزر
            fg=self.current_theme.value['toggle_fg'],  # لون النص
            activebackground=self.current_theme.value['button_active'],  # لون الخلفية عند الضغط
            activeforeground=self.current_theme.value['toggle_fg'],  # لون النص عند الضغط
            padx=15,  # الهامش الأفقي
            pady=5    # الهامش الرأسي
        )
        button.pack(pady=10)  # وضع الزر في النافذة مع هامش
        return button  # إرجاع الزر المنشأ

    def _toggle_theme(self):
        # تبديل النمط بين المظلم والمضيء
        self.current_theme = Theme.DARK if self.current_theme == Theme.LIGHT else Theme.LIGHT
        self._update_menu_theme()  # تحديث مظهر القائمة

    def _open_github(self):
        # فتح صفحة GitHub في المتصفح
        webbrowser.open('https://github.com/aliabdelmoaty')

    def _open_linkedin(self):
        # فتح صفحة LinkedIn في المتصفح
        webbrowser.open('https://www.linkedin.com/in/ali-abdelmoaty10')

    def _update_menu_theme(self):
        # الحصول على ألوان النمط الحالي
        colors = self.current_theme.value
        
        # تحديث ألوان الإطار الرئيسي والعنوان
        self.menu_frame.configure(bg=colors['background'])
        self.title.configure(
            bg=colors['background'],
            fg=colors['button_fg']
        )
        
        # تحديث تنسيق زر GitHub
        self.github_button.configure(
            font=('Helvetica', 12),
            bg=self.current_theme.value['toggle_bg'],
            fg=self.current_theme.value['toggle_fg'],
            activebackground=self.current_theme.value['button_active'],
            activeforeground=self.current_theme.value['toggle_fg'],
            padx=15,
            pady=5
        )
        
        # تحديث تنسيق زر LinkedIn
        self.linkedin_button.configure(
            font=('Helvetica', 12),
            bg=self.current_theme.value['toggle_bg'],
            fg=self.current_theme.value['toggle_fg'],
            activebackground=self.current_theme.value['button_active'],
            activeforeground=self.current_theme.value['toggle_fg'],
            padx=15,
            pady=5
        )
        
        # تحديث نص وألوان زر تغيير النمط
        self.theme_button.configure(
            text="🌙 Dark Mode" if self.current_theme == Theme.LIGHT else "☀️ Light Mode",
            bg=colors['toggle_bg'],
            fg=colors['toggle_fg']
        )

        # تحديث ألوان جميع الأزرار في القائمة
        for widget in self.menu_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(
                    bg=colors['toggle_bg'],
                    fg=colors['toggle_fg'],
                    activebackground=colors['button_active'],
                    activeforeground=colors['toggle_fg']
                )

    # دالة بدء اللعب ضد الكمبيوتر
    def _start_ai_game(self):
        self.menu_frame.destroy()  # إزالة القائمة الرئيسية
        game = AIGame(self.window, self.current_theme)  # إنشاء لعبة جديدة ضد الكمبيوتر
        game.on_back_to_menu = lambda: GameMenu(self.window)  # تعيين دالة الرجوع للقائمة

    # دالة بدء اللعب ضد صديق
    def _start_two_player_game(self):
        self.menu_frame.destroy()  # إزالة القائمة الرئيسية
        game = TwoPlayerGame(self.window, self.current_theme)  # إنشاء لعبة جديدة للاعبين
        game.on_back_to_menu = lambda: GameMenu(self.window)  # تعيين دالة الرجوع للقائمة

