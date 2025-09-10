import numpy as np

text = "eugostomuitodagatinha"
key = "xandao"
key_len = len(key)

def string_to_matrix(text, key_len, pad=" "):
    text_len = len(text)
    if text_len % key_len != 0:
        extra = key_len - (text_len % key_len)
        text = text.ljust(text_len + extra, pad)

    arr = np.array(list(text)).reshape(-1, key_len)
    return arr

matrix = string_to_matrix(text, key_len)

print("Matriz Original")
print(matrix)

print("Matriz Transposta")
print(matrix.T)


def alphabetical_order(key):
    sorted_key = sorted([(char, i) for i, char in enumerate(key)])
    print(sorted_key)

    order = [0] * len(key)
    for rank, (_, i) in enumerate(sorted_key):
        order[i] = rank
    return order

new_order = alphabetical_order(key)
print(f"new_order: {new_order}")
reordered = matrix[:, new_order]
print("Matriz Reordenada")
print(reordered)
