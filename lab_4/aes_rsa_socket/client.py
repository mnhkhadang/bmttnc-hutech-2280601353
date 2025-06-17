import socket
import threading
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# === Connect to Server ===
HOST = 'localhost'
PORT = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# === Generate Client RSA Key Pair ===
client_key = RSA.generate(2048)

# === Exchange Keys ===
# Receive server's public key
server_public_key = RSA.import_key(client_socket.recv(2048))

# Send client's public key to the server
client_socket.send(client_key.publickey().export_key(format='PEM'))

# Receive encrypted AES key from server
encrypted_aes_key = client_socket.recv(2048)

# Decrypt AES key using client's private RSA key
cipher_rsa = PKCS1_OAEP.new(client_key)
aes_key = cipher_rsa.decrypt(encrypted_aes_key)


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


# === Receiving Thread ===
def receive_messages():
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print("Received:", decrypted_message)
        except Exception as e:
            print("[!] Error receiving message:", e)
            break


# === Start Receiver Thread ===
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# === Send Messages ===
try:
    while True:
        message = input("Enter message ('exit' to quit): ")
        encrypted_message = encrypt_message(aes_key, message)
        client_socket.send(encrypted_message)

        if message.strip().lower() == "exit":
            break
except KeyboardInterrupt:
    print("\n[!] Interrupted by user.")

# === Cleanup ===
client_socket.close()
print("[*] Connection closed.")
