import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="module")
def driver_setup(request):
    service = Service("Resources/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(5)
    driver.get("http://todo.ly/")

    def teardown():
        driver.quit()

    request.addfinalizer(teardown)
    return driver


def test_verify_CRUD_project(driver_setup):
    driver = driver_setup

    # login
    driver.find_element(By.XPATH, "//img[contains(@src,'pagelogin')]").click()
    driver.find_element(By.ID, "ctl00_MainContent_LoginControl1_TextBoxEmail").send_keys("bootcamp@mojix44.com")
    driver.find_element(By.ID, "ctl00_MainContent_LoginControl1_TextBoxPassword").send_keys("12345")
    driver.find_element(By.ID, "ctl00_MainContent_LoginControl1_ButtonLogin").click()

    # Explicit Wait
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "ctl00_HeaderTopControl1_LinkButtonLogout")))

    assert driver.find_element(By.ID,
                               "ctl00_HeaderTopControl1_LinkButtonLogout").is_displayed(), "ERROR: login was incorrect"

    # create project
    name_project = "Mojix" + str(int(datetime.now().timestamp()))
    driver.find_element(By.XPATH, "//td[text()='Add New Project']").click()
    driver.find_element(By.ID, "NewProjNameInput").send_keys(name_project)
    driver.find_element(By.ID, "NewProjNameButton").click()
    time.sleep(1)
    actual_result = len(driver.find_elements(By.XPATH, "//td[text()='" + name_project + "']"))
    assert actual_result >= 1, "ERROR: The project was not created"

    # create task
    driver.find_element(By.ID, "NewItemContentInput").send_keys("Eynar")
    driver.find_element(By.ID, "NewItemAddButton").click()

    # update task
    task_element = driver.find_element(By.XPATH, "//div[@class='ItemContentDiv' and text()='Eynar']")
    task_element.click()
    driver.find_element(By.ID, "ItemEditTextbox").clear()
    driver.find_element(By.ID, "ItemEditTextbox").send_keys("Update\n")
    time.sleep(1)


# If you have more test functions, you can add them here in a similar format

if __name__ == "__main__":
    pytest.main([__file__])
