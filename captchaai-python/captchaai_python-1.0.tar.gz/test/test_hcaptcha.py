from captchaai_python import HCaptchaTask
from captchaai_python.utils import CaptchaAIException
import unittest


class HCaptchaTaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cpt = HCaptchaTask("apikey")
        self.cookies = "cookiename1=cookievalue1;cookiename2=cookievalue2"
        self.task_id = None
        return super().setUp()

    def test_create_task(self):
        try:
            self.task_id = self.cpt.create_task("https://lessons.zennolab.com/captchas/hcaptcha/?level=easy",
                "472fc7af-86a4-4382-9a49-ca9090474471", self.cookies)
        except CaptchaAIException:
            self.fail("hcaptchatask create task is failed!")

if __name__ == '__main__':
    unittest.main()