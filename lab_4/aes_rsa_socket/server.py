import socket
import threading
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# === Server Initialization ===
HOST = 'localhost'
PORT = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

# === Generate RSA Key Pair for Server ===
server_key = RSA.generate(2048)

# === Store Connected Clients ===
clients = []  # Each element: (client_socket, aes_key)


# === Utility Functions ===
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext


def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()


# === Client Handler ===
def handle_client(client_socket, client_address):
    print(f"[+] Connected with {client_address}")

    try:
        # Send server's public key
        client_socket.send(server_key.publickey().export_key(format='PEM'))

        # Receive client's public key
        client_received_key = RSA.import_key(client_socket.recv(2048))

        # Generate AES key and encrypt it with client's public RSA key
        aes_key = get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(client_received_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        client_socket.send(encrypted_aes_key)

        # Store the client and AES key
        clients.append((client_socket, aes_key))

        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break

            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print(f"[{client_address}] {decrypted_message}")

            # Broadcast to other clients
            for client, key in clients:
                if client != client_socket:
                    encrypted = encrypt_message(key, decrypted_message)
                    client.send(encrypted)

            if decrypted_message.strip().lower() == "exit":
                break

    except Exception as e:
        print(f"[!] Error with {client_address}: {e}")

    finally:
        # Remove client and close connection
        clients.remove((client_socket, aes_key))
        client_socket.close()
        print(f"[-] Connection with {client_address} closed")


# === Main Server Loop ===
print(f"[*] Server listening on {HOST}:{PORT}")
try:
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
except KeyboardInterrupt:
    print("\n[!] Server shutting down.")
    server_socket.close()
