from __future__ import annotations

from collections.abc import Iterable

from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

Locator = tuple[str, str]


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

    def invisible(self, locator: Locator) -> bool:
        return bool(
            WebDriverWait(self.driver, self.timeout_seconds).until(
                ec.invisibility_of_element_located(locator)
            )
        )

    def first_visible(self, locators: Iterable[Locator]) -> WebElement:
        locator_list = list(locators)

        def find_first_visible(driver: WebDriver) -> WebElement | bool:
            for locator in locator_list:
                try:
                    element = driver.find_element(*locator)
                    if element.is_displayed():
                        return element
                except (NoSuchElementException, StaleElementReferenceException):
                    continue
            return False

        return WebDriverWait(self.driver, self.timeout_seconds).until(
            find_first_visible,
            f"None of the locator candidates became visible: {locator_list}",
        )

    def first_clickable(self, locators: Iterable[Locator]) -> WebElement:
        locator_list = list(locators)

        def find_first_clickable(driver: WebDriver) -> WebElement | bool:
            for locator in locator_list:
                try:
                    element = driver.find_element(*locator)
                    if element.is_displayed() and element.is_enabled():
                        return element
                except (
                    ElementNotInteractableException,
                    NoSuchElementException,
                    StaleElementReferenceException,
                ):
                    continue
            return False

        return WebDriverWait(self.driver, self.timeout_seconds).until(
            find_first_clickable,
            f"None of the locator candidates became clickable: {locator_list}",
        )
