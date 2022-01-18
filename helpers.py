from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

# Retrieve all months from date-picker and store in array.
def get_all_months(driver):
    dateDropdownOptions = Select(driver.find_element(
        By.XPATH, "//select[@class='ui-datepicker-month']")).options

    for i in range(len(dateDropdownOptions)):
        dateDropdownOptions[i] = dateDropdownOptions[i].text

    return dateDropdownOptions
