import os
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from .consts import ENV_KEY, USER_AGENT


def chrofile(headless:bool=True, size='1920,1200')->webdriver.Chrome:
  options = Options()

  profile_dir = os.getenv(ENV_KEY)
  if profile_dir and os.path.exists(profile_dir):
    options.add_argument(f'--profile-directory={os.path.basename(profile_dir)}')
    options.add_argument(f'--user-data-dir={os.path.dirname(profile_dir)}')
  if headless: options.add_argument('--headless')
  
  options.add_argument(f'user-agent={USER_AGENT}')
  options.add_argument(f'--window-size={size}')

  chromedriver_autoinstaller.install()
  return webdriver.Chrome(options=options)


