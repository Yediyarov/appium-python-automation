from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _bool_from_env(name: str, default: bool) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    return raw_value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _optional_path_from_env(name: str) -> Path | None:
    raw_value = os.getenv(name)
    if not raw_value:
        return None

    return Path(raw_value).expanduser().resolve()


@dataclass(frozen=True)
class Settings:
    appium_server_url: str
    android_device_name: str
    android_platform_version: str | None
    tasks_apk_path: Path | None
    app_package: str | None
    app_activity: str | None
    no_reset: bool
    auto_grant_permissions: bool
    command_timeout_seconds: int
    explicit_wait_seconds: int
    screenshot_dir: Path

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            appium_server_url=os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723"),
            android_device_name=os.getenv("ANDROID_DEVICE_NAME", "Android Emulator"),
            android_platform_version=os.getenv("ANDROID_PLATFORM_VERSION") or None,
            tasks_apk_path=_optional_path_from_env("TASKS_APK_PATH"),
            app_package=os.getenv("APP_PACKAGE") or "org.tasks",
            app_activity=os.getenv("APP_ACTIVITY") or None,
            no_reset=_bool_from_env("NO_RESET", default=False),
            auto_grant_permissions=_bool_from_env("AUTO_GRANT_PERMISSIONS", default=True),
            command_timeout_seconds=int(os.getenv("APPIUM_COMMAND_TIMEOUT_SECONDS", "120")),
            explicit_wait_seconds=int(os.getenv("EXPLICIT_WAIT_SECONDS", "15")),
            screenshot_dir=Path(os.getenv("SCREENSHOT_DIR", "artifacts/screenshots")).resolve(),
        )

    def validate_for_appium(self) -> None:
        if self.tasks_apk_path is not None and not self.tasks_apk_path.exists():
            raise FileNotFoundError(
                f"TASKS_APK_PATH points to a missing file: {self.tasks_apk_path}"
            )

        if self.tasks_apk_path is None and not (self.app_package and self.app_activity):
            raise ValueError(
                "Set TASKS_APK_PATH, or set both APP_PACKAGE and APP_ACTIVITY for an "
                "already installed app."
            )
