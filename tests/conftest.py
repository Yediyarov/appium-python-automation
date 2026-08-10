from __future__ import annotations

import pytest

from mobile_automation.artifacts import save_screenshot
from mobile_automation.config import Settings
from mobile_automation.driver_factory import create_android_driver


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings.from_env()


@pytest.fixture
def driver(request: pytest.FixtureRequest, settings: Settings):
    try:
        appium_driver = create_android_driver(settings)
    except (FileNotFoundError, ValueError) as error:
        pytest.skip(f"Appium runtime is not configured: {error}")

    request.node.driver = appium_driver
    yield appium_driver
    appium_driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    appium_driver = getattr(item, "driver", None)
    settings = Settings.from_env()
    if appium_driver is None:
        return

    screenshot_path = save_screenshot(appium_driver, settings.screenshot_dir, item.name)
    html_plugin = item.config.pluginmanager.getplugin("html")
    if html_plugin:
        extra = getattr(report, "extra", [])
        extra.append(html_plugin.extras.image(str(screenshot_path)))
        report.extra = extra

