from captchaai_python import RecaptchaV2Task
from captchaai_python.utils import CaptchaAIException
import unittest


class RecaptchaV2TaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cpt = RecaptchaV2Task("apikey")
        self.cookies = "cookiename1=cookievalue1;cookiename2=cookievalue2"
        self.task_id = None
        return super().setUp()

    def test_create_task(self):
        try:
            self.task_id = self.cpt.create_task("https://www.google.com/recaptcha/api2/demo", "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-", self.cookies)
        except CaptchaAIException:
            self.fail("recaptcha v2 create task is failed!")

if __name__ == '__main__':
    unittest.main()