from time import sleep
import os
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from commitparser.parse_commit import parse_commit


def main(assignment, file):
    # Initialize chrom drive
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)

    # navigate to autolab
    driver.get('https://autograder.cse.buffalo.edu/auth/users/sign_in')

    # Log In
    driver.find_element(By.TAG_NAME, 'input').click()
    driver.find_element(By.NAME, 'j_username').send_keys(os.environ['UBIT_USERNAME'])
    driver.find_element(By.NAME, 'j_password').send_keys(os.environ['UBIT_PASSWORD'] + Keys.RETURN)

    # Wait for duo

    # Navigate to submission page, wait for duo
    x = 0
    while (driver.title != 'Autolab Home') and (x < 15):
        sleep(1)
        x += 1
    if x == 15:
        print('Error in Duo authentication')
        return
    driver.find_element(By.XPATH, f"//a[text()='{assignment}']").click()
    
    # Authorize AI
    driver.find_element(By.XPATH, "//form[@id='new_submission']/label").click()
    # Submit file
    driver.find_element(By.ID, 'submission_file').send_keys(f"{os.getcwd()}/{file}")
    print('Successfuly Submitted')
    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('commit')
    args = parser.parse_args()
    if ('UBIT_USERNAME' not in os.environ) or ('UBIT_PASSWORD' not in os.environ) or not os.environ['UBIT_USERNAME'] or not os.environ['UBIT_PASSWORD']:
        raise Exception('''Propper secrets/environment variables are not set.
You must have UBIT_USERNAME and UBIT_PASSWORD set as environment variables for this action.

ex:
- uses: actions/auto_lab
      env:
        UBIT_USERNAME: ${{ secrets.UBITUsername }}
        UBIT_PASSWORD: ${{ secrets.UBITPassword }}
''')
    info = parse_commit(args.commit)
    if not info:
        raise Exception('Not a submission Commit, start commit message with "submit " to submit: \nAdd if: startsWith(github.event.head_commit.message, "submit ") to this step in the action.yml')
    else:
        main(info[0], info[1])
