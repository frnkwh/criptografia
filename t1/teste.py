with open("./livros/TheBrothersKaramazov.txt", "rb") as f:
    original_bytes = f.read()

with open("decrypted.txt", "rb") as f:
    decrypted_bytes = f.read()

print(original_bytes == decrypted_bytes)  # should be True
print(len(original_bytes), len(decrypted_bytes))

