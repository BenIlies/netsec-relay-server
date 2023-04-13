import unittest
from netsec.relay_server import RelayServer


class TestRelayServer(unittest.TestCase):

    def setUp(self):
        self.relay_server = RelayServer("127.0.0.1", 8080, 2, 10.0, 10.0, 60)

    def test_init(self):
        self.assertEqual(self.relay_server.ip_address, "127.0.0.1")
        self.assertEqual(self.relay_server.port, 8080)
        self.assertEqual(self.relay_server.max_clients, 2)
        self.assertEqual(self.relay_server.client_timeout, 10.0)
        self.assertEqual(self.relay_server.response_timeout, 10.0)
        self.assertEqual(self.relay_server.requests_per_minute, 60)

    def test_send_data_to_end_server(self):
        pass

    def test_process_request(self):
        pass

    def test_start(self):
        pass


if __name__ == "__main__":
    unittest.main()
