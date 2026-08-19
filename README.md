# ⌨ Smart Float Keyboard

<p align="center">
  <img src="assets/icons/smart-keyboard.svg" alt="Smart Float Keyboard Logo" width="96" height="96">
</p>

<p align="center">
  <b>A modern, high-performance, non-intrusive floating on-screen keyboard for Ubuntu Linux.</b><br>
  Engineered with universal Linux kernel input injection, multi-language layouts, and flexible dock positioning.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Ubuntu%20%7C%20Debian%20%7C%20Linux-E95420?logo=ubuntu&logoColor=white" alt="Platform">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GUI-PyQt6-green?logo=qt&logoColor=white" alt="GUI">
  <img src="https://img.shields.io/badge/License-MIT-purple" alt="License">
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen" alt="PRs Welcome">
</p>

---

## 📸 Screenshots

*(Place your screenshots in `docs/screenshots/` and link them here)*

| Dark Obsidian Mode | Clean Light Mode |
|:---:|:---:|
| *(Add dark mode picture)* | *(Add light mode picture)* |

---

## ✨ Features

- 📌 **Always-on-Top Floating Toggle Badge:** A compact, draggable circular badge locked smoothly to the right screen edge.
- ⚡ **Non-Focus Kernel Input Engine:** Types directly into active text cursors across all applications (GNOME Terminal, Chrome, VS Code, Gedit, etc.) without stealing focus.
- 🌐 **Multi-Language Architecture:**
  - 🇺🇸 **English (US Standard QWERTY)**
  - 🇫🇷 **Français (AZERTY)** with full accent injection (`é`, `è`, `à`, `ç`, `ù`)
  - 🇸🇦 **العربية (Arabic 101)** with direct Unicode support (`ض`, `ص`, `ث`, `ّ`, Harakat)
- 🔠 **Hardware-Style Dual Character Keys:** Secondary Shift symbols and diacritics displayed directly on keys with active Shift lighting.
- 🔒 **Shift Lock & Caps Lock:** Persistent shift mode for effortless symbol/capital typing.
- 🎨 **Dynamic Theming:** Instant one-click switching between **Dark Obsidian** and **Clean Light** themes.
- ↔ **Full Freedom of Motion & Resizing:**
  - Drag the keyboard anywhere across your screen.
  - Scale up/down with `[＋]` / `[－]` buttons or drag the corner resize grip.
- ⚙ **Customization & Settings:**
  - Choose toggle button size (Mini 30px, Small 38px, Medium 48px, Large 58px).
  - Select toggle icons (`⌨`, `⚡`, `🖮`, `✦`, `❖`).
  - Set default startup language and size scale.
  - Automatic persistence to `~/.config/smart-float-keyboard/config.json`.

---

## 🚀 Installation

### Option 1: Install via `.deb` Package (Recommended)

1. Download the latest `.deb` release:
   ```bash
   sudo apt update
   sudo apt install ./smart-float-keyboard_1.0.1.deb
   ```
2. Launch it from your Ubuntu Dash / Application Menu by searching **"Smart Float Keyboard"**, or run:
   ```bash
   smart-keyboard
   ```

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/your-username/smart-float-keyboard.git
cd smart-float-keyboard

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python3 src/main.py
```

---

## 🛠 Building the `.deb` Package

To build an installable `.deb` installer locally:

```bash
chmod +x build_deb.sh
./build_deb.sh
```
The output package will be generated at `build_deb/smart-float-keyboard_1.0.1.deb`.

---

## 👤 Author

**RAHEB Aref Mahyoub Saeed**
- GitHub: [@your-username](https://github.com/your-username)
- Project: [Smart Float Keyboard](https://github.com/your-username/smart-float-keyboard)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](../../issues) or submit a Pull Request.

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
