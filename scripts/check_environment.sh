#!/usr/bin/env bash
set -euo pipefail

ANDROID_HOME="${ANDROID_HOME:-$HOME/Library/Android/sdk}"
export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"

echo "Python:"
python3.11 --version

echo
echo "pytest:"
.venv/bin/pytest --version

echo
echo "Node:"
node --version

echo
echo "npm:"
npm --version

echo
echo "Appium:"
appium --version

echo
echo "Installed Appium drivers:"
appium driver list --installed

echo
echo "adb:"
adb version

echo
echo "Android virtual devices:"
emulator -list-avds

