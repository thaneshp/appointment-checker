import keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
from helpers import *
import time

CHROME_DRIVER_PATH = keys.DRIVER_PATH
TARGET_WEBSITE = keys.TARGET_WEBSITE

# Values to be used in pre-filling select elements.
FIRST_SELECT_ELEMENT_ID = 'jim'
SECOND_SELECT_ELEMENT_ID = 'urusan'
FIRST_SELECT_ELEMENT_VALUE = '4'
SECOND_SELECT_ELEMENT_VALUE = '6'

MONTH_INDEX_OFFSET = 1

# Function to initialise Chrome WebDriver.
def initialise_webdriver():
    service = Service(CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(TARGET_WEBSITE)
    
    return driver

# Function to pre-fill in first two select inputs.
def prefill_select_options(driver):
    Select(driver.find_element_by_id(FIRST_SELECT_ELEMENT_ID)
           ).select_by_value(FIRST_SELECT_ELEMENT_VALUE)
    time.sleep(3)
    Select(driver.find_element_by_id(SECOND_SELECT_ELEMENT_ID)
           ).select_by_value(SECOND_SELECT_ELEMENT_VALUE)

# Function to click on the date input.
def click_date_input(driver):
    dateInput = driver.find_element(By.XPATH, "//input[@id='from']")
    dateInput.click()

# Function to determine if given month has any available dates.
def find_available_date_in_month(driver, month_index, dateDropdownOptions):

    all_dates = driver.find_elements(
        By.XPATH, "//table[@class='ui-datepicker-calendar']//td/span | //table[@class='ui-datepicker-calendar']//td/a")

    todays_date = datetime.today()

    # Iterate through all dates to determine an available date.
    for date in all_dates:
        curr_date_str = "{date}/{month}/2022".format(date=date.text,month=month_index+MONTH_INDEX_OFFSET)
        curr_date = datetime.strptime(curr_date_str, "%d/%m/%Y")

        # Skip dates prior to today's date.
        if (curr_date.date() < todays_date.date()):
            continue

        # Determine if date is clickable.
        if (date.tag_name == 'a'):
            foundDate = dateDropdownOptions[month_index] + \
                " " + date.text + " " + "2022"
            return foundDate

    return False

# Function to find an available date given a list of months.
def find_available_date(driver, list_of_months):

    # Iterate through all months to determine if it contains an available date.
    for month_index in range(len(list_of_months)):
        # Click on the select option of the current month.
        Select(driver.find_element(
            By.XPATH, "//select[@class='ui-datepicker-month']")).select_by_value(str(month_index))

        if available_date := find_available_date_in_month(driver, month_index, list_of_months):
            alert_subscribers(available_date)
            break
        else:
            continue

# Function to send email and sms notification.
def alert_subscribers(available_date):

    send_email_alert(available_date)
    send_sms_alert(available_date)

# Function to display date & time the script completed.
def display_completion_time():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Completed at: ", dt_string)