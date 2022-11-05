#
# Copyright © 2012–2022 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""Captcha tests."""

from unittest import TestCase

from weblate.accounts.captcha import MathCaptcha


class CaptchaTest(TestCase):
    def test_object(self):
        captcha = MathCaptcha("1 * 2")
        self.assertFalse(captcha.validate(1))
        self.assertTrue(captcha.validate(2))
        restored = MathCaptcha.unserialize(captcha.serialize())
        self.assertEqual(captcha.question, restored.question)
        self.assertTrue(restored.validate(2))

    def test_generate(self):
        """Test generating of captcha for every operator."""
        captcha = MathCaptcha()
        for operator in MathCaptcha.operators:
            captcha.operators = (operator,)
            self.assertIn(operator, captcha.generate_question())
