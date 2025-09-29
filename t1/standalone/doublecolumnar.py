import sys
import numpy as np
import math
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
    print("Matriz Original")
    print(matrix)
    print()
    col = scramble(matrix, key, key_len)
    print("Embaralhado")
    print(col)
    print()
    col_transp = transpose_cols(col, key_len2)
    print("Transposto")
    print(col_transp)
    print()
    col_transp_col = scramble(col_transp, key2, key_len2)
    print("Embaralhado 2")
    print(col_transp_col)
    print()
    col_transp_col_transp = transpose_cols(col_transp_col, key_len2)
    print("Transposto 2 e Final:")
    print(col_transp_col_transp)
    print()

    return col_transp_col_transp


def reverse_double_transposition(matrix, key, key2, key_len, key_len2):
    reversed = reverse_transpose_cols(matrix, key_len2)
    print("Transposta Reversa")
    print(reversed)
    print()
    reversed = reverse_scramble(reversed, key2, key_len2)
    print("Desembaralhada")
    print(reversed)
    print()
    reversed = reverse_transpose_cols(reversed, key_len)
    print("Transposta Reversa 2")
    print(reversed)
    print()
    reversed = reverse_scramble(reversed, key, key_len)
    print("Desembaralhada 2 e final")
    print(reversed)
    print()

    return reversed


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


def encrypt_file(input_file, encrypted_file, key1, key2):
    print(f"Reading text from '{input_file}'...")
    text = read_text_file(input_file)
    
    if text is None:
        return False
    
    print(f"Original text length: {len(text)} characters")
    
    key_len = len(key1)
    key_len2 = len(key2)
    
    print("Encrypting...")
    matrix = string_to_matrix(text, key_len)
    encrypted_matrix = double_transposition(matrix, key1, key2, key_len, key_len2)
    
    print(f"Saving encrypted data to '{encrypted_file}'...")
    save_encrypted_simple(encrypted_matrix, encrypted_file)
    
    return True


def decrypt_file(encrypted_file, decrypted_file, key1, key2):
    print(f"Reading encrypted data from '{encrypted_file}'...")
    
    key_len = len(key1)
    key_len2 = len(key2)
    
    try:
        encrypted_matrix = load_encrypted_simple(encrypted_file, key_len2)
    except FileNotFoundError:
        print(f"Error: Encrypted file '{encrypted_file}' not found.")
        return False
    except Exception as e:
        print(f"Error loading encrypted file: {e}")
        return False
    
    print("Decrypting...")
    decrypted_matrix = reverse_double_transposition(encrypted_matrix, key1, key2, key_len, key_len2)
    decrypted_text = matrix_to_string(decrypted_matrix)
    
    print(f"Saving decrypted text to '{decrypted_file}'...")
    write_text_file(decrypted_file, decrypted_text)
    
    return True


#matrix = string_to_matrix(text, key_len)
#
#final = double_transposition(matrix, key, key2, key_len, key_len2)
#
#reversed = reverse_double_transposition(final, key, key2, key_len, key_len2)
#
#final_text = matrix_to_string(reversed)
#print(final_text)


def main():
    if len(sys.argv) != 4:
        print("Usage: uv run main.py <key> <key2> <path_to_txt>")
        sys.exit(1)

    key = sys.argv[1]
    key2 = sys.argv[2]
    name = sys.argv[3]

    encrypted_file = "encrypted_double.txt"
    decrypted_file = "decrypted_double.txt"

    dir_path = Path() / "livros"
    #name = input("Digite o nome do arquivo: ")
    if not name.endswith('.txt'):
            name += '.txt'
    book_path = dir_path / name

    success = encrypt_file(book_path, encrypted_file, key, key2)

    if not success:
        print("Criptografia falhou!")
        return

    print("Criptografia completa com sucesso!")
    print()

    success = decrypt_file(encrypted_file, decrypted_file, key, key2)

    if not success:
        print("Descriptografia falhou!")
        return

    print("Descriptografia completa com sucesso!")
    print()
    
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
    print()
    print("arquivos criados:")
    print(f"- input: {book_path}")
    print(f"- criptografado: {encrypted_file}")
    print(f"- descriptografado: {decrypted_file}")


if __name__ == "__main__":
    main()
