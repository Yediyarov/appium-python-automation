from __future__ import annotations

from datetime import datetime
from pathlib import Path

from selenium.common.exceptions import WebDriverException


def safe_artifact_name(value: str) -> str:
    return "".join(
        character if character.isalnum() or character in "-_." else "_"
        for character in value
    )


def save_screenshot(driver, directory: Path, name: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = directory / f"{timestamp}_{safe_artifact_name(name)}.png"
    driver.save_screenshot(str(path))
    return path


def try_save_screenshot(driver, directory: Path, name: str) -> Path | None:
    try:
        return save_screenshot(driver, directory, name)
    except WebDriverException:
        return None
