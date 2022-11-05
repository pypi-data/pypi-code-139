import os

from random import random
from time import sleep

from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions, FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from super_eureka import logging

def create_driver() -> Chrome:
    user_data_dir = os.environ['CHROME_USER_DATA_DIR']
    profile_folder = os.environ['CHROME_PROFILE_FOLDER']
    
    options = ChromeOptions()
    options.add_argument(f'--user-data-dir={user_data_dir}')
    options.add_argument(f'--profile-folder={profile_folder}')
    options.headless = False

    driver = Chrome(executable_path='./chromedriver', options=options)
    return driver

def download_report(download_link: str) -> bool:
    logging.info('Downloading report...')

    driver = create_driver()
    driver.get(download_link)

    try:
        sign_w_google_link = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Sign in with Google']")))
        sleep(random() * 2.0 + 1.0)
        sign_w_google_link.click()
    except:
        logging.info('Could not find \'Sign in with Google\' button. Maybe the page took too long to load.')
        return False

    try:
        login_email = os.getenv('HUBSPOT_LOGIN_EMAIL')
        sign_in_email = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{login_email}')]")))
        sleep(random() * 2.0 + 1.0)
        sign_in_email.click()
    except:
        logging.info(f'Could not find the desired login email ({login_email}) to login. Maybe you don\'t have it currently on the browser storage or the page took too long to load.')
        return False

    sleep(60)
    driver.quit()
    return True
