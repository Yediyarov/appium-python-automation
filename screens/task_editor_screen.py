from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from screens.base_screen import BaseScreen


class TaskEditorScreen(BaseScreen):
    TITLE_FIELD_CANDIDATES = [
        (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.EditText").instance(0)',
        ),
        (AppiumBy.CLASS_NAME, "android.widget.EditText"),
    ]

    SAVE_CANDIDATES = [
        (AppiumBy.ACCESSIBILITY_ID, "Save"),
        (AppiumBy.ID, "org.tasks:id/menu_save"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Save")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Save")'),
    ]

    COMPLETE_CANDIDATES = [
        (AppiumBy.ACCESSIBILITY_ID, "Complete"),
        (AppiumBy.ACCESSIBILITY_ID, "Mark complete"),
        (AppiumBy.ID, "org.tasks:id/complete"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Complete")'),
    ]

    DELETE_CANDIDATES = [
        (AppiumBy.ACCESSIBILITY_ID, "Delete task"),
        (AppiumBy.ACCESSIBILITY_ID, "Delete"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Delete task")'),
        (AppiumBy.ID, "org.tasks:id/menu_delete"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Delete")'),
    ]

    CONFIRM_DELETE_CANDIDATES = [
        (AppiumBy.ID, "android:id/button1"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Delete")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")'),
    ]

    def wait_until_ready(self) -> TaskEditorScreen:
        self.waits.first_visible(self.TITLE_FIELD_CANDIDATES)
        return self

    def enter_title(self, title: str) -> TaskEditorScreen:
        title_field = self.waits.first_visible(self.TITLE_FIELD_CANDIDATES)
        title_field.click()
        title_field.clear()
        title_field.send_keys(title)
        return self

    def save(self):
        self.tap_first(self.SAVE_CANDIDATES)
        from screens.tasks_list_screen import TasksListScreen

        return TasksListScreen(self.driver, self.settings)

    def complete(self):
        self.tap_first(self.COMPLETE_CANDIDATES)
        from screens.tasks_list_screen import TasksListScreen

        return TasksListScreen(self.driver, self.settings)

    def delete(self):
        self.tap_first(self.DELETE_CANDIDATES)
        self.tap_first_if_visible(self.CONFIRM_DELETE_CANDIDATES, timeout_seconds=3)
        from screens.tasks_list_screen import TasksListScreen

        return TasksListScreen(self.driver, self.settings)
