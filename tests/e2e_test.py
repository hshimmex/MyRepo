import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from objects.todo import TODOList, TaskStatus


@pytest.fixture(autouse=True)
def todo_object():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Overcome limited resource problems
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://todomvc.com/examples/vue/dist/#/")
    todo_object = TODOList(driver)
    yield todo_object
    driver.quit()

def test_add_item(todo_object):
    todo_object.add_task("Interview")
    assert todo_object.get_tasks_count() == 1
    todo_object.add_task("Interview2")
    assert todo_object.get_tasks_count() == 2


def test_remove_item(todo_object):
    todo_object.add_task("Interview")
    todo_object.add_task("Interview2")
    todo_object.remove_task(1)
    assert todo_object.get_tasks_count() == 1
    assert todo_object.get_task_name(0) == "Interview"


def test_filter(todo_object):
    todo_object.add_task("Interview")
    todo_object.add_task("Interview1")
    todo_object.add_task("Interview2")
    todo_object.toggle_task(0)
    todo_object.filter_items(TaskStatus.COMPLETED)
    assert todo_object.get_tasks_count() == 1
    assert todo_object.get_task_name(0) == "Interview"
    todo_object.toggle_task(0)
    assert todo_object.get_tasks_count() == 0
    todo_object.filter_items(TaskStatus.ALL)
    assert todo_object.get_tasks_count() == 3
    assert todo_object.get_task_name(0) == "Interview"
    assert todo_object.get_task_name(1) == "Interview1"
    assert todo_object.get_task_name(2) == "Interview2"
    todo_object.toggle_task(1)
    todo_object.filter_items(TaskStatus.ACTIVE)
    assert todo_object.get_tasks_count() == 2
    assert todo_object.get_task_name(0) == "Interview"
    assert todo_object.get_task_name(1) == "Interview2"

def test_edit_task(todo_object):
    todo_object.add_task("Interview")
    todo_object.add_task("Interview1")
    todo_object.add_task("Interview2")
    todo_object.edit_task(0, "edited_interview")
    assert todo_object.get_task_name(0) == "edited_interview"
    todo_object.toggle_task(1)
    todo_object.edit_task(1, "edited_interview1")
    assert todo_object.get_task_name(1) == "edited_interview1"
    todo_object.filter_items(TaskStatus.COMPLETED)
    assert todo_object.get_tasks_count() == 1
    assert todo_object.get_task_name(0) == "edited_interview1"

def test_toggle_tasks(todo_object,):
    todo_object.add_task("Interview")
    todo_object.add_task("Interview1")
    todo_object.add_task("Interview2")
    todo_object.toggle_all_tasks()
    todo_object.filter_items(TaskStatus.COMPLETED)
    assert todo_object.get_tasks_count() == 3
    todo_object.toggle_all_tasks()
    todo_object.filter_items(TaskStatus.COMPLETED)
    assert todo_object.get_tasks_count() == 0
    todo_object.filter_items(TaskStatus.ACTIVE)
    assert todo_object.get_tasks_count() == 3
    todo_object.toggle_all_tasks()
    todo_object.filter_items(TaskStatus.COMPLETED)
    assert todo_object.get_tasks_count() == 3


