from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, 
    QLabel, QApplication, QSizePolicy, QSizeGrip, QMenu
)
from PyQt6.QtGui import QCursor
from core.layouts import LANGUAGE_REGISTRY

class DualKeyButton(QPushButton):
    def __init__(self, normal_text: str, shift_text: str, evdev_code: int, key_type: str):
        super().__init__()
        self.normal_text = normal_text
        self.shift_text = shift_text
        self.evdev_code = evdev_code
        self.key_type = key_type
        self.current_display_char = normal_text
        
        self.setProperty("class", "keyBtn")
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setMinimumHeight(28)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(0)

        self.is_dual = (key_type == "char" and shift_text != normal_text and not (len(normal_text) == 1 and normal_text.isalpha()))

        if self.is_dual:
            self.top_label = QLabel(shift_text)
            self.top_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.top_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            
            self.bottom_label = QLabel(normal_text)
            self.bottom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.bottom_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

            self.layout.addWidget(self.top_label)
            self.layout.addWidget(self.bottom_label)
        else:
            self.single_label = QLabel(normal_text)
            self.single_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.single_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            self.layout.addWidget(self.single_label)

    def update_visuals(self, is_shift: bool, is_caps: bool, is_dark: bool):
        dim_color = "#6c7086" if is_dark else "#94a3b8"
        bright_color = "#cdd6f4" if is_dark else "#1e293b"
        accent_color = "#89b4fa" if is_dark else "#2563eb"

        if self.is_dual:
            if is_shift:
                self.current_display_char = self.shift_text
                self.top_label.setStyleSheet(f"color: {accent_color}; font-size: 11px; font-weight: 900; border: none;")
                self.bottom_label.setStyleSheet(f"color: {dim_color}; font-size: 10px; font-weight: normal; border: none;")
            else:
                self.current_display_char = self.normal_text
                self.top_label.setStyleSheet(f"color: {dim_color}; font-size: 10px; font-weight: normal; border: none;")
                self.bottom_label.setStyleSheet(f"color: {bright_color}; font-size: 13px; font-weight: bold; border: none;")
        else:
            if self.key_type == "char" and self.normal_text.isalpha():
                is_upper = is_shift ^ is_caps
                self.current_display_char = self.shift_text if is_upper else self.normal_text
                self.single_label.setText(self.current_display_char)
                self.single_label.setStyleSheet(f"color: {bright_color}; font-size: 13px; font-weight: bold; border: none;")
            else:
                self.current_display_char = self.normal_text
                self.single_label.setStyleSheet(f"color: {bright_color}; font-size: 12px; font-weight: bold; border: none;")

class DraggableHeader(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self._drag_pos = None
        self.setCursor(QCursor(Qt.CursorShape.SizeAllCursor))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.parent_window.pos()
            self.parent_window.user_has_manually_moved = True
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.globalPosition().toPoint() - self._drag_pos
            screen = QApplication.primaryScreen().geometry()
            x = max(0, min(new_pos.x(), screen.width() - self.parent_window.width()))
            y = max(0, min(new_pos.y(), screen.height() - self.parent_window.height()))
            self.parent_window.move(x, y)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

class KeyboardView(QWidget):
    charTriggered = pyqtSignal(str)
    specialKeyTriggered = pyqtSignal(int)
    closeRequested = pyqtSignal()
    themeToggled = pyqtSignal()
    settingsRequested = pyqtSignal()
    languageChanged = pyqtSignal(str)

    def __init__(self, theme_manager, current_lang="en"):
        super().__init__()
        self.theme_manager = theme_manager
        self.current_lang = current_lang
        self.is_shift = False
        self.is_caps = False
        self.key_widgets = []
        self.shift_buttons = []
        self.caps_button = None
        self.user_has_manually_moved = False
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.ToolTip |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowDoesNotAcceptFocus |
            Qt.WindowType.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysStackOnTop, True)
        self.setAttribute(Qt.WidgetAttribute.WA_X11DoNotAcceptFocus, True)

        self.setMinimumSize(560, 210)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(6, 6, 6, 6)
        self.main_layout.setSpacing(0)

        self.container = QWidget()
        self.container.setObjectName("keyboardContainer")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(10, 8, 10, 8)
        self.container_layout.setSpacing(5)

        # Header Bar
        self.header = DraggableHeader(self)
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(4, 2, 4, 2)
        header_layout.setSpacing(6)

        self.title_label = QLabel(f"⠿ Float Keyboard — {LANGUAGE_REGISTRY[self.current_lang]['name']}")
        self.title_label.setObjectName("headerTitle")
        self.title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        # Direct Language Menu Button
        self.lang_btn = QPushButton(f"{LANGUAGE_REGISTRY[self.current_lang]['badge']} ▼")
        self.lang_btn.setObjectName("themeBtn")
        self.lang_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lang_btn.setFixedHeight(24)
        self.lang_btn.clicked.connect(self.show_language_menu)

        # Scale -
        self.zoom_out_btn = QPushButton("－")
        self.zoom_out_btn.setObjectName("themeBtn")
        self.zoom_out_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.zoom_out_btn.setFixedSize(24, 24)
        self.zoom_out_btn.clicked.connect(self.scale_down)

        # Scale +
        self.zoom_in_btn = QPushButton("＋")
        self.zoom_in_btn.setObjectName("themeBtn")
        self.zoom_in_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.zoom_in_btn.setFixedSize(24, 24)
        self.zoom_in_btn.clicked.connect(self.scale_up)

        # Theme Switcher
        self.theme_btn = QPushButton("☾" if self.theme_manager.is_dark() else "☀")
        self.theme_btn.setObjectName("themeBtn")
        self.theme_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.theme_btn.setFixedSize(26, 24)
        self.theme_btn.clicked.connect(self._handle_theme_toggle)

        # Settings Button
        self.settings_btn = QPushButton("⚙")
        self.settings_btn.setObjectName("themeBtn")
        self.settings_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.settings_btn.setFixedSize(26, 24)
        self.settings_btn.clicked.connect(self.settingsRequested.emit)

        # Close Button
        close_btn = QPushButton("✕")
        close_btn.setObjectName("closeBtn")
        close_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        close_btn.setFixedSize(22, 22)
        close_btn.clicked.connect(self.closeRequested.emit)

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.lang_btn)
        header_layout.addWidget(self.zoom_out_btn)
        header_layout.addWidget(self.zoom_in_btn)
        header_layout.addWidget(self.theme_btn)
        header_layout.addWidget(self.settings_btn)
        header_layout.addSpacing(4)
        header_layout.addWidget(close_btn)
        self.container_layout.addWidget(self.header)

        # Rows Layout Container
        self.rows_widget = QWidget()
        self.rows_layout = QVBoxLayout(self.rows_widget)
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.setSpacing(4)
        self.container_layout.addWidget(self.rows_widget, 1)

        # Bottom Corner Grip
        bottom_bar = QHBoxLayout()
        bottom_bar.setContentsMargins(0, 0, 0, 0)
        bottom_bar.addStretch()
        self.size_grip = QSizeGrip(self)
        self.size_grip.setFixedSize(16, 16)
        bottom_bar.addWidget(self.size_grip)
        self.container_layout.addLayout(bottom_bar)

        self.main_layout.addWidget(self.container)
        self.setLayout(self.main_layout)

        self.render_layout()
        self.resize(760, 275)
        self.refresh_styles()

    def show_language_menu(self):
        menu = QMenu(self)
        menu.setWindowFlags(
            Qt.WindowType.Popup |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        is_dark = self.theme_manager.is_dark()
        bg = "#1e1e2e" if is_dark else "#ffffff"
        fg = "#cdd6f4" if is_dark else "#1e293b"
        border = "#45475a" if is_dark else "#cbd5e1"

        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {bg};
                color: {fg};
                border: 1px solid {border};
                border-radius: 8px;
                padding: 4px;
                font-size: 12px;
                font-weight: bold;
            }}
            QMenu::item {{
                padding: 6px 14px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: #3b82f6;
                color: #ffffff;
            }}
        """)

        for code, data in LANGUAGE_REGISTRY.items():
            mark = "✔ " if code == self.current_lang else "    "
            action = menu.addAction(f"{mark}{data['badge']}  {data['name']}")
            action.triggered.connect(lambda checked, c=code, m=menu: self._select_language(c, m))

        pos = self.lang_btn.mapToGlobal(QPoint(0, self.lang_btn.height() + 4))
        menu.exec(pos)

    def _select_language(self, lang_code: str, menu: QMenu):
        menu.close()
        menu.deleteLater()
        self.set_language(lang_code)

    def set_language(self, lang_code: str):
        if lang_code in LANGUAGE_REGISTRY:
            self.current_lang = lang_code
            self.title_label.setText(f"⠿ Float Keyboard — {LANGUAGE_REGISTRY[self.current_lang]['name']}")
            self.lang_btn.setText(f"{LANGUAGE_REGISTRY[self.current_lang]['badge']} ▼")
            self.render_layout()
            self.refresh_styles()
            self.languageChanged.emit(lang_code)

    def render_layout(self):
        while self.rows_layout.count():
            item = self.rows_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget():
                        sub.widget().deleteLater()

        self.key_widgets.clear()
        self.shift_buttons.clear()
        self.caps_button = None

        layout_matrix = LANGUAGE_REGISTRY[self.current_lang]["layout"]

        for row in layout_matrix:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(4)
            for norm, shft, code, ktype, stretch in row:
                btn = DualKeyButton(norm, shft, code, ktype)
                if ktype == "shift":
                    self.shift_buttons.append(btn)
                    btn.clicked.connect(self.toggle_shift)
                elif ktype == "caps":
                    self.caps_button = btn
                    btn.clicked.connect(self.toggle_caps)
                elif ktype in ["backspace", "enter", "tab", "space"]:
                    btn.clicked.connect(lambda checked, c=code: self.specialKeyTriggered.emit(c))
                else:
                    self.key_widgets.append(btn)
                    btn.clicked.connect(lambda checked, b=btn: self.handle_char_click(b))

                row_layout.addWidget(btn, int(stretch * 10))
            self.rows_layout.addLayout(row_layout, 1)

    def scale_up(self):
        new_w = min(int(self.width() * 1.1), 1200)
        new_h = min(int(self.height() * 1.1), 450)
        self.resize(new_w, new_h)

    def scale_down(self):
        new_w = max(int(self.width() * 0.9), 540)
        new_h = max(int(self.height() * 0.9), 200)
        self.resize(new_w, new_h)

    def handle_char_click(self, btn: DualKeyButton):
        # Transmit the exact visible character to the engine
        self.charTriggered.emit(btn.current_display_char)
        # Shift stays permanently active until user clicks Shift again!

    def toggle_shift(self):
        self.is_shift = not self.is_shift
        self.refresh_key_labels()

    def toggle_caps(self):
        self.is_caps = not self.is_caps
        self.refresh_key_labels()

    def _handle_theme_toggle(self):
        self.theme_manager.toggle_theme()
        self.theme_btn.setText("☾" if self.theme_manager.is_dark() else "☀")
        self.refresh_styles()
        self.themeToggled.emit()

    def refresh_key_labels(self):
        is_dark = self.theme_manager.is_dark()
        for btn in self.key_widgets:
            btn.update_visuals(self.is_shift, self.is_caps, is_dark)

        # Shift Active Highlight
        shift_bg = "#89b4fa" if is_dark else "#2563eb"
        shift_fg = "#11111b" if is_dark else "#ffffff"
        for s_btn in self.shift_buttons:
            if self.is_shift:
                s_btn.setStyleSheet(f"background-color: {shift_bg} !important; border: 2px solid {shift_fg}; border-radius: 6px;")
            else:
                s_btn.setStyleSheet("")
            s_btn.update_visuals(self.is_shift, self.is_caps, is_dark)

        # Caps Active Highlight
        caps_bg = "#a6e3a1" if is_dark else "#16a34a"
        caps_fg = "#11111b" if is_dark else "#ffffff"
        if self.caps_button:
            if self.is_caps:
                self.caps_button.setStyleSheet(f"background-color: {caps_bg} !important; border: 2px solid {caps_fg}; border-radius: 6px;")
            else:
                self.caps_button.setStyleSheet("")
            self.caps_button.update_visuals(self.is_shift, self.is_caps, is_dark)

    def refresh_styles(self):
        self.setStyleSheet(self.theme_manager.get_keyboard_stylesheet())
        self.refresh_key_labels()
