from __future__ import annotations

import pytest

from mobile_automation.test_data import unique_task_title
from screens.tasks_list_screen import TasksListScreen


@pytest.mark.android
@pytest.mark.smoke
@pytest.mark.crud
def test_user_can_create_task(driver, settings):
    task_title = unique_task_title()
    tasks = TasksListScreen(driver, settings).dismiss_initial_prompts().wait_until_ready()

    tasks.open_new_task().enter_title(task_title).save().assert_task_visible(task_title)


@pytest.mark.android
@pytest.mark.crud
@pytest.mark.regression
def test_user_can_edit_task_title(driver, settings):
    original_title = unique_task_title("Original task")
    updated_title = unique_task_title("Updated task")
    tasks = TasksListScreen(driver, settings).dismiss_initial_prompts().wait_until_ready()

    tasks.open_new_task().enter_title(original_title).save().assert_task_visible(original_title)
    tasks.open_task(original_title).enter_title(updated_title).save().assert_task_visible(
        updated_title
    ).assert_task_not_visible(original_title)


@pytest.mark.android
@pytest.mark.crud
@pytest.mark.regression
def test_user_can_complete_task(driver, settings):
    task_title = unique_task_title("Complete task")
    tasks = TasksListScreen(driver, settings).dismiss_initial_prompts().wait_until_ready()

    tasks.open_new_task().enter_title(task_title).save().assert_task_visible(task_title)
    tasks.complete_task(task_title).wait_until_ready().assert_task_not_visible(task_title)
