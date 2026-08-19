"""
Theme Manager: Handles Dark and Light color palettes and styling.
"""

class ThemeManager:
    DARK = "dark"
    LIGHT = "light"

    def __init__(self, current_theme="dark"):
        self.current_theme = current_theme

    def toggle_theme(self):
        self.current_theme = self.LIGHT if self.current_theme == self.DARK else self.DARK
        return self.current_theme

    def is_dark(self):
        return self.current_theme == self.DARK

    def get_keyboard_stylesheet(self):
        if self.is_dark():
            return """
                #keyboardContainer {
                    background-color: rgba(24, 24, 37, 0.97);
                    border: 2px solid #45475a;
                    border-radius: 14px;
                }
                #headerTitle {
                    color: #a6adc8;
                    font-size: 12px;
                    font-weight: bold;
                    border: none;
                }
                #themeBtn {
                    background: #313244;
                    color: #f9e2af;
                    border: 1px solid #45475a;
                    border-radius: 12px;
                    font-size: 12px;
                }
                #themeBtn:hover { background: #45475a; }
                #closeBtn {
                    background: #f38ba8;
                    color: #11111b;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: bold;
                    border: none;
                }
                #closeBtn:hover { background: #eba0ac; }
                QPushButton.keyBtn {
                    background-color: #313244;
                    border: 1px solid #45475a;
                    border-radius: 6px;
                }
                QPushButton.keyBtn:hover {
                    background-color: #45475a;
                    border-color: #89b4fa;
                }
                QPushButton.keyBtn:pressed {
                    background-color: #89b4fa;
                }
            """
        else:
            return """
                #keyboardContainer {
                    background-color: rgba(248, 249, 250, 0.98);
                    border: 2px solid #cbd5e1;
                    border-radius: 14px;
                }
                #headerTitle {
                    color: #475569;
                    font-size: 12px;
                    font-weight: bold;
                    border: none;
                }
                #themeBtn {
                    background: #e2e8f0;
                    color: #d97706;
                    border: 1px solid #cbd5e1;
                    border-radius: 12px;
                    font-size: 12px;
                }
                #themeBtn:hover { background: #cbd5e1; }
                #closeBtn {
                    background: #ef4444;
                    color: #ffffff;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: bold;
                    border: none;
                }
                #closeBtn:hover { background: #dc2626; }
                QPushButton.keyBtn {
                    background-color: #ffffff;
                    border: 1px solid #cbd5e1;
                    border-radius: 6px;
                }
                QPushButton.keyBtn:hover {
                    background-color: #f1f5f9;
                    border-color: #3b82f6;
                }
                QPushButton.keyBtn:pressed {
                    background-color: #3b82f6;
                }
            """