import unittest
from ipaddress import AddressValueError
from netsec.sanitizer import Sanitizer

class TestSanitizer(unittest.TestCase):
    def test_validate_ip(self):
        # Test valid IP address
        valid_ip = "192.168.1.1"
        self.assertIsNone(Sanitizer.validate_ip(valid_ip))

        # Test invalid IP address
        invalid_ips = ["256.256.256.256", "192.168.1", "192.168.1.1.1"]
        for ip in invalid_ips:
            with self.assertRaises(ValueError):
                Sanitizer.validate_ip(ip)

        # Test multicast, reserved, and unspecified IP addresses
        special_ips = ["224.0.0.1", "240.0.0.1", "0.0.0.0"]
        for ip in special_ips:
            with self.assertRaises(ValueError):
                Sanitizer.validate_ip(ip)

    def test_validate_port(self):
        # Test valid port
        valid_port = 8080
        self.assertIsNone(Sanitizer.validate_port(valid_port))

        # Test invalid ports
        invalid_ports = [-1, 0, 65536, 70000]
        for port in invalid_ports:
            with self.assertRaises(ValueError):
                Sanitizer.validate_port(port)

    def test_validate_input(self):
        # Test valid input
        valid_input = (2, 3)
        self.assertIsNone(Sanitizer.validate_input(*valid_input))

        # Test division by zero
        div_by_zero = (5, 0)
        with self.assertRaises(ValueError):
            Sanitizer.validate_input(*div_by_zero)

        # Test second input value too large
        large_input = (2, 10001)
        with self.assertRaises(ValueError):
            Sanitizer.validate_input(*large_input)

if __name__ == '__main__':
    unittest.main()
