from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException

from screens.base_screen import BaseScreen
from screens.task_editor_screen import TaskEditorScreen


class TasksListScreen(BaseScreen):
    READY_CANDIDATES = [
        (AppiumBy.ID, "org.tasks:id/body_empty"),
        (AppiumBy.ID, "org.tasks:id/fab"),
        (AppiumBy.ACCESSIBILITY_ID, "Create new task"),
        (AppiumBy.ACCESSIBILITY_ID, "New task"),
        (AppiumBy.ACCESSIBILITY_ID, "Add task"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Tasks")'),
    ]

    ADD_TASK_CANDIDATES = [
        (AppiumBy.ID, "org.tasks:id/fab"),
        (AppiumBy.ACCESSIBILITY_ID, "Create new task"),
        (AppiumBy.ACCESSIBILITY_ID, "New task"),
        (AppiumBy.ACCESSIBILITY_ID, "Add task"),
        (AppiumBy.ACCESSIBILITY_ID, "Add"),
    ]

    ONBOARDING_DISMISS_CANDIDATES = [
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Get started")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continue")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Next")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Skip")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Not now")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("No thanks")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continue without sync")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")'),
    ]

    TASK_TITLE_CANDIDATES_TEMPLATE = [
        'new UiSelector().text("{title}")',
        'new UiSelector().textContains("{title}")',
    ]

    def dismiss_initial_prompts(self) -> TasksListScreen:
        self.dismiss_common_system_dialogs()
        for _ in range(6):
            dismissed = self.tap_first_if_visible(
                self.ONBOARDING_DISMISS_CANDIDATES,
                timeout_seconds=1,
            )
            self.dismiss_common_system_dialogs()
            if not dismissed:
                break
        return self

    def wait_until_ready(self) -> TasksListScreen:
        self.waits.first_visible(self.READY_CANDIDATES)
        return self

    def open_new_task(self) -> TaskEditorScreen:
        self.tap_first(self.ADD_TASK_CANDIDATES)
        return TaskEditorScreen(self.driver, self.settings)

    def open_task(self, title: str) -> TaskEditorScreen:
        self.tap(self._task_title_locator(title))
        return TaskEditorScreen(self.driver, self.settings)

    def assert_task_visible(self, title: str) -> TasksListScreen:
        try:
            self.find_visible(self._task_title_locator(title))
        except TimeoutException as error:
            raise AssertionError(f"Expected task to be visible in task list: {title}") from error
        return self

    def task_is_visible(self, title: str) -> bool:
        return self.is_visible(self._task_title_locator(title), timeout_seconds=3)

    def _task_title_locator(self, title: str) -> tuple[str, str]:
        escaped_title = title.replace('"', '\\"')
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            self.TASK_TITLE_CANDIDATES_TEMPLATE[0].format(title=escaped_title),
        )
