class RailFenceCipher:
    def __init__(self):
        pass

    def rail_fence_encrypt(self, plain_text, num_rails):
        if num_rails <= 1:
            return plain_text

        # Tạo các hàng (rails)
        rails = ['' for _ in range(num_rails)]
        rail_index = 0
        direction = 1  # 1: xuống, -1: lên

        for char in plain_text:
            rails[rail_index] += char
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        # Ghép các hàng lại thành chuỗi mã hóa
        cipher_text = ''.join(rails)
        return cipher_text

    def rail_fence_decrypt(self, cipher_text, num_rails):
        if num_rails <= 1:
            return cipher_text

        # Bước 1: Xác định vị trí các ký tự sẽ nằm ở hàng nào theo thứ tự
        pattern = [0] * len(cipher_text)
        rail_index = 0
        direction = 1
        for i in range(len(cipher_text)):
            pattern[i] = rail_index
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        # Bước 2: Đếm số lượng ký tự mỗi hàng
        rail_counts = [pattern.count(r) for r in range(num_rails)]

        # Bước 3: Cắt cipher_text thành các phần tương ứng với từng rail
        rails = []
        idx = 0
        for count in rail_counts:
            rails.append(list(cipher_text[idx:idx+count]))
            idx += count

        # Bước 4: Duyệt lại theo pattern để lấy lại thứ tự ban đầu
        plain_text = ''
        rail_index = 0
        direction = 1
        for i in range(len(cipher_text)):
            plain_text += rails[pattern[i]].pop(0)

        return plain_text
