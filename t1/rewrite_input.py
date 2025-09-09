path = "./livros/TheBrothersKaramazov.txt"
with open(path, "r", encoding="utf-8", newline="") as f:
    text = f.read()

with open("./livros/TheBrothersKaramazov_rewrite.txt", "w", encoding="utf-8", newline="") as f:
    f.write(text)

