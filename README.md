# NetSec Relay Server

A simple network security relay server that performs calculations and sanitizes input, ensuring safe communication with the end server.

## Table of Contents

- [TODO](#todo)
- [Assumptions](#assumptions)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Structure](#structure)
- [Testing](#testing)

## TODO

- [ ] Change the tests for the `relay_server`

## Assumptions

- IP addresses are considered correct only if they are in the format `x.x.x.x`, where `x` represents an integer between 0 and 255.

## Installation

To install the NetSec Relay Server, simply clone the repository and install any necessary dependencies.

```bash
git clone https://github.com/BenIlies/netsec-relay-server.git
```

## Usage

To start the relay server, run the following command:

```bash
python main.py [--config CONFIG_FILE] [--log LOG_FILE] [--verbose] [--log-level {info, warning, error}]
```

- `--config CONFIG_FILE`: Path to the configuration file (default: `config.ini`).
- `--log LOG_FILE`: Path to the log file (default: `log.txt`).
- `--verbose`: Print logs to the console instead of writing them to a file.
- `--log-level {info, warning, error}`: Log level for output (default: `error`).

## Configuration

Configure the relay server by modifying the `config.ini` file. The available options are:

```ini
[RelayServer]
ip_address = 127.0.0.1
port = 44444
max_clients = 10
client_timeout = 10
response_timeout = 10
requests_per_minute = 60
```

- `ip_address`: IP address for the relay server to bind to.
- `port`: Port number for the relay server to listen on.
- `max_clients`: Maximum number of clients that can connect to the relay server at the same time (optional).
- `client_timeout`: Timeout period in seconds for inactive clients to be disconnected (optional).
- `response_timeout`: Timeout period in seconds for the relay server to wait for a response from the end_server (optional).
- `requests_per_minute`: Maximum number of requests that a client can make per minute (optional).

## Structure

The following files make up the project:

- `main.py`: Entry point for starting the relay server.
- `config.ini`: Configuration file for the relay server settings.
- `netsec`:
  - `__init__.py`: Contains utility functions for setting up logging and reading the configuration file.
  - `client.py`: Defines the `Client` class for managing client connections and request limits.
  - `relayserver.py`: Defines the `RelayServer` class for managing client connections and handling requests.
  - `sanitizer.py`: Contains the `Sanitizer` class for validating and sanitizing user inputs.

## Testing

NetSec Relay Server has been designed with testing in mind, and provides a suite of automated tests that can be run to ensure that the server is functioning correctly. To run the tests, use the following command:

```bash
python -m unittest discover -s tests
```