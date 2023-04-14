import socket
import logging
from concurrent.futures import ThreadPoolExecutor
from threading import Timer, Lock
from netsec.client import Client
from netsec.sanitizer import Sanitizer


class RelayServer:
    """
    Initialize the RelayServer with the given parameters.

    Args:
        ip_address (str): The IP address for the server.
        port (int): The port number for the server.
        max_clients (int): Maximum number of allowed clients.
        client_timeout (float): Time (in seconds) before a client is disconnected due to inactivity.
        response_timeout (float): Time (in seconds) before a request is considered failed.
        requests_per_minute (int): Limit on the number of requests per minute.

    Example:
    >>> relay_server = RelayServer("127.0.0.1", 8080, 10, 10.0, 10.0, 60)
    """

    def __init__(self, ip_address, port, max_clients, client_timeout, response_timeout, requests_per_minute):
        self.ip_address = ip_address
        self.port = port
        self.server_socket = None
        self.max_clients = max_clients
        self.client_timeout = client_timeout
        self.response_timeout = response_timeout
        self.requests_per_minute = requests_per_minute
        self.current_clients = 0
        self.lock = Lock()
        logging.info(f"RelayServer initialized with ip_address: {ip_address}, port: {port}, max_clients: {max_clients}, "
                     f"client_timeout: {client_timeout}, response_timeout: {response_timeout}, "
                     f"requests_per_minute: {requests_per_minute}")

    def send_data_to_end_server(self, o1, o2, i3, i4):
        """
        Send data to the end server.

        Connect to the IP address and port specified by i3 and i4, respectively, and send the data o1, o2, i3, and i4 in the format "{o1} {o2} {i3} {i4}\r\n".

        Args:
            o1 (float): The result of I1 / I2.
            o2 (int): The result of I1 ** I2.
            i3 (str): The IP address of the target end server.
            i4 (int): The port number of the target end server.

        Raises:
            Exception: If there is an error while sending the data to the end server.

        Example:
        >>> relay_server.send_data_to_end_server(2.5, 25, "127.0.0.1", 8081)
        """
        logging.info(f"Sending data to end server at {i3}:{i4}: {o1} {o2} {i3} {i4}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((i3, i4))
                sock.sendall(f"{o1} {o2} {i3} {i4}\r\n".encode())
                logging.info(f"Data sent to the end server at {i3}:{i4}: {o1} {o2} {i3} {i4}")
        except Exception as e:
            logging.error(f"Error while sending data to end server: {e}")
            raise

    # Process the request from a client, handle input validation, send data to end server, and handle errors
    def _process_request(self, client):
        """
        Process a request from the given client.

        Validate input, handle request processing, send data to the end server, and manage errors.

        Args:
            client (Client): The client object whose request needs to be processed.

        Example:
        >>> relay_server._process_request(client)
        """
        logging.info(f"Processing request for client {client.addr}")

        # Close the connection with the client,
        # optionally send a timeout message if the client has timed out
        def close_connection(timeout=False):
            try:
                if timeout:
                    client.conn.sendall("Timeout\r\n".encode())
                    logging.warning(f"Client timed out: {client.addr}")
            except OSError as e:
                logging.error(f"Error while sending data to client: {e}")
            finally:
                client.conn.close()
                self.current_clients -= 1
                logging.info(f"Connection closed for {client.addr}")

        # Start a timer to manage client inactivity timeouts
        def start_client_timer():
            timer = Timer(self.client_timeout, lambda: close_connection(timeout=True))
            timer.start()
            return timer
        
        # This method handles end server timeout for a client connection.
        def handle_end_server_timeout():
                response = "End server timeout\r\n"
                client.conn.sendall(response.encode())
                logging.warning(f"End server timeout for client {addr}")

        addr = client.addr
        logging.info(f"Connection accepted from {addr}")
        while True:
            client_timer = start_client_timer()
            response_timer = Timer(self.response_timeout, handle_end_server_timeout)
            try:
                data = client.conn.recv(1024)
                logging.debug(f"Data received from client {addr}: {data}")
                if client.check_request_limit(self.requests_per_minute):
                    client.conn.sendall("Request limit reached, try again later.\r\n".encode())
                    logging.warning(f"Request limit reached for client {addr}")
                    break
                client_timer.cancel()
                split_data = data.decode().split(" ")
                if len(split_data) != 4:
                    raise ValueError("Incorrect number of input arguments")

                i1, i2, i3, i4 = map(str.strip, split_data)
                i1, i2, i4 = float(i1), float(i2), int(i4)

                Sanitizer.validate_ip(i3)
                Sanitizer.validate_port(i4)
                
                o1, o2 = Sanitizer.validate_input(i1, i2)
                response_timer.start()
                self.send_data_to_end_server(o1, o2, i3, i4)
                response = "Success\r\n"
                logging.info(f"Successfully processed request for client {addr}")
            except ValueError as e:
                response = f"Invalid input value: {e}\r\n"
                logging.error(f"Invalid input value from {addr}: {e}")
            except OverflowError as e:
                response = f"Overflow error: {e}\r\n"
                logging.error(f"Overflow error from {addr}: {e}")
            except TimeoutError as e:
                response = f"Computation timeout error: {e}\r\n"
                logging.error(f"Computation timeout error from {addr}: {e}")
            except Exception as e:
                response = f"Error while processing request: {e}\r\n"
                logging.error(f"Error while processing request from {addr}: {e}")
            finally:
                response_timer.cancel()
                client.conn.sendall(response.encode())

        client_timer.cancel()
        close_connection(timeout=True)

    def start(self):
        """
        Start the RelayServer.

        Accept incoming connections, manage connection limits, and process client requests.

        Raises:
            PermissionError: If privileged access is required to bind the address.
            OSError: If there is an error while binding the address.

        Example:
        >>> relay_server.start()
        """
        Sanitizer.validate_ip(self.ip_address)
        Sanitizer.validate_port(self.port)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            try:
                server_socket.bind((self.ip_address, self.port))
            except PermissionError as e:
                error_msg = f"Permission error, privileged access required to bind the address {self.ip_address}:{self.port}: {e}"
                logging.error(f"Permission error, privileged access required to bind the address {self.ip_address}:{self.port}: {e}")
                print(error_msg)
                return
            except OSError as e:
                error_msg = f"Error while binding the address {self.ip_address}:{self.port}: {e}"
                logging.error(f"Error while binding the address {self.ip_address}:{self.port}: {e}")
                print(error_msg)
                return

            
            server_socket.listen(self.max_clients)
            self.server_socket = server_socket
            logging.info(f"Relay server started at {self.ip_address}:{self.port}")

            # Use ThreadPoolExecutor to handle multiple client connections concurrently
            with ThreadPoolExecutor() as executor:
                while True:
                    conn, addr = server_socket.accept()
                    logging.debug(f"Connection attempt from {addr}")
                    if self.current_clients < self.max_clients:
                        self.current_clients += 1
                        client = Client(conn, addr, self.client_timeout)
                        executor.submit(self._process_request, client)
                        logging.info(f"Accepted connection from {addr} and submitted for processing")
                    else:
                        conn.sendall("Connection limit reached, try again later.\r\n".encode())
                        conn.close()
                        logging.warning(f"Connection limit reached, denied connection from {addr}")
