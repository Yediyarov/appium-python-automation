from __future__ import annotations

from datetime import datetime


def unique_task_title(prefix: str = "Appium task") -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{prefix} {timestamp}"

