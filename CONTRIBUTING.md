# Contributing to Smart Float Keyboard

Thank you for your interest in contributing to **Smart Float Keyboard**! This project is open-source, and we welcome contributions from developers worldwide.

## Ways to Contribute
1. **Adding New Languages:**
   - Open `src/core/layouts.py`.
   - Add your language layout matrix following the existing format (`ENGLISH_US_LAYOUT`, `FRENCH_AZERTY_LAYOUT`, `ARABIC_LAYOUT`).
   - Register the layout in `LANGUAGE_REGISTRY`.
2. **Bug Fixes & UI Enhancements:**
   - Themes, animations, touchscreen improvements, or Wayland/X11 optimizations.
3. **Packaging Improvements:**
   - Debian packaging scripts or Snapcraft configuration.

## Development Workflow
1. Fork the repository on GitHub.
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/smart-float-keyboard.git
   cd smart-float-keyboard
   ```
3. Set up your virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt  # Or: pip install PyQt6 evdev
   ```
4. Run the app locally:
   ```bash
   python3 src/main.py
   ```
5. Create a branch and submit a Pull Request!
