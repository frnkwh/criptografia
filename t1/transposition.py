import numpy as np

text = "TRANSPOSITIONCIPHERSSCRAMBLELETTERSLIKEPUZZLEPIECESTOCREATEANINDECIPHERABLEARRANGEMENT"
key = "JANEAUSTEN"
#text = "123456123456123456123456123456123456"
#key = "zebras"
key_len = len(key)

def string_to_matrix(text, key_len, pad=" "):
    text_len = len(text)
    if text_len % key_len != 0:
        extra = key_len - (text_len % key_len)
        text = text.ljust(text_len + extra, pad)

    arr = np.array(list(text)).reshape(-1, key_len)
    return arr

def alphabetical_order(key):
    sorted_key = sorted([(char, i) for i, char in enumerate(key)])
    print(sorted_key)

    order = [0] * len(key)
    for rank, (_, i) in enumerate(sorted_key):
        order[i] = rank
    return order

def columnar_transposition(matrix, key, key_len):
    new_order = alphabetical_order(key)
    zipped = np.column_stack((np.arange(key_len), new_order))
    sorted_zipped = zipped[zipped[:, 1].argsort()]
    indices = sorted_zipped[:, 0]
    transposed = matrix[:, indices]

    return transposed

#nao funciona ainda, tem que trocar essa funcao inteira
def transpose_fixed_cols(matrix, key_len):
    flat = matrix.flatten()
    result = [flat[i:i + key_len] for i in range(0, len(flat), key_len)]
    return result

matrix = string_to_matrix(text, key_len)
print("Matriz Original")
print(matrix)

transposed = columnar_transposition(matrix, key, key_len)
print("Transposto Colunarmente")
print(transposed)

transposed = transpose_fixed_cols(transposed, len("AEROPLANES"))
print(transposed)
double = columnar_transposition(transposed, "AEROPLANES", len("AEROPLANES"))
print("Transposto Duplamente Colunarmente")
print(double)

