import unittest

import os.path
from os import path

from cert_handler import CertHandler


class MyTestCase(unittest.TestCase):
    def test_certificate_generations(self):

        CertHandler.generate_key("testuser", "testtest")

        file_exists =

        self.

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
