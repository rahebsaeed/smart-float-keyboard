# ⌨ Smart Float Keyboard

<p align="center">
  <img src="assets/icons/smart-keyboard.svg" alt="Smart Float Keyboard Logo" width="96" height="96">
</p>

<p align="center">
  <b>A modern, high-performance, non-intrusive floating on-screen keyboard for Ubuntu Linux.</b><br>
  Engineered with universal Linux kernel input injection, multi-language layouts, persistent shift lock, and dynamic edge docking.
</p>

<p align="center">
  <a href="https://github.com/rahebsaeed/smart-float-keyboard/actions/workflows/ci.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/rahebsaeed/smart-float-keyboard/ci.yml?branch=main&label=Build%20%26%20CI" alt="CI Status">
  </a>
  <img src="https://img.shields.io/badge/Platform-Ubuntu%20%7C%20Debian%20%7C%20Linux-E95420?logo=ubuntu&logoColor=white" alt="Platform">
  <img src="https://img.shields.io/badge/PPA-ppa%3Arahebsaeed%2Fsmart--keyboard-orange?logo=ubuntu&logoColor=white" alt="PPA">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GUI-PyQt6-green?logo=qt&logoColor=white" alt="GUI">
  <img src="https://img.shields.io/badge/License-MIT-purple" alt="License">
</p>

---

## 📸 Screenshots

| ☾ Dark Obsidian Mode | ☀ Clean Light Mode |
|:---:|:---:|
| <img src="docs/screenshots/Screenshot%20from%202026-08-19%2018-59-58.png" alt="Dark Mode Screenshot" width="100%"> | <img src="docs/screenshots/Screenshot%20from%202026-08-19%2019-00-05.png" alt="Light Mode Screenshot" width="100%"> |

---

## ✨ Features

- 📌 **Always-on-Top Edge Dock:** Compact, draggable circular toggle badge smoothly locked along the right screen edge.
- ⚡ **Non-Focus Kernel Input Engine:** Types directly into any active text field (GNOME Terminal, Chrome, VS Code, Gedit, etc.) without stealing window focus.
- 🌐 **Multi-Language Architecture:**
  - 🇺🇸 **English (US Standard QWERTY)**
  - 🇫🇷 **Français (AZERTY)** with full accent injection (`é`, `è`, `à`, `ç`, `ù`)
  - 🇸🇦 **العربية (Arabic 101)** with direct Unicode support (`ض`, `ص`, `ث`, `ّ`, Harakat)
- 🔠 **Hardware-Style Dual Character Keys:** Secondary Shift symbols and diacritics displayed directly on keys with active Shift lighting.
- 🔒 **Persistent Shift Lock & Caps Lock:** Shift stays active across multiple keystrokes until explicitly toggled off.
- 🎨 **Dynamic Theming:** Instant one-click switching between **Dark Obsidian** (`☾`) and **Clean Light** (`☀`) modes.
- ↔ **Full Freedom of Motion & Resizing:**
  - Drag the keyboard anywhere across your screen.
  - Scale up/down with `[＋]` / `[－]` buttons or drag the corner resize grip.
- ⚙ **Settings & Customization:**
  - Customize toggle button size (Mini 30px, Small 38px, Medium 48px, Large 58px).
  - Select custom toggle icons (`⌨`, `⚡`, `🖮`, `✦`, `❖`).
  - Set default startup language and size scale.
  - Automatic persistence to `~/.config/smart-float-keyboard/config.json`.

---

## 🚀 Installation

### Option 1: Install via Official Launchpad PPA (APT)

```bash
# 1. Add the official PPA
sudo add-apt-repository ppa:rahebsaeed/smart-keyboard

# 2. Update and install
sudo apt update
sudo apt install smart-float-keyboard
```

---

### Option 2: Install via Standalone `.deb` Package

1. Download the latest `.deb` package from the **[Releases](https://github.com/rahebsaeed/smart-float-keyboard/releases)** page.
2. Install via APT:
   ```bash
   sudo apt update
   sudo apt install ./smart-float-keyboard_1.0.1.deb
   ```

---

### Option 3: Install via Canonical Snap Store

```bash
sudo snap install smart-float-keyboard
```

---

### Option 4: Run from Source

```bash
# 1. Clone repository
git clone https://github.com/rahebsaeed/smart-float-keyboard.git
cd smart-float-keyboard

# 2. Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Launch application
python3 src/main.py
```

---

## 🖥 Usage

After installation, launch **Smart Float Keyboard** by searching for it in the Ubuntu Application Dash, or run:

```bash
smart-keyboard
```

---

## 🛠 Building the `.deb` Package Locally

```bash
chmod +x build_deb.sh
./build_deb.sh
```
The output package will be generated at `build_deb/smart-float-keyboard_1.0.1.deb`.

---

## 👤 Author

**RAHEB Aref Mahyoub Saeed**
- GitHub: [@rahebsaeed](https://github.com/rahebsaeed)
- Repository: [smart-float-keyboard](https://github.com/rahebsaeed/smart-float-keyboard)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the **[Issues page](https://github.com/rahebsaeed/smart-float-keyboard/issues)** or submit a Pull Request.

## 📄 License

This project is licensed under the **MIT License** — see the **[LICENSE](LICENSE)** file for details.
