import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_Railfence  # Đảm bảo đúng tên file .ui đã chuyển đổi
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Railfence()
        self.ui.setupUi(self)

        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        plain_text = self.ui.txt_plain_text.toPlainText()
        key_text = self.ui.txt_key.toPlainText()

        # Kiểm tra và ép kiểu key
        try:
            key = int(key_text)
        except ValueError:
            self.show_error("Key must be an integer.")
            return

        url = "http://127.0.0.1:5001/api/railfence/encrypt"
        payload = {
            "plain_text": plain_text,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                encrypted_text = data.get("encrypted_text", "")
                self.ui.txt_cipher_text.setPlainText(encrypted_text)
                self.show_message("Encrypted Successfully")
            else:
                self.show_error(f"API error: {response.status_code}\n{response.text}")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Request Error: {str(e)}")

    def call_api_decrypt(self):
        cipher_text = self.ui.txt_cipher_text.toPlainText()
        key_text = self.ui.txt_key.toPlainText()

        # Kiểm tra và ép kiểu key
        try:
            key = int(key_text)
        except ValueError:
            self.show_error("Key must be an integer.")
            return

        url = "http://127.0.0.1:5001/api/railfence/decrypt"
        payload = {
            "cipher_text": cipher_text,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                decrypted_text = data.get("decrypted_text", "")
                self.ui.txt_plain_text.setPlainText(decrypted_text)
                self.show_message("Decrypted Successfully")
            else:
                self.show_error(f"API error: {response.status_code}\n{response.text}")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Request Error: {str(e)}")

    def show_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle("Success")
        msg.exec_()

    def show_error(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setWindowTitle("Error")
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
