import time

class Client:
    """
    A class representing a client that can connect to a server and make requests.

    Attributes:
        conn (socket.socket): The socket connection object.
        addr (tuple): A tuple containing the IP address and port of the client.
        timeout (float): The timeout value for the client's connection.
        request_timestamps (List[float]): A list of timestamps representing the times when requests were made.
    """

    def __init__(self, conn, addr, timeout):
        """
        Initialize a Client object with the given parameters.

        Args:
            conn (socket.socket): The socket connection object.
            addr (tuple): A tuple containing the IP address and port of the client.
            timeout (float): The timeout value for the client's connection.
        """
        self.conn = conn
        self.addr = addr
        self.timeout = timeout
        self.request_timestamps = []

    def check_request_limit(self, requests_per_minute):
        """
        Check if the request limit per minute for the client has been reached.

        Args:
            requests_per_minute (int): The limit on the number of requests per minute.

        Returns:
            bool: True if the limit has been reached, False otherwise.
        """
        current_time = time.time()

        # Remove the timestamps that are older than one minute
        self.request_timestamps = [ts for ts in self.request_timestamps if current_time - ts <= 60]

        # Check if the request limit has been reached
        if len(self.request_timestamps) < requests_per_minute:
            self.request_timestamps.append(current_time)
            return False
        else:
            return True
