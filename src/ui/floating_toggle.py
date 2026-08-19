from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
from PyQt6.QtGui import QCursor

class DraggableCircleButton(QPushButton):
    dragged_y = pyqtSignal(int)
    clicked_clean = pyqtSignal()

    def __init__(self, text="⌨", parent=None):
        super().__init__(text, parent)
        self._start_pos = None
        self._is_dragging = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._start_pos = event.globalPosition().toPoint()
            self._is_dragging = False
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._start_pos is not None:
            delta = (event.globalPosition().toPoint() - self._start_pos).manhattanLength()
            if delta > 4:
                self._is_dragging = True
                self.dragged_y.emit(event.globalPosition().toPoint().y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self._is_dragging:
                self.clicked_clean.emit()
            self._start_pos = None
            self._is_dragging = False
        super().mouseReleaseEvent(event)

class FloatingToggle(QWidget):
    toggled = pyqtSignal()
    positionChanged = pyqtSignal(int)

    def __init__(self, icon_text="⌨", size_px=38):
        super().__init__()
        self.icon_text = icon_text
        self.size_px = size_px
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

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.btn = DraggableCircleButton(self.icon_text, self)
        self.btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))

        self.btn.dragged_y.connect(self.snap_to_y)
        self.btn.clicked_clean.connect(self.toggled.emit)

        self.layout.addWidget(self.btn)
        self.apply_dimensions()

        screen = QApplication.primaryScreen().geometry()
        self.snap_to_y(screen.height() // 2)

    def set_icon(self, new_icon: str):
        self.icon_text = new_icon
        self.btn.setText(new_icon)

    def set_size(self, size_px: int):
        self.size_px = size_px
        self.apply_dimensions()

    def apply_dimensions(self):
        self.btn.setFixedSize(self.size_px, self.size_px)
        font_sz = max(11, int(self.size_px * 0.46))
        radius = self.size_px // 2

        self.btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b82f6, stop:1 #1d4ed8);
                color: #ffffff;
                font-size: {font_sz}px;
                border-radius: {radius}px;
                border: 2px solid rgba(255, 255, 255, 0.7);
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #60a5fa, stop:1 #2563eb);
                border: 2px solid #ffffff;
            }}
            QPushButton:pressed {{
                background: #1e40af;
            }}
        """)
        self.resize(self.size_px + 2, self.size_px + 2)
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 4, self.pos().y())

    def snap_to_y(self, global_y: int):
        screen = QApplication.primaryScreen().geometry()
        new_y = global_y - (self.height() // 2)
        new_y = max(10, min(new_y, screen.height() - self.height() - 10))
        self.move(screen.width() - self.width() - 4, new_y)
        self.positionChanged.emit(new_y)
