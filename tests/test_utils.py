import unittest
import time
from unittest.mock import patch
from netsec.utils import timeout

class TestTimeoutDecorator(unittest.TestCase):
    def test_timeout_decorator(self):
        @timeout(1.0)
        def my_function():
            time.sleep(2.0)

        with self.assertRaises(TimeoutError):
            my_function()

    def test_timeout_decorator_with_result(self):
        @timeout(1.0)
        def my_function():
            return 42

        result = my_function()
        self.assertEqual(result, 42)

    def test_timeout_decorator_with_args_and_kwargs(self):
        @timeout(1.0)
        def my_function(x, y, z=None):
            return x + y + (z or 0)

        result = my_function(1, 2, z=3)
        self.assertEqual(result, 6)

    def test_timeout_decorator_with_mocked_sleep(self):
        with patch('time.sleep', side_effect=Exception('Sleep called')):
            @timeout(1.0)
            def my_function():
                time.sleep(2.0)

            with self.assertRaises(TimeoutError):
                my_function()
