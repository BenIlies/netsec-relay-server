import argparse
import logging
from netsec import setup_logging
from netsec import read_config
from netsec.relay_server import RelayServer
from netsec.sanitizer import Sanitizer

def main():
    parser = argparse.ArgumentParser(description="Start Relay server.")
    parser.add_argument("--config", dest="config_path", default="server.cfg", help="Path to the configuration file (default: %(default)s)")
    parser.add_argument("--log", dest="log_file", default="log.txt", help="Path to the log file (default: %(default)s)")
    parser.add_argument("--verbose", action="store_true", help="Print logs instead of writing to a file")
    parser.add_argument("--log-level", choices=["info", "warning", "error"], help="Log level for output")
    parser.add_argument("--ip-address", dest="ip_address", help="IP address to bind to (overrides value in config file)")
    parser.add_argument("--port", type=int, help="Port number to bind to (overrides value in config file)")
    parser.add_argument("--max-clients", dest="max_clients", type=int, help="Maximum number of clients (overrides value in config file)")
    parser.add_argument("--client-timeout", dest="client_timeout", type=float, help="Client timeout in seconds (overrides value in config file)")
    parser.add_argument("--response-timeout", dest="response_timeout", type=float, help="Response timeout in seconds (overrides value in config file)")
    parser.add_argument("--requests-per-minute", dest="requests_per_minute", type=int, help="Maximum number of requests per minute (overrides value in config file)")
    args = parser.parse_args()

    # Configure logging based on command line arguments
    setup_logging(args)

    try:
        # Read configuration from the specified config file
        config = read_config(args.config_path)

        # Get ip_address
        ip_address = args.ip_address or config.get("RelayServer", "ip_address")
        Sanitizer.validate_ip(ip_address)

        # Get port
        port = args.port or config.getint("RelayServer", "port")
        Sanitizer.validate_port(port)

        # Get other configuration parameters
        max_clients = args.max_clients or config.getint("RelayServer", "max_clients", fallback=10)
        if not isinstance(max_clients, int) or max_clients < 0:
            raise ValueError("The maximum number of clients must be a non-negative integer")
        client_timeout = args.client_timeout or config.getfloat("RelayServer", "client_timeout", fallback=60.0)
        if client_timeout < 0:
            raise ValueError("The client timeout must be non-negative")
        response_timeout = args.response_timeout or config.getfloat("RelayServer", "response_timeout", fallback=10.0)
        if response_timeout < 0:
            raise ValueError("The response timeout must be non-negative")
        requests_per_minute = args.requests_per_minute or config.getint("RelayServer", "requests_per_minute", fallback=60)
        if not isinstance(requests_per_minute, int) or requests_per_minute < 0:
            raise ValueError("The maximum number of requests per minute must be a non-negative integer")

        # Create a RelayServer instance and start it
        relay_server = RelayServer(ip_address, port, max_clients, client_timeout, response_timeout, requests_per_minute)
        relay_server.start()

        print(f"Server started and listening on {ip_address}:{port}")

    except FileNotFoundError as e:
        logging.error(f"The configuration file {args.config_path} was not found: {str(e)}")
        print(f"Error: The configuration file {args.config_path} was not found. Please check the file path.")
    except ValueError as e:
        logging.error(str(e))
        print(f"Error: {str(e)}. Please check the validity of the IP address or port number.")
    except Exception as e:
        logging.error(str(e))
        print(f"An error occurred: {str(e)}.")


# Run the main function when the script is executed
if __name__ == "__main__":
    main()