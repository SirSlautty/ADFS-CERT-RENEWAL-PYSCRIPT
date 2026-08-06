import unittest
from unittest.mock import patch

import adfs_certificates


class CertificateToolTests(unittest.TestCase):
    def test_token_rotation_is_dry_run_by_default(self):
        with patch.object(adfs_certificates, "run_powershell") as runner:
            output = adfs_certificates.rotate_token_signing(False)
        runner.assert_not_called()
        self.assertIn("DRY RUN", output)

    def test_invalid_thumbprint_is_rejected(self):
        with self.assertRaises(ValueError):
            adfs_certificates.validate_ssl("not-a-thumbprint", False)


if __name__ == "__main__":
    unittest.main()
