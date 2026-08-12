from __future__ import annotations

import pytest

from mobile_automation.test_data import unique_task_title
from screens.tasks_list_screen import TasksListScreen


@pytest.mark.android
@pytest.mark.navigation
@pytest.mark.regression
def test_user_can_return_from_task_editor_with_back(driver, settings):
    task_title = unique_task_title("Navigation task")
    tasks = TasksListScreen(driver, settings).dismiss_initial_prompts().wait_until_ready()

    tasks.open_new_task().enter_title(task_title).save().assert_task_visible(task_title)
    tasks.open_task(task_title).go_back_to_list().assert_task_visible(task_title)
