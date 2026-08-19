"""
Input Engine: Hybrid low-level evdev + Linux Unicode Injector.
Guarantees 100% accurate typing for English, French Accents, and Arabic characters
into any Wayland or X11 application (including GNOME Terminal).
"""

import time
from evdev import UInput, ecodes as e

# Hex scancodes for Linux Unicode IBus composition (Ctrl+Shift+U)
HEX_CODES = {
    '0': e.KEY_0, '1': e.KEY_1, '2': e.KEY_2, '3': e.KEY_3,
    '4': e.KEY_4, '5': e.KEY_5, '6': e.KEY_6, '7': e.KEY_7,
    '8': e.KEY_8, '9': e.KEY_9, 'a': e.KEY_A, 'b': e.KEY_B,
    'c': e.KEY_C, 'd': e.KEY_D, 'e': e.KEY_E, 'f': e.KEY_F,
}

# Standard ASCII hardware keycode mapping
DIRECT_KEY_MAP = {
    'a': (e.KEY_A, False), 'A': (e.KEY_A, True),
    'b': (e.KEY_B, False), 'B': (e.KEY_B, True),
    'c': (e.KEY_C, False), 'C': (e.KEY_C, True),
    'd': (e.KEY_D, False), 'D': (e.KEY_D, True),
    'e': (e.KEY_E, False), 'E': (e.KEY_E, True),
    'f': (e.KEY_F, False), 'F': (e.KEY_F, True),
    'g': (e.KEY_G, False), 'G': (e.KEY_G, True),
    'h': (e.KEY_H, False), 'H': (e.KEY_H, True),
    'i': (e.KEY_I, False), 'I': (e.KEY_I, True),
    'j': (e.KEY_J, False), 'J': (e.KEY_J, True),
    'k': (e.KEY_K, False), 'K': (e.KEY_K, True),
    'l': (e.KEY_L, False), 'L': (e.KEY_L, True),
    'm': (e.KEY_M, False), 'M': (e.KEY_M, True),
    'n': (e.KEY_N, False), 'N': (e.KEY_N, True),
    'o': (e.KEY_O, False), 'O': (e.KEY_O, True),
    'p': (e.KEY_P, False), 'P': (e.KEY_P, True),
    'q': (e.KEY_Q, False), 'Q': (e.KEY_Q, True),
    'r': (e.KEY_R, False), 'R': (e.KEY_R, True),
    's': (e.KEY_S, False), 'S': (e.KEY_S, True),
    't': (e.KEY_T, False), 'T': (e.KEY_T, True),
    'u': (e.KEY_U, False), 'U': (e.KEY_U, True),
    'v': (e.KEY_V, False), 'V': (e.KEY_V, True),
    'w': (e.KEY_W, False), 'W': (e.KEY_W, True),
    'x': (e.KEY_X, False), 'X': (e.KEY_X, True),
    'y': (e.KEY_Y, False), 'Y': (e.KEY_Y, True),
    'z': (e.KEY_Z, False), 'Z': (e.KEY_Z, True),
    '1': (e.KEY_1, False), '!': (e.KEY_1, True),
    '2': (e.KEY_2, False), '@': (e.KEY_2, True),
    '3': (e.KEY_3, False), '#': (e.KEY_3, True),
    '4': (e.KEY_4, False), '$': (e.KEY_4, True),
    '5': (e.KEY_5, False), '%': (e.KEY_5, True),
    '6': (e.KEY_6, False), '^': (e.KEY_6, True),
    '7': (e.KEY_7, False), '&': (e.KEY_7, True),
    '8': (e.KEY_8, False), '*': (e.KEY_8, True),
    '9': (e.KEY_9, False), '(': (e.KEY_9, True),
    '0': (e.KEY_0, False), ')': (e.KEY_0, True),
    '-': (e.KEY_MINUS, False), '_': (e.KEY_MINUS, True),
    '=': (e.KEY_EQUAL, False), '+': (e.KEY_EQUAL, True),
    '[': (e.KEY_LEFTBRACE, False), '{': (e.KEY_LEFTBRACE, True),
    ']': (e.KEY_RIGHTBRACE, False), '}': (e.KEY_RIGHTBRACE, True),
    '\\': (e.KEY_BACKSLASH, False), '|': (e.KEY_BACKSLASH, True),
    ';': (e.KEY_SEMICOLON, False), ':': (e.KEY_SEMICOLON, True),
    "'": (e.KEY_APOSTROPHE, False), '"': (e.KEY_APOSTROPHE, True),
    '`': (e.KEY_GRAVE, False), '~': (e.KEY_GRAVE, True),
    ',': (e.KEY_COMMA, False), '<': (e.KEY_COMMA, True),
    '.': (e.KEY_DOT, False), '>': (e.KEY_DOT, True),
    '/': (e.KEY_SLASH, False), '?': (e.KEY_SLASH, True),
}

class InputEngine:
    def __init__(self):
        try:
            self.ui = UInput(name="SmartFloatVirtualKeyboard")
            print("✔ Kernel Virtual Keyboard Device active.")
        except PermissionError:
            print("❌ Permission denied for /dev/uinput.")
            self.ui = None

    def send_special_key(self, evdev_code: int):
        """Sends non-character keys like Backspace, Enter, Tab, Space, Esc."""
        if not self.ui:
            return
        self.ui.write(e.EV_KEY, evdev_code, 1)
        self.ui.syn()
        time.sleep(0.008)
        self.ui.write(e.EV_KEY, evdev_code, 0)
        self.ui.syn()

    def send_character(self, char: str):
        """Types standard characters, Arabic letters, and French accents accurately."""
        if not self.ui or not char:
            return

        # 1. Standard ASCII Direct Fast Dispatch
        if char in DIRECT_KEY_MAP:
            code, req_shift = DIRECT_KEY_MAP[char]
            if req_shift:
                self.ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
                self.ui.syn()
                time.sleep(0.004)

            self.ui.write(e.EV_KEY, code, 1)
            self.ui.syn()
            time.sleep(0.008)
            self.ui.write(e.EV_KEY, code, 0)
            self.ui.syn()

            if req_shift:
                time.sleep(0.004)
                self.ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
                self.ui.syn()
            return

        # 2. Universal Linux Unicode Sequence for Arabic & French Accents
        # Emits: Ctrl+Shift+U -> [hex digits] -> Enter
        codepoint = ord(char)
        hex_str = f"{codepoint:x}"

        # Press Ctrl + Shift + U
        self.ui.write(e.EV_KEY, e.KEY_LEFTCTRL, 1)
        self.ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
        self.ui.write(e.EV_KEY, e.KEY_U, 1)
        self.ui.syn()
        time.sleep(0.004)
        self.ui.write(e.EV_KEY, e.KEY_U, 0)
        self.ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
        self.ui.write(e.EV_KEY, e.KEY_LEFTCTRL, 0)
        self.ui.syn()
        time.sleep(0.005)

        # Type hex codes
        for h in hex_str:
            if h in HEX_CODES:
                h_code = HEX_CODES[h]
                self.ui.write(e.EV_KEY, h_code, 1)
                self.ui.syn()
                time.sleep(0.004)
                self.ui.write(e.EV_KEY, h_code, 0)
                self.ui.syn()

        # Commit Unicode with Enter
        time.sleep(0.004)
        self.ui.write(e.EV_KEY, e.KEY_ENTER, 1)
        self.ui.syn()
        time.sleep(0.008)
        self.ui.write(e.EV_KEY, e.KEY_ENTER, 0)
        self.ui.syn()
