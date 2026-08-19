#!/bin/bash
set -e

VERSION="1.0.1"
PKG_NAME="smart-float-keyboard"
BUILD_DIR="build_deb/${PKG_NAME}_${VERSION}"

echo "🔨 Building Debian (.deb) Package for ${PKG_NAME} v${VERSION}..."

rm -rf build_deb
mkdir -p "${BUILD_DIR}/DEBIAN"
mkdir -p "${BUILD_DIR}/usr/share/${PKG_NAME}/src/core"
mkdir -p "${BUILD_DIR}/usr/share/${PKG_NAME}/src/ui"
mkdir -p "${BUILD_DIR}/usr/share/${PKG_NAME}/src/utils"
mkdir -p "${BUILD_DIR}/usr/share/${PKG_NAME}/assets/icons"
mkdir -p "${BUILD_DIR}/usr/bin"
mkdir -p "${BUILD_DIR}/usr/share/applications"
mkdir -p "${BUILD_DIR}/usr/share/icons/hicolor/scalable/apps"
mkdir -p "${BUILD_DIR}/etc/udev/rules.d"

cp -r src/* "${BUILD_DIR}/usr/share/${PKG_NAME}/src/"
cp -r assets/* "${BUILD_DIR}/usr/share/${PKG_NAME}/assets/"
cp smart-keyboard.desktop "${BUILD_DIR}/usr/share/applications/"
cp assets/icons/smart-keyboard.svg "${BUILD_DIR}/usr/share/icons/hicolor/scalable/apps/smart-keyboard.svg"

cat << 'LAUNCHER' > "${BUILD_DIR}/usr/bin/smart-keyboard"
#!/bin/bash
export QT_QPA_PLATFORM=xcb
exec python3 /usr/share/smart-float-keyboard/src/main.py "$@"
LAUNCHER
chmod +x "${BUILD_DIR}/usr/bin/smart-keyboard"

echo 'KERNEL=="uinput", MODE="0666"' > "${BUILD_DIR}/etc/udev/rules.d/99-smart-float-keyboard.rules"

cat << CONTROL > "${BUILD_DIR}/DEBIAN/control"
Package: ${PKG_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-pip, python3-pyqt6, python3-evdev, libxcb-cursor0
Maintainer: Developer <dev@example.com>
Description: Smart Float Keyboard
 A modern, floating virtual on-screen keyboard with non-focus injection,
 multi-language support (EN, FR, AR), and dark/light themes.
CONTROL

cat << 'POSTINST' > "${BUILD_DIR}/DEBIAN/postinst"
#!/bin/sh
set -e
udevadm control --reload-rules && udevadm trigger || true
modprobe uinput || true
exit 0
POSTINST
chmod 755 "${BUILD_DIR}/DEBIAN/postinst"

dpkg-deb --build "${BUILD_DIR}"
echo "✅ Package created: build_deb/${PKG_NAME}_${VERSION}.deb"
