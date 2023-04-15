from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
import argparse
import sys
import getpass

def generate_key(passphrase):
    # Hash the passphrase using SHA256
    hash_object = SHA256.new(data=passphrase.encode())
    key = hash_object.digest()
    return key

def encrypt_data(data, passphrase):
    try:
        # Generate a key from the passphrase
        key = generate_key(passphrase)

        # Generate a random initialization vector (IV)
        iv = get_random_bytes(16)

        # Create an AES cipher in GCM mode with the generated key and IV
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)

        # Encrypt the data using the AES cipher
        ciphertext, tag = cipher.encrypt_and_digest(data)

        # Return the IV, ciphertext, and tag
        return iv, ciphertext, tag
    except Exception as e:
        print(f"Encryption failed: {e}", file=sys.stderr)
        sys.exit(1)

def decrypt_data(iv, ciphertext, tag, passphrase):
    try:
        # Generate a key from the passphrase
        key = generate_key(passphrase)

        # Create an AES cipher in GCM mode with the generated key and IV
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)

        # Decrypt the ciphertext and verify the tag using the AES cipher
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        # Return the plaintext
        return plaintext
    except Exception as e:
        print(f"Decryption failed: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # Define command line arguments using argparse
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a file using AES-GCM encryption.')
    parser.add_argument('operation', choices=['encrypt', 'decrypt'], help='the operation to perform (encrypt or decrypt)')
    parser.add_argument('filename', help='the filename of the input file')

    # Parse the command line arguments
    args = parser.parse_args()

    # Get the passphrase from the user (hidden)
    passphrase = getpass.getpass(prompt='Enter passphrase: ', stream=None)

    # Perform the requested operation
    if args.operation == 'encrypt':
        # Read the contents of the input file into memory
        with open(args.filename, 'rb') as f:
            data = f.read()

        # Encrypt the data
        iv, ciphertext, tag = encrypt_data(data, passphrase)

        # Write the IV, ciphertext, and tag to the original file
        with open(args.filename, 'wb') as f:
            f.write(iv)
            f.write(ciphertext)
            f.write(tag)

        print(f"File {args.filename} encrypted successfully.")
    elif args.operation == 'decrypt':
        # Read the IV, ciphertext, and tag from the input file
        with open(args.filename, 'rb') as f:
            iv = f.read(16)
            ciphertext = f.read()
            tag = ciphertext[-16:]
            ciphertext = ciphertext[:-16]

        # Decrypt the data
        plaintext = decrypt_data(iv, ciphertext, tag, passphrase)

        # Write the plaintext to the original file
        with open(args.filename, 'wb') as f:
            f.write(plaintext)

        print(f"File {args.filename} decrypted successfully.")

if __name__ == '__main__':
    main()
