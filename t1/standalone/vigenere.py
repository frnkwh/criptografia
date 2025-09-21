import sys

def encrypt_vigenere(text, key):
    key_len = len(key)
    encrypted_text = []

    for i, c in enumerate(text):
        key_letter = key[i % key_len]
        encrypted_char = (ord(c) + ord(key_letter)) % 0x110000
        encrypted_text.append(chr(encrypted_char))

    return "".join(encrypted_text)

def decrypt_vigenere(encrypted_text, key):
    key_len = len(key)
    decrypted_text = []

    for i, c in enumerate(encrypted_text):
        key_letter = key[i % key_len]
        decrypted_char = (ord(c) - ord(key_letter)) % 0x110000
        decrypted_text.append(chr(decrypted_char))

    return "".join(decrypted_text)

def encrypt_autokey(text, key):
    key_len = len(key)
    encrypted_text = []

    for i in range(key_len):
        key_letter = key[i]
        encrypted_char = (ord(text[i]) + ord(key_letter)) % 0x110000
        encrypted_text.append(chr(encrypted_char))

    for i, c in enumerate(text[key_len:]):
        key_letter = text[i]       
        encrypted_char = (ord(c) + ord(key_letter)) % 0x110000
        encrypted_text.append(chr(encrypted_char))

    return "".join(encrypted_text)

def decrypt_autokey(text, key):
    key_len = len(key)
    decrypted_text = []
    
    for i in range(key_len):
        key_letter = key[i % key_len]
        decrypted_char = (ord(text[i]) - ord(key_letter)) % 0x110000
        decrypted_text.append(chr(decrypted_char))

    for i, c in enumerate(text[key_len:], start=key_len):
        key_letter = decrypted_text[i - key_len]
        decrypted_char = (ord(c) - ord(key_letter)) % 0x110000
        decrypted_text.append(chr(decrypted_char))

    return "".join(decrypted_text)

def main():
    if len(sys.argv) != 3:
        print("Usage: uv run python main.py <key> <path_to_txt>")
        sys.exit(1)

    key = sys.argv[1]
    path = sys.argv[2]

    # 1. Read input text
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # 2. Encrypt
    encrypted_text = encrypt_autokey(text, key)
    with open("encrypted.txt", "w", encoding="utf-8") as f:
        f.write(encrypted_text)

    # 3. Decrypt
    decrypted_text = decrypt_autokey(encrypted_text, key)
    with open("decrypted.txt", "w", encoding="utf-8") as f:
        f.write(decrypted_text)

if __name__ == "__main__":
    main()

