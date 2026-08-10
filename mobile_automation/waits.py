from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

Locator = tuple[str, str]
T = TypeVar("T")


class Waits:
    def __init__(self, driver: WebDriver, timeout_seconds: int) -> None:
        self.driver = driver
        self.timeout_seconds = timeout_seconds

    def visible(self, locator: Locator) -> WebElement:
        return WebDriverWait(self.driver, self.timeout_seconds).until(
            ec.visibility_of_element_located(locator)
        )

    def clickable(self, locator: Locator) -> WebElement:
        return WebDriverWait(self.driver, self.timeout_seconds).until(
            ec.element_to_be_clickable(locator)
        )

    def first_visible(self, locators: Iterable[Locator]) -> WebElement:
        last_error: TimeoutException | NoSuchElementException | None = None
        for locator in locators:
            try:
                return self.visible(locator)
            except (TimeoutException, NoSuchElementException) as error:
                last_error = error

        raise TimeoutException(
            f"None of the locator candidates became visible: {locators}"
        ) from last_error

    def first_clickable(self, locators: Iterable[Locator]) -> WebElement:
        last_error: TimeoutException | NoSuchElementException | None = None
        for locator in locators:
            try:
                return self.clickable(locator)
            except (TimeoutException, NoSuchElementException) as error:
                last_error = error

        raise TimeoutException(
            f"None of the locator candidates became clickable: {locators}"
        ) from last_error
