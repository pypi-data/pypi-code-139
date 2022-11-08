import re
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Parser:
    def __init__(self, chrome_path, profile_path, sleep=10):
        self._html_body = ''
        self._sleep = sleep
        self._response_code = '0'
        self._search_result = []
        self._chrome_service = Service(chrome_path)
        self._chrome_options = webdriver.ChromeOptions()
        self._chrome_capabilities = DesiredCapabilities.CHROME.copy()

        self.set_chrome_options(profile_path)
        self.set_chrome_capabilities()

    def set_chrome_options(self, profile_path):
        self._chrome_options.add_argument('--allow-profiles-outside-user-dir')
        self._chrome_options.add_argument('--enable-profile-shortcut-manager')
        self._chrome_options.add_argument(f'user-data-dir={profile_path}')
        self._chrome_options.add_argument('--profile-directory=Default')

    def set_chrome_capabilities(self):
        self._chrome_capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

    def _parse(self, url):
        with webdriver.Chrome(service=self._chrome_service,
                              desired_capabilities=self._chrome_capabilities,
                              options=self._chrome_options) as driver:
            driver.get(url)
            self._get_response_code(driver.get_log('performance'))

            time.sleep(self._sleep)
            body = driver.page_source
            driver.quit()
            self._html_body = ''.join(body)

        return self

    def _get_response_code(self, logs):
        for log in logs:
            if log['message']:
                response_logs = json.loads(log['message'])
                try:
                    content_type = 'text/html' in response_logs['message']['params']['response']['headers'][
                        'content-type']
                    response_received = response_logs['message']['method'] == 'Network.responseReceived'
                    if content_type and response_received:
                        self._response_code = response_logs['message']['params']['response']['status']
                except:
                    pass

    def _regular_search(self, regular):
        self._search_result = re.findall(regular, self._html_body)

    def _put_html_to_file(self, path):
        with open(path, 'w+', encoding='utf-8') as file:
            file.write(self._html_body)

    def handle(self, url, regular):
        self._parse(url)._regular_search(regular)
        self._put_html_to_file(f'result.html')
        return self._search_result

    def json_handle(self, url, regular):
        results = self.handle(url, regular)
        data = {'status code': self._response_code, 'regular results': results}

        with open('result.json', 'w+', encoding='utf-8') as file:
            json.dump(data, file)
