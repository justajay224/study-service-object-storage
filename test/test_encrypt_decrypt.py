import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.encrypt_decrypt import encrypt_file, decrypt_file


def test_encryption():
    original_data = b"Contoh"
    password = "password-ku"

    # Enkripsi
    encrypted_data = encrypt_file(original_data, password)
    print(f"Encrypted (base64): {encrypted_data}")

    # Dekripsi
    decrypted_data = decrypt_file(encrypted_data, password)
    print(f"Decrypted: {decrypted_data}")

    # Verifikasi
    assert decrypted_data == original_data, "Data tidak sama"
    print("berhasil")

if __name__ == "__main__":
    test_encryption()

# def test_png_encryption():
#     # Baca file PNG
#     current_dir = os.path.dirname(__file__)
#     file_path = os.path.join(current_dir, "Screenshot_24.png")  # Jika file ada di folder test

#     with open(file_path, "rb") as f:
#         original_data = f.read()

#     password = "password-ku"

#     # Enkripsi
#     encrypted_data = encrypt_file(original_data, password)
    
#     # Dekripsi
#     decrypted_data = decrypt_file(encrypted_data, password)

#     # Simpan hasil dekripsi
#     with open("decrypted_Screenshot_24", "wb") as f:
#         f.write(decrypted_data)

#     # Verifikasi header PNG
#     png_header = decrypted_data[:8]
#     assert png_header == b"\x89PNG\r\n\x1a\n", "Header PNG tidak valid!"
#     print("File PNG valid!")

# if __name__ == "__main__":
#     test_png_encryption()