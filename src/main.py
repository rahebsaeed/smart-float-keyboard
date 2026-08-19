import os
import sys
import signal

os.environ["QT_QPA_PLATFORM"] = "xcb"

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication
from core.input_engine import InputEngine
from utils.config import ConfigManager
from ui.theme_manager import ThemeManager
from ui.floating_toggle import FloatingToggle
from ui.keyboard_view import KeyboardView
from ui.settings_dialog import SettingsDialog

class SmartFloatKeyboardApp:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.theme_manager = ThemeManager(self.config_manager.get("theme", "dark"))
        self.input_engine = InputEngine()

        initial_lang = self.config_manager.get("language", "en")
        initial_icon = self.config_manager.get("toggle_icon", "⌨")
        initial_tsize = self.config_manager.get("toggle_size", 38)
        initial_scale = self.config_manager.get("scale", 1.0)

        # UI Components
        self.toggle_button = FloatingToggle(icon_text=initial_icon, size_px=initial_tsize)
        self.keyboard_view = KeyboardView(self.theme_manager, current_lang=initial_lang)
        self.settings_dialog = None

        self.apply_scale(initial_scale)

        # Connect Signals
        self.toggle_button.toggled.connect(self.toggle_keyboard)
        self.keyboard_view.charTriggered.connect(self.input_engine.send_character)
        self.keyboard_view.specialKeyTriggered.connect(self.input_engine.send_special_key)
        self.keyboard_view.closeRequested.connect(self.hide_keyboard)
        self.keyboard_view.settingsRequested.connect(self.open_settings)
        self.keyboard_view.themeToggled.connect(self.save_theme_preference)
        self.keyboard_view.languageChanged.connect(lambda lang: self.config_manager.set("language", lang))

        self.toggle_button.show()

    def apply_scale(self, scale_val: float):
        base_w = 760
        base_h = 275
        self.keyboard_view.resize(int(base_w * scale_val), int(base_h * scale_val))

    def save_theme_preference(self):
        self.config_manager.set("theme", self.theme_manager.current_theme)

    def toggle_keyboard(self):
        if self.keyboard_view.isVisible():
            self.hide_keyboard()
        else:
            self.show_keyboard()

    def show_keyboard(self):
        if not self.keyboard_view.user_has_manually_moved:
            toggle_pos = self.toggle_button.pos()
            screen = QApplication.primaryScreen().geometry()
            
            kb_width = self.keyboard_view.width()
            kb_height = self.keyboard_view.height()
            
            target_x = screen.width() - kb_width - 50
            target_y = min(max(10, toggle_pos.y() - (kb_height // 2)), screen.height() - kb_height - 50)
            self.keyboard_view.move(target_x, target_y)
        
        self.keyboard_view.show()

    def hide_keyboard(self):
        self.keyboard_view.hide()
        if self.settings_dialog and self.settings_dialog.isVisible():
            self.settings_dialog.hide()

    def open_settings(self):
        if not self.settings_dialog:
            self.settings_dialog = SettingsDialog(self.config_manager, self.theme_manager)
            self.settings_dialog.settingsSaved.connect(self.apply_new_settings)
        
        kb_pos = self.keyboard_view.pos()
        self.settings_dialog.move(kb_pos.x() + 50, kb_pos.y() + 30)
        self.settings_dialog.show()

    def apply_new_settings(self, new_settings: dict):
        self.keyboard_view.set_language(new_settings["language"])
        self.toggle_button.set_icon(new_settings["toggle_icon"])
        self.toggle_button.set_size(new_settings["toggle_size"])
        self.apply_scale(new_settings["scale"])

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    app = QApplication(sys.argv)
    app.setApplicationName("SmartFloatKeyboard")
    
    timer = QTimer()
    timer.start(300)
    timer.timeout.connect(lambda: None)

    manager = SmartFloatKeyboardApp()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
