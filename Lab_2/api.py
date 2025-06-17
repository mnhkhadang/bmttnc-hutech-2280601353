from flask import Flask,request,  jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
app = Flask(__name__)
#Caesar Cipher algorithm
caesar_cipher = CaesarCipher()

@app.route("/api/caesar/encrypt", methods=['POST'])
def caesar_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({"encrypted_text": encrypted_text})

@app.route("/api/caesar/decrypt", methods=['POST'])
def caesar_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    return jsonify({"decrypted_text": decrypted_text})

# Vigenere Cipher algorithm
vigenere_cipher = VigenereCipher()
@app.route("/api/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
    return jsonify({"encrypted_text": encrypted_text})
@app.route("/api/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    data = request.json
    encrypted_text = data['cipher_text']
    key = data['key']
    decrypted_text = vigenere_cipher.vigenere_decrypt(encrypted_text, key)
    return jsonify({"decrypted_text": decrypted_text})

# Rail Fence Cipher algorithm
rail_fence_cipher = RailFenceCipher()
@app.route("/api/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = rail_fence_cipher.rail_fence_encrypt(plain_text, key)
    return jsonify({"encrypted_text": encrypted_text})
@app.route("/api/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = rail_fence_cipher.rail_fence_decrypt(cipher_text, key)
    return jsonify({"decrypted_text": decrypted_text})
# Playfair Cipher algorithm
playfair_cipher = PlayFairCipher()
@app.route("/api/playfair/creatematrix", methods=['POST'])
def playfair_create_matrix():
    data = request.json
    key = data['key']
    # Create the Playfair matrix using the provided key
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    return jsonify({"encrypted_text": playfair_matrix})
@app.route("/api/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted_text = playfair_cipher.playfair_encrypt(plain_text, playfair_matrix)
    return jsonify({"encrypted_text": encrypted_text})
@app.route("/api/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, playfair_matrix)
    return jsonify({"decrypted_text": decrypted_text})

#main function
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True, use_reloader=False)
