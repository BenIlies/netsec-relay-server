import logging
import configparser
import os

# Set up the logging configuration.
def setup_logging(args):
    """
    Set up the logging configuration with the provided arguments.

    Args:
        args: A namespace object with the command-line arguments.

    Example:
    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument("--log_level", choices=["info", "warning", "error"], help="Set log level")
    >>> parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    >>> parser.add_argument("--log_file", default="log.txt", help="Set log file name")
    >>> args = parser.parse_args()
    >>> setup_logging(args)
    """
    log_levels = {
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
    }
    log_level = log_levels[args.log_level] if args.log_level else logging.ERROR
    if args.verbose:
        logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")
    else:
        logging.basicConfig(filename=args.log_file, level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

# Read the configuration file.
def read_config(config_file):
    """
    Read the configuration file and return the configuration object.

    Args:
        config_file (str): The path to the configuration file.

    Raises:
        FileNotFoundError: If the configuration file is not found.

    Returns:
        configparser.ConfigParser: The configuration object.

    Example:
    >>> config = read_config("config.ini")
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file '{config_file}' not found")
    config = configparser.ConfigParser()
    config.read(config_file)
    return config
