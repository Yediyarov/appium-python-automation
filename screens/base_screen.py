from __future__ import annotations

from collections.abc import Iterable

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from mobile_automation.config import Settings
from mobile_automation.waits import Locator, Waits


class BaseScreen:
    def __init__(self, driver: WebDriver, settings: Settings) -> None:
        self.driver = driver
        self.settings = settings
        self.waits = Waits(driver, settings.explicit_wait_seconds)

    def find_visible(self, locator: Locator) -> WebElement:
        return self.waits.visible(locator)

    def tap(self, locator: Locator) -> None:
        self.waits.clickable(locator).click()

    def tap_first(self, locators: Iterable[Locator]) -> None:
        self.waits.first_clickable(locators).click()

    def type_text(self, locator: Locator, value: str, clear_first: bool = True) -> None:
        element = self.waits.visible(locator)
        if clear_first:
            element.clear()
        element.send_keys(value)

    def is_visible(self, locator: Locator, timeout_seconds: int = 2) -> bool:
        try:
            Waits(self.driver, timeout_seconds).visible(locator)
            return True
        except TimeoutException:
            return False

    def tap_if_visible(self, locator: Locator, timeout_seconds: int = 2) -> bool:
        try:
            Waits(self.driver, timeout_seconds).clickable(locator).click()
            return True
        except TimeoutException:
            return False

    def tap_first_if_visible(self, locators: Iterable[Locator], timeout_seconds: int = 2) -> bool:
        try:
            Waits(self.driver, timeout_seconds).first_clickable(locators).click()
            return True
        except TimeoutException:
            return False

    def text_is_visible(self, text: str, timeout_seconds: int = 2) -> bool:
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
        return self.is_visible(locator, timeout_seconds)

    def scroll_to_text(self, text: str) -> WebElement:
        selector = (
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().text("{text}"))'
        )
        return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)

    def dismiss_common_system_dialogs(self) -> None:
        candidates = [
            (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"),
            (
                AppiumBy.ID,
                "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
            ),
            (AppiumBy.ID, "android:id/button1"),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Allow")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("While using the app")'),
        ]

        for _ in range(3):
            if not self.tap_first_if_visible(candidates, timeout_seconds=1):
                break

    def element_exists(self, locator: Locator) -> bool:
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
