from __future__ import annotations

import pytest

from mobile_automation.test_data import unique_task_title
from screens.tasks_list_screen import TasksListScreen


@pytest.mark.android
@pytest.mark.search
@pytest.mark.regression
def test_user_can_filter_tasks_by_search_query(driver, settings):
    target_title = unique_task_title("Search target")
    other_title = unique_task_title("Search other")
    tasks = TasksListScreen(driver, settings).dismiss_initial_prompts().wait_until_ready()

    tasks.open_new_task().enter_title(target_title).save().assert_task_visible(target_title)
    tasks.open_new_task().enter_title(other_title).save().assert_task_visible(other_title)

    tasks.search_for(target_title).assert_task_visible(target_title).assert_task_not_visible(
        other_title
    )
