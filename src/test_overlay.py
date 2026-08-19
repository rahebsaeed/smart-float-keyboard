import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from core.input_engine import InputEngine

class NonFocusFloatingTest(QWidget):
    def __init__(self):
        super().__init__()
        self.input_engine = InputEngine()
        self.init_ui()

    def init_ui(self):
        # 1. Critical Window Flags: Stay on top + never steal focus
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        
        # 2. Prevent window activation on mouse click
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setAttribute(Qt.WidgetAttribute.WA_X11DoNotAcceptFocus, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

        # Style the test window
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 2px solid #89b4fa;
                border-radius: 10px;
                font-family: sans-serif;
            }
            QPushButton {
                background-color: #313244;
                color: #ffffff;
                border: 1px solid #45475a;
                border-radius: 6px;
                padding: 10px 14px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45475a;
                border-color: #89b4fa;
            }
            QPushButton:pressed {
                background-color: #89b4fa;
                color: #11111b;
            }
            QLabel {
                border: none;
                font-size: 11px;
                color: #a6adc8;
            }
        """)

        # Layout
        main_layout = QVBoxLayout()
        header = QLabel("⚡ Test Floating Bar (Drag to move)")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        btn_layout = QHBoxLayout()
        
        # Buttons for testing
        buttons = [
            ("A", lambda: self.input_engine.tap_key("a")),
            ("B", lambda: self.input_engine.tap_key("b")),
            ("Hello", lambda: self.input_engine.type_text("Hello ")),
            ("⌫ Del", lambda: self.input_engine.press_special("BACKSPACE")),
            ("↵ Enter", lambda: self.input_engine.press_special("ENTER")),
            ("✕ Close", self.close)
        ]

        for text, callback in buttons:
            btn = QPushButton(text)
            # CRITICAL: Buttons must not accept keyboard focus
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.clicked.connect(callback)
            btn_layout.addWidget(btn)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

        # Position at the top-right of the screen
        self.resize(420, 100)
        screen_geometry = QApplication.primaryScreen().geometry()
        self.move(screen_geometry.width() - 440, 60)

        # Mouse drag tracking support
        self._drag_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_bar = NonFocusFloatingTest()
    test_bar.show()
    sys.exit(app.exec())