from flask import Flask, render_template
import subprocess
import os
import sys

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/open_form/<cipher>")
def open_form(cipher):
    # Lấy đường dẫn thư mục hiện tại
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Mapping đúng các file nằm trong TEST/
    forms = {
        "caesar": os.path.join(base_dir, "caesar_cipher.py"),
        "railfence": os.path.join(base_dir, "railfence_cipher.py"),
        "playfair": os.path.join(base_dir, "playfair_cipher.py"),
        "vigenere": os.path.join(base_dir, "vigenere_cipher.py")
    }

    if cipher in forms and os.path.exists(forms[cipher]):
        try:
            print(f"🔄 Đang mở: {forms[cipher]}")
            subprocess.Popen([sys.executable, forms[cipher]])
        except Exception as e:
            print(f"❌ Lỗi khi chạy {cipher}: {e}")
    else:
        print(f"⚠️ File không tồn tại hoặc không hợp lệ: {cipher}")

    return ('', 204)

if __name__ == '__main__':
    print("🚀 Flask server đang chạy tại: http://127.0.0.1:5000")
    app.run(debug=True)
