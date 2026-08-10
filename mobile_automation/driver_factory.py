from __future__ import annotations

from appium import webdriver
from appium.options.android import UiAutomator2Options

from mobile_automation.config import Settings


def create_android_driver(settings: Settings) -> webdriver.Remote:
    settings.validate_for_appium()

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = settings.android_device_name
    options.no_reset = settings.no_reset
    options.auto_grant_permissions = settings.auto_grant_permissions
    options.new_command_timeout = settings.command_timeout_seconds

    if settings.android_platform_version:
        options.platform_version = settings.android_platform_version

    if settings.tasks_apk_path:
        options.app = str(settings.tasks_apk_path)

    if settings.app_package:
        options.app_package = settings.app_package

    if settings.app_activity:
        options.app_activity = settings.app_activity

    options.set_capability("appium:uiautomator2ServerInstallTimeout", 60_000)
    options.set_capability("appium:adbExecTimeout", 60_000)

    return webdriver.Remote(settings.appium_server_url, options=options)
