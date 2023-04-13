import unittest
from unittest.mock import Mock
import time
from netsec.client import Client

class TestClient(unittest.TestCase):

    def setUp(self):
        self.conn = Mock()
        self.addr = ('127.0.0.1', 12345)
        self.timeout = 5.0
        self.client = Client(self.conn, self.addr, self.timeout)

    def test_init(self):
        self.assertEqual(self.client.conn, self.conn)
        self.assertEqual(self.client.addr, self.addr)
        self.assertEqual(self.client.timeout, self.timeout)
        self.assertEqual(self.client.request_timestamps, [])

    def test_check_request_limit_under_limit(self):
        requests_per_minute = 5
        for _ in range(requests_per_minute - 1):
            self.client.request_timestamps.append(time.time())

        self.assertFalse(self.client.check_request_limit(requests_per_minute))

    def test_check_request_limit_reached_limit(self):
        requests_per_minute = 5
        for _ in range(requests_per_minute):
            self.client.request_timestamps.append(time.time())

        self.assertTrue(self.client.check_request_limit(requests_per_minute))

    def test_check_request_limit_old_requests_removed(self):
        requests_per_minute = 5
        old_time = time.time() - 70
        self.client.request_timestamps.append(old_time)

        for _ in range(requests_per_minute - 1):
            self.client.request_timestamps.append(time.time())

        self.assertFalse(self.client.check_request_limit(requests_per_minute))

if __name__ == '__main__':
    unittest.main()
