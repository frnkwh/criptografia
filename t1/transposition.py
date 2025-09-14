import numpy as np
import math

#text = "TRANSPOSITIONCIPHERSSCRAMBLELETTERSLIKEPUZZLEPIECESTOCREATEANINDECIPHERABLEARRANGEMENT"
#key = "JANEAUSTEN"
#key2 = "AEROPLANES"
text = "abcdefghijklmnop"
key = "zebr"
key2 = "milen"
key_len = len(key)
key_len2 = len(key2)
def string_to_matrix(text, key_len, pad=" "):
    text_len = len(text)
    if text_len % key_len != 0:
        extra = key_len - (text_len % key_len)
        text = text.ljust(text_len + extra, pad)

    arr = np.array(list(text)).reshape(-1, key_len)
    return arr

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
    #indices = alphabetical_order(key, key_len)
    #transposed = matrix[:, indices]

    #return transposed

    forward = insert_order(key)        # e.g. [4,2,1,3,5,0]
    inverse = np.argsort(forward)      # gives [5,2,1,3,0,4]

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
    size = math.ceil(flat.size / key_len)
    flat.resize(key_len, size)
    transp = flat.T

    return transp 

def double_transposition(matrix, key, key2, key_len, key_len2):
    print("Matriz Original")
    print(matrix)
    col = scramble(matrix, key, key_len)
    print("Embaralhado")
    print(col)
    col_transp = transpose_cols(col, key_len2)
    print("Transposto")
    print(col_transp)
    col_transp_col = scramble(col_transp, key2, key_len2)
    print("Embaralhado 2")
    print(col_transp_col)
    col_transp_col_transp = transpose_cols(col_transp_col, key_len2)
    print("Transposto 2 e Final:")
    print(col_transp_col_transp)

    return col_transp_col_transp

matrix = string_to_matrix(text, key_len)
#print("Matriz Original")
#print(matrix)



final = double_transposition(matrix, key, key2, key_len, key_len2)
#print("Double Columnar Transposition")
#print(final)

final = reverse_transpose_cols(final, key_len2)
##final = transpose_fixed_cols(final, key_len2)
print("Transposta Reversa")
print(final)

final = reverse_scramble(final, key2, key_len2)
print("Desembaralhada")
print(final)

final = reverse_transpose_cols(final, key_len)
##final = transpose_fixed_cols(final, key_len2)
print("Transposta Reversa 2")
print(final)

final = reverse_scramble(final, key, key_len)
print("Desembaralhada 2 e final")
print(final)
