#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ANDROID_HOME="${ANDROID_HOME:-$HOME/Library/Android/sdk}"

export ANDROID_HOME
export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"
export TASKS_APK_PATH="${TASKS_APK_PATH:-$PROJECT_ROOT/apps/tasks-org-15.9.apk}"
export APPIUM_SERVER_URL="${APPIUM_SERVER_URL:-http://127.0.0.1:4723}"
export ANDROID_DEVICE_NAME="${ANDROID_DEVICE_NAME:-Android Emulator}"
export APP_PACKAGE="${APP_PACKAGE:-org.tasks}"
export APP_ACTIVITY="${APP_ACTIVITY:-com.todoroo.astrid.activity.TaskListActivity}"
export NO_RESET="${NO_RESET:-false}"
export AUTO_GRANT_PERMISSIONS="${AUTO_GRANT_PERMISSIONS:-true}"

fail_preflight() {
  echo "Android test preflight failed: $1" >&2
  exit 1
}

if [[ ! -f "$TASKS_APK_PATH" ]]; then
  fail_preflight "TASKS_APK_PATH does not point to an APK: $TASKS_APK_PATH"
fi

if ! command -v adb >/dev/null 2>&1; then
  fail_preflight "adb was not found. Check ANDROID_HOME: $ANDROID_HOME"
fi

if ! command -v curl >/dev/null 2>&1; then
  fail_preflight "curl was not found and is required to check Appium server status"
fi

if ! curl --silent --fail "$APPIUM_SERVER_URL/status" >/dev/null; then
  fail_preflight "Appium server is not reachable at $APPIUM_SERVER_URL. Start it with: bash scripts/start_appium.sh"
fi

if ! adb devices | awk 'NR > 1 && $2 == "device" { found = 1 } END { exit !found }'; then
  fail_preflight "no Android emulator/device is connected. Start an emulator before running tests"
fi

cd "$PROJECT_ROOT"

if [[ $# -eq 0 ]]; then
  set -- -m smoke
fi

.venv/bin/pytest "$@"
