# Client implementation

This folder provides two Python scripts to simulate TCP clients connecting to a server: `good_client_ilies.py` and `bad_client_ilies.py`. The `good_client_ilies.py` script simulates a good client that sends a properly formatted configuration file to the server. The `bad_client_ilies.py` script simulates a bad client that sends malicious input to try to crash the server.

Both scripts require an encrypted configuration file to be provided. The decrypted configuration files should be formatted with one piece of data per line, and each line should end with a newline character.

## Table of Contents

- [Files](#files)
- [Installation](#installation)
- [Usage](#usage)

## Files

The following Python files are included in this folder:

- `good_client_ilies.py`: A script that simulates a good client connecting to your server and sending correctly formatted inputs.
- `bad_client_ilies.py`: A script that simulates a bad client connecting to your server and sending malicious input to crash the server.
- `config_encryptor.py`: A script used to encrypt and decrypt configuration files.

The following configuration files are included in this folder:

- `good_client_ilies.cfg`: A configuration file containing data that a good client might send to your server.
- `bad_client_ilies.cfg`: A configuration file containing data that a malicious user might send to try to crash your server.

## Installation

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

The scripts in this folder were developed and tested using Python 3.8.10.

## Usage

### Good client

To use the `good_client_ilies.py` script, run:

```bash
python good_client_ilies.py [IP] [PORT] [ENCRYPTED_FILE]
```

Replace `[IP]` with the IP address of the server, `[PORT]` with the port number of the server, and `[ENCRYPTED_FILE]` with the path to the encrypted configuration file.

The `good_client_ilies.py` script reads the decrypted contents of the encrypted configuration file, which contains data that a good client might send to your server. The script then creates a TCP socket, connects to the server, sends data from the configuration file to the server, line by line, and prints the server's response for each line.

### Bad client

To use the `bad_client_ilies.py` script, run:

```bash
python bad_client_ilies.py [IP] [PORT] [ENCRYPTED_FILE]
```

Replace `[IP]` with the IP address of the server, `[PORT]` with the port number of the server, and `[ENCRYPTED_FILE]` with the path to the encrypted configuration file.

The `bad_client_ilies.py` script reads the decrypted contents of the encrypted configuration file, which contains data that a malicious user might send to try to crash your server. The script then creates a TCP socket, connects to the server, sends the malicious input to the server, and closes the connection.

### Config encryptor

To use the `config_encryptor.py` script, run:

```bash
python config_encryptor.py [OPERATION] [FILENAME]
```

Replace `[OPERATION]` with either `encrypt` or `decrypt`, depending on whether you want to encrypt or decrypt a file, and replace `[FILENAME]` with the name of the file you want to encrypt or decrypt.

When you run the script, it will prompt you to enter a passphrase. This passphrase will be used to encrypt or decrypt the file.
