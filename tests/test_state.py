from __future__ import annotations

import pytest

from mobile_automation.test_data import unique_task_title
from screens.tasks_list_screen import TasksListScreen


@pytest.mark.android
@pytest.mark.state
@pytest.mark.regression
def test_created_task_persists_after_app_restart(driver, settings):
    task_title = unique_task_title("Persisted task")
    tasks = TasksListScreen(driver, settings).dismiss_initial_prompts().wait_until_ready()

    tasks.open_new_task().enter_title(task_title).save().assert_task_visible(task_title)
    tasks.restart_app().assert_task_visible(task_title)
