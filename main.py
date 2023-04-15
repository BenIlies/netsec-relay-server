import argparse
from netsec import setup_logging
from netsec import read_config
from netsec.relay_server import RelayServer

# Define the main function
def main():
    # Set up command line argument parser
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
    ip_address = config.get("RelayServer", "ip_address")
    port = config.getint("RelayServer", "port")
    max_clients = config.getint("RelayServer", "max_clients", fallback=10)
    client_timeout = config.getfloat("RelayServer", "client_timeout", fallback=10.0)
    response_timeout = config.getfloat("RelayServer", "response_timeout", fallback=10.0)
    requests_per_minute = config.getint("RelayServer", "requests_per_minute", fallback=60)

    # Create a RelayServer instance and start it
    relay_server = RelayServer(ip_address, port, max_clients, client_timeout, response_timeout, requests_per_minute)
    relay_server.start()

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
