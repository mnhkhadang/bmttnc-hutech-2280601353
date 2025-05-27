from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Caesar cipher routes
@app.route('/caesar')
def caesar():
    return render_template('caesar.html')

@app.route('/caesar/encrypt', methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    Caesar = CaesarCipher()
    encrypt_text = Caesar.encrypt_text(text, key)
    return f"text: {text} <br/>key: {key} <br/>encrypted text: {encrypt_text}"

@app.route('/caesar/decrypt', methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    Caesar = CaesarCipher()
    decrypt_text = Caesar.decrypt_text(text, key)
    return f"text: {text} <br/>key: {key} <br/>decrypted text: {decrypt_text}"

# Vigenère cipher routes
@app.route('/vigenere')
def vigenere():
    return render_template('vigenere.html')

@app.route('/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    vigenere = VigenereCipher()
    encrypt_text = vigenere.vigenere_encrypt(text, key)
    return f"text: {text} <br/>key: {key} <br/>encrypted text: {encrypt_text}"

@app.route('/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    vigenere = VigenereCipher()
    decrypt_text = vigenere.vigenere_decrypt(text, key)
    return f"text: {text} <br/>key: {key} <br/>decrypted text: {decrypt_text}"

#rail fence cipher routes
@app.route('/railfence')
def railfence():
    return render_template('railfence.html')
@app.route('/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    from cipher.railfence import RailFenceCipher
    railfence = RailFenceCipher()
    encrypt_text = railfence.rail_fence_encrypt(text, key)  # <-- Đã sửa
    return f"text: {text} <br/>key: {key} <br/>encrypted text: {encrypt_text}"

@app.route('/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    from cipher.railfence import RailFenceCipher
    railfence = RailFenceCipher()
    decrypt_text = railfence.rail_fence_decrypt(text, key)
    return f"text: {text} <br/>key: {key} <br/>decrypted text: {decrypt_text}"  

@app.route('/playfair')
def playfair():
    return render_template('playfair.html')


@app.route('/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']

    if not text or not key:
        return "Please enter both plaintext and key.", 400

    cipher = PlayFairCipher()
    matrix = cipher.create_playfair_matrix(key)
    encrypted_text = cipher.playfair_encrypt(text, matrix)

    return f"text: {text} <br/>key: {key} <br/>encrypted text: {encrypted_text}"


@app.route('/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']

    if not text or not key:
        return "Please enter both ciphertext and key.", 400

    cipher = PlayFairCipher()
    matrix = cipher.create_playfair_matrix(key)
    decrypted_text = cipher.playfair_decrypt(text, matrix)

    return f"text: {text} <br/>key: {key} <br/>decrypted text: {decrypted_text}"
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
