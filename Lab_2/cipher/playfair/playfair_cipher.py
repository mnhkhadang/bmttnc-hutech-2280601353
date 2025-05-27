class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.upper().replace("J", "I")
        key = "".join(dict.fromkeys(key))  # Loại bỏ ký tự trùng

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Bỏ chữ J
        for char in alphabet:
            if char not in key:
                key += char

        matrix = [list(key[i:i + 5]) for i in range(0, 25, 5)]
        return matrix

    def find_letter_coords(self, letter, matrix):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        return None, None  # Tránh lỗi nếu không tìm thấy

    def preprocess_plain_text(self, text):
        text = text.upper().replace("J", "I")
        result = ""
        i = 0
        while i < len(text):
            a = text[i]
            b = text[i + 1] if i + 1 < len(text) else 'X'

            if a == b:
                result += a + 'X'
                i += 1
            else:
                result += a + b
                i += 2

        if len(result) % 2 != 0:
            result += 'X'
        return result

    def playfair_encrypt(self, plain_text, matrix):
        plain_text = self.preprocess_plain_text(plain_text)
        encrypted_text = ""

        for i in range(0, len(plain_text), 2):
            a, b = plain_text[i], plain_text[i + 1]
            row1, col1 = self.find_letter_coords(a, matrix)
            row2, col2 = self.find_letter_coords(b, matrix)

            if row1 == row2:  # Cùng hàng
                encrypted_text += matrix[row1][(col1 + 1) % 5]
                encrypted_text += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:  # Cùng cột
                encrypted_text += matrix[(row1 + 1) % 5][col1]
                encrypted_text += matrix[(row2 + 1) % 5][col2]
            else:  # Khác hàng, khác cột
                encrypted_text += matrix[row1][col2]
                encrypted_text += matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):
            a, b = cipher_text[i], cipher_text[i + 1]
            row1, col1 = self.find_letter_coords(a, matrix)
            row2, col2 = self.find_letter_coords(b, matrix)

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]

        return self.clean_decrypted_text(decrypted_text)

    def clean_decrypted_text(self, text):
        # Loại bỏ các ký tự X được chèn vào nếu cần
        cleaned = ""
        i = 0
        while i < len(text):
            if i + 2 < len(text) and text[i] == text[i + 2] and text[i + 1] == 'X':
                cleaned += text[i]
                i += 2
            else:
                cleaned += text[i]
                i += 1
        if cleaned.endswith('X'):
            cleaned = cleaned[:-1]
        return cleaned
