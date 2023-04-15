import argparse
import logging
from netsec import setup_logging
from netsec import read_config
from netsec.relay_server import RelayServer
from netsec.sanitizer import Sanitizer

def main():
    parser = argparse.ArgumentParser(description="Start Relay server.")
    parser.add_argument("--config", dest="config_file", default="server.cfg", help="path to config file")
    parser.add_argument("--log", dest="log_file", default="log.txt", help="path to log file")
    parser.add_argument("--verbose", action="store_true", help="print logs instead of writing to a file")
    parser.add_argument("--log-level", choices=["info", "warning", "error"], help="log level for output")
    args = parser.parse_args()

    # Configure logging based on command line arguments
    setup_logging(args)

    # Read configuration from the specified config file
    config = read_config(args.config_file)

    try:
        # Validate ip_address
        ip_address = config.get("RelayServer", "ip_address")
        Sanitizer.validate_ip(ip_address)

        # Validate port
        port = config.getint("RelayServer", "port")
        Sanitizer.validate_port(port)

        # Get other configuration parameters
        max_clients = config.getint("RelayServer", "max_clients", fallback=10)
        if not isinstance(max_clients, int) or max_clients < 0:
            raise ValueError("max_clients must be a non-negative integer")
        client_timeout = config.getint("RelayServer", "client_timeout", fallback=60)
        if client_timeout < 0:
            raise ValueError("client_timeout must be non-negative")
        response_timeout = config.getint("RelayServer", "response_timeout", fallback=10)
        if response_timeout < 0:
            raise ValueError("response_timeout must be non-negative")
        requests_per_minute = config.getint("RelayServer", "requests_per_minute", fallback=60)
        if not isinstance(requests_per_minute, int) or requests_per_minute < 0:
            raise ValueError("requests_per_minute must be a non-negative integer")

        # Create a RelayServer instance and start it
        relay_server = RelayServer(ip_address, port, max_clients, client_timeout, response_timeout, requests_per_minute)
        relay_server.start()
    except ValueError as e:
        logging.error(str(e))
        print(f"Configuration error: {str(e)}.")
    except Exception as e:
        logging.error(str(e))
        print(f"An error occurred: {str(e)}.")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
