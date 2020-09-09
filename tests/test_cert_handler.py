import unittest

from pathlib import Path

from cert_handler import CertHandler

test_file_location = Path.cwd().joinpath("pki")

def remove_test_files():
    import shutil
    shutil.rmtree(test_file_location)

class CertficateGenTestCase(unittest.TestCase):
    def test_certificate_not_none(self):
        key_file = CertHandler.generate_key("test_not_none", "test_not_none")

        self.assertIsNotNone(key_file, "Certificate file doesn't exist")

    def test_certificate_signing_request_not_none(self):
        key_file = CertHandler.generate_key("testuser", "testuser")

        csr_file = CertHandler.generate_certificate_signing_request("testuser_csr", "testuser", key_file)

        self.assertIsNotNone(csr_file, "Certificate Signing Request file doesn't exist")


if __name__ == '__main__':
    remove_test_files()
    unittest.main()
