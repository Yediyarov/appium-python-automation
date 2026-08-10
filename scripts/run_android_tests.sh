#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ANDROID_HOME="${ANDROID_HOME:-$HOME/Library/Android/sdk}"

export ANDROID_HOME
export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"
export TASKS_APK_PATH="${TASKS_APK_PATH:-$PROJECT_ROOT/apps/tasks-org-15.9.apk}"
export APPIUM_SERVER_URL="${APPIUM_SERVER_URL:-http://127.0.0.1:4723}"
export ANDROID_DEVICE_NAME="${ANDROID_DEVICE_NAME:-Android Emulator}"
export NO_RESET="${NO_RESET:-false}"
export AUTO_GRANT_PERMISSIONS="${AUTO_GRANT_PERMISSIONS:-true}"

if [[ ! -f "$TASKS_APK_PATH" ]]; then
  echo "TASKS_APK_PATH does not point to an APK: $TASKS_APK_PATH" >&2
  exit 1
fi

cd "$PROJECT_ROOT"

if [[ $# -eq 0 ]]; then
  set -- -m smoke
fi

.venv/bin/pytest "$@"

