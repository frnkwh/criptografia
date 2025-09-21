import sys
import numpy as np
import math
import time
from pathlib import Path

def string_to_matrix(text, key_len, pad=" "):
    text_len = len(text)
    if text_len % key_len != 0:
        extra = key_len - (text_len % key_len)
        text = text.ljust(text_len + extra, pad)

    arr = np.array(list(text)).reshape(-1, key_len)
    return arr

def matrix_to_string(matrix, pad=" "):
    flat = matrix.flatten()
    text = "".join(flat)

    return text

def insert_order(key):
    key_arr = np.array(list(key))
    sorted_idx = np.argsort(key_arr)

    return sorted_idx

def alphabetical_order(key, key_len):
    order = insert_order(key)
    ranks = np.empty_like(order)
    ranks[order] = np.arange(key_len)

    return ranks

def scramble(matrix, key, key_len):
    indices = insert_order(key)
    transposed = matrix[:, indices]

    return transposed

def reverse_scramble(matrix, key, key_len):
    forward = insert_order(key)
    inverse = np.argsort(forward)
    transposed = matrix[:, inverse]

    return transposed

def transpose_cols(matrix, key_len):
    transp = matrix.T
    flat = transp.flatten()
    size = math.ceil(flat.size / key_len)
    flat.resize(size, key_len)

    return flat

def reverse_transpose_cols(matrix, key_len):
    flat = matrix.flatten()
    while flat.size > 0 and flat[-1] == "":
        flat = flat[:-1]
    size = math.ceil(flat.size / key_len)
    flat = flat.copy()
    flat.resize(key_len, size)
    transp = flat.T

    return transp 

def double_transposition(matrix, key, key2, key_len, key_len2):
    col = scramble(matrix, key, key_len)
    col_transp = transpose_cols(col, key_len2)
    col_transp_col = scramble(col_transp, key2, key_len2)
    col_transp_col_transp = transpose_cols(col_transp_col, key_len2)

    return col_transp_col_transp

def reverse_double_transposition(matrix, key, key2, key_len, key_len2):
    reversed = reverse_transpose_cols(matrix, key_len2)
    reversed = reverse_scramble(reversed, key2, key_len2)
    reversed = reverse_transpose_cols(reversed, key_len)
    reversed = reverse_scramble(reversed, key, key_len)

    return reversed

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

def save_encrypted_simple(matrix, filename):
    text = matrix_to_string(matrix)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def load_encrypted_simple(filename, key_len2):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Calculate correct dimensions
    total_chars = len(text)
    rows = math.ceil(total_chars / key_len2)
    
    # Pad text to fit matrix dimensions
    expected_size = rows * key_len2
    if len(text) < expected_size:
        text = text.ljust(expected_size, ' ')
    
    return string_to_matrix(text, key_len2, pad=' ')

def read_text_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return None

def write_text_file(filename, content):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully wrote to '{filename}'")
    except Exception as e:
        print(f"Error writing to file '{filename}': {e}")

def format_time(seconds):
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f} μs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f} ms"
    elif seconds < 60:
        return f"{seconds:.3f} s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.3f}s"

def encrypt_file(input_file, encrypted_file, key1, key2):
    print(f"Reading text from '{input_file}'...")
    start_read = time.perf_counter()
    text = read_text_file(input_file)
    read_time = time.perf_counter() - start_read
    
    if text is None:
        return False, {}
    
    print(f"Original text length: {len(text)} characters")
    print(f"File read time: {format_time(read_time)}")
    
    key_len = len(key1)
    key_len2 = len(key2)
    
    print("Encrypting...")
    
    # Time autokey encryption
    start_encrypt = time.perf_counter()
    encrypted_vigenere = encrypt_autokey(text, key1)
    matrix = string_to_matrix(encrypted_vigenere, key_len)
    encrypted_matrix = double_transposition(matrix, key1, key2, key_len, key_len2)
    encrypt_time = time.perf_counter() - start_encrypt
    print(f"  Encryption: {format_time(encrypt_time)}")
    
    # Time file saving
    start_save = time.perf_counter()
    save_encrypted_simple(encrypted_matrix, encrypted_file)
    save_time = time.perf_counter() - start_save
    print(f"  File save: {format_time(save_time)}")
    
    timing_data = {
        'read_time': read_time,
        'encrypt_time': encrypt_time,
        'save_time': save_time,
    }
    
    print(f"Saving encrypted data to '{encrypted_file}'...")
    
    return True, timing_data

def decrypt_file(encrypted_file, decrypted_file, key1, key2):
    print(f"Reading encrypted data from '{encrypted_file}'...")
    
    key_len = len(key1)
    key_len2 = len(key2)
    
    # Time loading encrypted file
    start_load = time.perf_counter()
    try:
        encrypted_matrix = load_encrypted_simple(encrypted_file, key_len2)
    except FileNotFoundError:
        print(f"Error: Encrypted file '{encrypted_file}' not found.")
        return False, {}
    except Exception as e:
        print(f"Error loading encrypted file: {e}")
        return False, {}
    load_time = time.perf_counter() - start_load
    print(f"File load time: {format_time(load_time)}")
    
    print("Decrypting...")
    
    # Time reverse double transposition
    start_transpose = time.perf_counter()
    decrypted_matrix = reverse_double_transposition(encrypted_matrix, key1, key2, key_len, key_len2)
    transpose_time = time.perf_counter() - start_transpose
    print(f"  Reverse double transposition: {format_time(transpose_time)}")
    
    # Time matrix to string conversion
    start_matrix = time.perf_counter()
    decrypted_text = matrix_to_string(decrypted_matrix)
    matrix_time = time.perf_counter() - start_matrix
    print(f"  Matrix to string conversion: {format_time(matrix_time)}")
    
    # Time autokey decryption
    start_autokey = time.perf_counter()
    decrypted_vigenere = decrypt_autokey(decrypted_text, key1)
    autokey_time = time.perf_counter() - start_autokey
    print(f"  Autokey decryption: {format_time(autokey_time)}")
    
    # Time file saving
    start_save = time.perf_counter()
    write_text_file(decrypted_file, decrypted_vigenere)
    save_time = time.perf_counter() - start_save
    print(f"  File save: {format_time(save_time)}")
    
    total_decrypt_time = transpose_time + matrix_time + autokey_time
    
    timing_data = {
        'load_time': load_time,
        'transpose_time': transpose_time,
        'matrix_conversion_time': matrix_time,
        'autokey_decrypt_time': autokey_time,
        'save_time': save_time,
        'total_decrypt_time': total_decrypt_time
    }
    
    print(f"Total decryption time: {format_time(total_decrypt_time)}")
    print(f"Saving decrypted text to '{decrypted_file}'...")
    
    return True, timing_data

def print_performance_summary(encrypt_times, decrypt_times, text_length):
    """Print a comprehensive performance summary"""
    print("\n" + "="*60)
    print("PERFORMANCE SUMMARY")
    print("="*60)
    
    print(f"Text length: {text_length:,} characters")
    print(f"Processing rate (encryption): {text_length / encrypt_times['total_encrypt_time']:,.0f} chars/sec")
    print(f"Processing rate (decryption): {text_length / decrypt_times['total_decrypt_time']:,.0f} chars/sec")
    
    print(f"\nENCRYPTION BREAKDOWN:")
    print(f"  Autokey encryption:    {format_time(encrypt_times['autokey_encrypt_time']):>12} ({encrypt_times['autokey_encrypt_time']/encrypt_times['total_encrypt_time']*100:.1f}%)")
    print(f"  Matrix conversion:     {format_time(encrypt_times['matrix_conversion_time']):>12} ({encrypt_times['matrix_conversion_time']/encrypt_times['total_encrypt_time']*100:.1f}%)")
    print(f"  Double transposition:  {format_time(encrypt_times['transpose_time']):>12} ({encrypt_times['transpose_time']/encrypt_times['total_encrypt_time']*100:.1f}%)")
    print(f"  Total encryption:      {format_time(encrypt_times['total_encrypt_time']):>12}")
    
    print(f"\nDECRYPTION BREAKDOWN:")
    print(f"  Reverse transposition: {format_time(decrypt_times['transpose_time']):>12} ({decrypt_times['transpose_time']/decrypt_times['total_decrypt_time']*100:.1f}%)")
    print(f"  Matrix conversion:     {format_time(decrypt_times['matrix_conversion_time']):>12} ({decrypt_times['matrix_conversion_time']/decrypt_times['total_decrypt_time']*100:.1f}%)")
    print(f"  Autokey decryption:    {format_time(decrypt_times['autokey_decrypt_time']):>12} ({decrypt_times['autokey_decrypt_time']/decrypt_times['total_decrypt_time']*100:.1f}%)")
    print(f"  Total decryption:      {format_time(decrypt_times['total_decrypt_time']):>12}")
    
    total_crypto_time = encrypt_times['total_encrypt_time'] + decrypt_times['total_decrypt_time']
    print(f"\nTOTAL CRYPTOGRAPHIC TIME: {format_time(total_crypto_time)}")
    print("="*60)

def main():
    if len(sys.argv) != 4:
        print("Uso: uv run main.py <chave1> <chave2> <caminho_para_txt>")
        sys.exit(1)

    key = sys.argv[1]
    key2 = sys.argv[2]
    name = sys.argv[3]

    print(f"Starting cryptography performance test...")
    print(f"Key1: {key}")
    print(f"Key2: {key2}")
    print()

    # Normalize key lengths
    if len(key) != len(key2):
        max_len = max(len(key), len(key2))
        key = key.ljust(max_len, 'a')
        key2 = key2.ljust(max_len, 'a')
        print(f"Keys normalized to length {max_len}:")
        print(f"Key1: {key}")
        print(f"Key2: {key2}")
        print()

    encrypted_file = "encrypted.txt"
    decrypted_file = "decrypted.txt"

    dir_path = Path() / "livros"
    if not name.endswith('.txt'):
        name += '.txt'
    book_path = dir_path / name

    # Time the entire process
    total_start = time.perf_counter()

    # Encryption
    success, encrypt_times = encrypt_file(book_path, encrypted_file, key, key2)
    if not success:
        print("Criptografia falhou!")
        return

    print("Criptografia completa com sucesso!")
    print()

    # Decryption  
    success, decrypt_times = decrypt_file(encrypted_file, decrypted_file, key, key2)
    if not success:
        print("Descriptografia falhou!")
        return

    print("Descriptografia completa com sucesso!")
    print()

    total_time = time.perf_counter() - total_start

    # Verify correctness
    original_text = read_text_file(book_path)
    decrypted_text = read_text_file(decrypted_file)

    if original_text and decrypted_text:
        if original_text.strip() == decrypted_text.strip():
            print("Sucesso: texto original e descriptografado batem!")
        else:
            print("Erro: texto original e descriptografado não batem!")
            print(f"tamanho do original: {len(original_text)}")
            print(f"tamanho do descriptografado: {len(decrypted_text)}")

            min_len = min(len(original_text), len(decrypted_text))
            for i in range(min_len):
                if original_text[i] != decrypted_text[i]:
                    print(f"primeira diferença na posição {i}:")
                    print(f"  original: '{original_text[i]}' (ord: {ord(original_text[i])})")
                    print(f"  decrypted: '{decrypted_text[i]}' (ord: {ord(decrypted_text[i])})")
                    break

    # Performance summary
    if original_text:
        print_performance_summary(encrypt_times, decrypt_times, len(original_text))

    print()
    print("arquivos criados:")
    print(f"- input: {book_path}")
    print(f"- criptografado: {encrypted_file}")
    print(f"- descriptografado: {decrypted_file}")
    print(f"Total execution time: {format_time(total_time)}")

if __name__ == "__main__":
    main()
