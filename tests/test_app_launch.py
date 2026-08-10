from __future__ import annotations

import pytest

from screens.tasks_list_screen import TasksListScreen


@pytest.mark.android
@pytest.mark.smoke
def test_app_launches_to_tasks_list(driver, settings):
    tasks = TasksListScreen(driver, settings)

    tasks.dismiss_initial_prompts().wait_until_ready()

