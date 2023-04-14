import unittest
from netsec.utils import timeout
from netsec.sanitizer import Sanitizer

class TestSanitizer(unittest.TestCase):

    def test_validate_ip(self):
        self.assertIsNone(Sanitizer.validate_ip("127.0.0.1"))
        with self.assertRaises(ValueError):
            Sanitizer.validate_ip("invalid_ip")
        with self.assertRaises(ValueError):
            Sanitizer.validate_ip("224.0.0.1", check_specific_ips=True)
        with self.assertRaises(ValueError):
            Sanitizer.validate_ip("240.0.0.0", check_specific_ips=True)
        with self.assertRaises(ValueError):
            Sanitizer.validate_ip("0.0.0.0", check_specific_ips=True)

    def test_validate_port(self):
        self.assertIsNone(Sanitizer.validate_port(8080))
        with self.assertRaises(ValueError):
            Sanitizer.validate_port(0)
        with self.assertRaises(ValueError):
            Sanitizer.validate_port(65536)

    def test_validate_input(self):
        self.assertEqual(Sanitizer.validate_input(2.0, 3.0), (0.6666666666666666, 8.0))
        with self.assertRaises(ValueError):
            Sanitizer.validate_input(2.0, 0)
        with self.assertRaises(OverflowError):
            Sanitizer.validate_input(100000000, 1000000000)
        with self.assertRaises(ValueError):
            Sanitizer.validate_input(float('nan'), 1.0)

if __name__ == '__main__':
    unittest.main()
