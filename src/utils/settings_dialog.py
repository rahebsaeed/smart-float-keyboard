from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton

class SettingsDialog(QDialog):
    settingsSaved = pyqtSignal(dict)

    def __init__(self, config_manager, theme_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.theme_manager = theme_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("⚙ Keyboard Settings")
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
        self.setFixedSize(360, 380)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setObjectName("settingsContainer")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(18, 14, 18, 16)
        layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        title = QLabel("⚙ Settings & Preferences")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(22, 22)
        close_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        close_btn.setStyleSheet("""
            QPushButton { background: #f38ba8; color: #111; border-radius: 11px; border: none; font-weight: bold; }
            QPushButton:hover { background: #eba0ac; }
        """)
        close_btn.clicked.connect(self.close)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(close_btn)
        layout.addLayout(header)

        # 1. Default Language
        lbl_lang = QLabel("Default Language:")
        lbl_lang.setStyleSheet("font-size: 11px; color: #a6adc8;")
        self.combo_lang = QComboBox()
        self.combo_lang.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.combo_lang.addItem("🇺🇸 English (US)", "en")
        self.combo_lang.addItem("🇫🇷 Français (AZERTY)", "fr")
        self.combo_lang.addItem("🇸🇦 العربية (Arabic)", "ar")
        
        current_lang = self.config_manager.get("language", "en")
        index = self.combo_lang.findData(current_lang)
        if index >= 0:
            self.combo_lang.setCurrentIndex(index)
        layout.addWidget(lbl_lang)
        layout.addWidget(self.combo_lang)

        # 2. Toggle Icon
        lbl_icon = QLabel("Floating Toggle Icon:")
        lbl_icon.setStyleSheet("font-size: 11px; color: #a6adc8;")
        self.combo_icon = QComboBox()
        self.combo_icon.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.combo_icon.addItem("⌨ Keyboard", "⌨")
        self.combo_icon.addItem("⚡ Circuit", "⚡")
        self.combo_icon.addItem("🖮 Board", "🖮")
        self.combo_icon.addItem("✦ Star", "✦")
        self.combo_icon.addItem("💠 Badge", "💠")
        
        current_icon = self.config_manager.get("toggle_icon", "⌨")
        idx_icon = self.combo_icon.findData(current_icon)
        if idx_icon >= 0:
            self.combo_icon.setCurrentIndex(idx_icon)
        layout.addWidget(lbl_icon)
        layout.addWidget(self.combo_icon)

        # 3. Default Scale
        lbl_scale = QLabel("Default Size Scale:")
        lbl_scale.setStyleSheet("font-size: 11px; color: #a6adc8;")
        self.combo_scale = QComboBox()
        self.combo_scale.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.combo_scale.addItem("Compact (80%)", 0.8)
        self.combo_scale.addItem("Normal (100%)", 1.0)
        self.combo_scale.addItem("Large (120%)", 1.2)
        self.combo_scale.addItem("Extra Large (140%)", 1.4)
        
        current_scale = self.config_manager.get("scale", 1.0)
        idx_scale = self.combo_scale.findData(current_scale)
        if idx_scale >= 0:
            self.combo_scale.setCurrentIndex(idx_scale)
        layout.addWidget(lbl_scale)
        layout.addWidget(self.combo_scale)

        # 4. Save Button
        save_btn = QPushButton("💾 Save & Apply")
        save_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        save_btn.setFixedHeight(34)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: #ffffff;
                font-weight: bold;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover { background-color: #60a5fa; }
        """)
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)

        main_layout.addWidget(container)
        self.setLayout(main_layout)
        self.apply_theme()

    def save_settings(self):
        selected_lang = self.combo_lang.currentData()
        selected_icon = self.combo_icon.currentData()
        selected_scale = self.combo_scale.currentData()

        self.config_manager.set("language", selected_lang)
        self.config_manager.set("toggle_icon", selected_icon)
        self.config_manager.set("scale", selected_scale)

        self.settingsSaved.emit({
            "language": selected_lang,
            "toggle_icon": selected_icon,
            "scale": selected_scale
        })
        self.close()

    def apply_theme(self):
        is_dark = self.theme_manager.is_dark()
        bg_color = "rgba(30, 30, 46, 0.98)" if is_dark else "rgba(248, 249, 250, 0.98)"
        text_color = "#cdd6f4" if is_dark else "#1e293b"
        card_border = "#45475a" if is_dark else "#cbd5e1"
        combo_bg = "#313244" if is_dark else "#ffffff"

        self.setStyleSheet(f"""
            #settingsContainer {{
                background-color: {bg_color};
                border: 2px solid {card_border};
                border-radius: 14px;
                color: {text_color};
            }}
            QLabel {{
                color: {text_color};
                border: none;
            }}
            QComboBox {{
                background-color: {combo_bg};
                color: {text_color};
                border: 1px solid {card_border};
                border-radius: 6px;
                padding: 5px 10px;
                font-size: 12px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {combo_bg};
                color: {text_color};
                selection-background-color: #3b82f6;
            }}
        """)