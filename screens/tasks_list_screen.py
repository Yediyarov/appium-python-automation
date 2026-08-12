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

    SEARCH_BUTTON_CANDIDATES = [
        (AppiumBy.ID, "org.tasks:id/menu_search"),
        (AppiumBy.ACCESSIBILITY_ID, "Search"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Search")'),
    ]

    SEARCH_FIELD_CANDIDATES = [
        (AppiumBy.ID, "org.tasks:id/search_src_text"),
        (AppiumBy.CLASS_NAME, "android.widget.AutoCompleteTextView"),
    ]

    ONBOARDING_DISMISS_CANDIDATES = [
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continue without sync")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Get started")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continue")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Next")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Skip")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Not now")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("No thanks")'),
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
        return TaskEditorScreen(self.driver, self.settings).wait_until_ready()

    def open_task(self, title: str) -> TaskEditorScreen:
        self.tap(self._task_title_locator(title))
        return TaskEditorScreen(self.driver, self.settings).wait_until_ready()

    def complete_task(self, title: str) -> TasksListScreen:
        self.tap(self._task_complete_box_locator(title))
        return self

    def search_for(self, query: str) -> TasksListScreen:
        self.tap_first(self.SEARCH_BUTTON_CANDIDATES)
        search_field = self.waits.first_visible(self.SEARCH_FIELD_CANDIDATES)
        search_field.click()
        search_field.clear()
        search_field.send_keys(query)
        return self

    def assert_task_visible(self, title: str) -> TasksListScreen:
        try:
            self.find_visible(self._task_title_locator(title))
        except TimeoutException as error:
            raise AssertionError(f"Expected task to be visible in task list: {title}") from error
        return self

    def assert_task_not_visible(self, title: str) -> TasksListScreen:
        if not self.waits.invisible(self._task_title_locator(title)):
            raise AssertionError(f"Expected task to be hidden from task list: {title}")
        return self

    def task_is_visible(self, title: str) -> bool:
        return self.is_visible(self._task_title_locator(title), timeout_seconds=3)

    def _task_title_locator(self, title: str) -> tuple[str, str]:
        escaped_title = title.replace('"', '\\"')
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            self.TASK_TITLE_CANDIDATES_TEMPLATE[0].format(title=escaped_title),
        )

    def _task_complete_box_locator(self, title: str) -> tuple[str, str]:
        return (
            AppiumBy.XPATH,
            "//android.widget.TextView"
            f"[@resource-id='org.tasks:id/title' and @text={self._xpath_literal(title)}]"
            "/parent::android.widget.RelativeLayout"
            "/android.widget.ImageView[@resource-id='org.tasks:id/completeBox']",
        )

    @staticmethod
    def _xpath_literal(value: str) -> str:
        if "'" not in value:
            return f"'{value}'"

        if '"' not in value:
            return f'"{value}"'

        parts = value.split("'")
        return "concat(" + ', "\"\'\"", '.join(f"'{part}'" for part in parts) + ")"
