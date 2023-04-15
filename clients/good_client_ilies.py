import argparse
import socket
import getpass
from config_encryptor import decrypt_data

def main():
    # Define the arguments that the script should accept
    parser = argparse.ArgumentParser(description='Connect to a server and send an encrypted config file.')
    parser.add_argument('ip', metavar='IP', type=str, help='The IP address of the server')
    parser.add_argument('port', metavar='PORT', type=int, help='The port number of the server')
    parser.add_argument('--encrypted_file', metavar='ENCRYPTED_FILE', type=str, help='The path to the encrypted config file', default='good_client_ilies.cfg')

    # Parse the arguments
    args = parser.parse_args()

    # Get the passphrase from the user (hidden)
    passphrase = getpass.getpass(prompt='Enter passphrase: ', stream=None)

    try:
        # Decrypt the file
        with open(args.encrypted_file, 'rb') as f:
            iv = f.read(16)
            ciphertext = f.read()
            tag = ciphertext[-16:]
            ciphertext = ciphertext[:-16]

        # Decrypt the data
        plaintext = decrypt_data(iv, ciphertext, tag, passphrase).decode()

        # Create a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the server
            s.connect((args.ip, args.port))

            # Send the decrypted config file to the server line by line
            for line in plaintext.splitlines():
                # Send a line to the server
                print(line)
                s.sendall(line.encode())

                # Receive the server's response
                response = s.recv(1024)

                # Print the server's response
                print(response.decode())

    except FileNotFoundError:
        print("Error: encrypted file not found.")
    except ValueError:
        print("Error: invalid port number.")
    except socket.gaierror:
        print("Error: could not connect to server. Check IP address and port number.")
    except ConnectionRefusedError:
        print("Error: connection refused by server.")
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    main()
