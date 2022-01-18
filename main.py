#!/usr/bin/python3
from functions import *
from helpers import *

def main():
    web_driver = initialise_webdriver()
    
    fill_select_options(web_driver)
    select_date_input(web_driver)
    find_available_date(web_driver, list_of_months=get_all_months(web_driver))
    display_completion_time()

    web_driver.quit()

if __name__ == '__main__':
    main()