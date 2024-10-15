from enum import Enum

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TaskStatus(Enum):
    ALL = "All"
    COMPLETED = "Completed"
    ACTIVE = "Active"

class TODOList:

    def __init__(self, driver):
        self.driver = driver
        self.driver_wait_click = WebDriverWait(self.driver, 10)


    def add_task(self, task_name: str):
        element = self.driver.find_element(By.CLASS_NAME, "new-todo")
        element.send_keys(task_name, Keys.ENTER)

    def get_tasks_count(self):
        tasks = self.driver.find_elements(By.XPATH, get_to_do_list_xpath())
        return tasks.__len__()

    def remove_task(self, index: int):
        task_xpath = get_task_xpath(index)
        task_element = self.driver.find_element(By.XPATH, task_xpath)

        delete_button_xpath = f"{task_xpath}/button"

        hover = ActionChains(self.driver).move_to_element(task_element)
        hover.perform()
        self.driver_wait_click.until(EC.element_to_be_clickable((By.XPATH, delete_button_xpath)))
        self.driver.find_element(By.XPATH, delete_button_xpath).click()

    def get_task_name(self, index: int):
        task_xpath = get_task_name_xpath(index)
        task_element = self.driver.find_element(By.XPATH, task_xpath)
        return task_element.text

    def toggle_task(self, index: int):
        task_xpath = f"{get_task_xpath(index)}/input"
        task_element = self.driver.find_element(By.XPATH, task_xpath)
        return task_element.click()

    def filter_items(self, task_status: TaskStatus):
        task_xpath = f"//ul[@class='filters']/li/a[text()='{task_status.value}']"
        task_element = self.driver.find_element(By.XPATH, task_xpath)
        task_element.click()

    def edit_task(self, index: int, new_name: str):
        task_xpath = get_task_name_xpath(index)
        task_element = self.driver.find_element(By.XPATH, task_xpath)
        action = ActionChains(self.driver)
        action.double_click(task_element).click_and_hold().send_keys(Keys.CLEAR, new_name, Keys.ENTER).perform()

    def toggle_all_tasks(self):
        element = self.driver.find_element(By.ID, "toggle-all-input")
        element.click()

def get_to_do_list_xpath():
    return "//ul[@class='todo-list']/li"

def get_task_xpath(index: int):
    index_as_string = f'[{index + 1}]' if index > 0 else ''
    return f"{get_to_do_list_xpath()}{index_as_string}/div"

def get_task_name_xpath(index: int):
    return f"{get_task_xpath(index)}/label"
