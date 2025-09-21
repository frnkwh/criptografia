import pandas as pd
import json
import subprocess
import ast


def run_encryption_decryption():
    key1 = "milena"
    key2 = "frank"
    books = ["RipVanWinkle", "BlackBeauty", "TheBrothersKaramazov"]

    # run 10 times for each book
    for book in books:
        for i in range(10):
            print(f"Running with {book}, attempt {i+1}/10")
            cmd = ["uv", "run", "main.py", key1, key2, book]
            subprocess.run(cmd, check=True)


def run_encryption_decryption_aes():
    key = "milenalinda"
    books = ["RipVanWinkle", "BlackBeauty", "TheBrothersKaramazov"]

    # run 10 times for each book
    for book in books:
        input_file = f"../livros/{book}.txt"
        for i in range(10):
            print(f"Running with {book}, attempt {i+1}/10")
            cmd = ["./aes", key, input_file]
            subprocess.run(cmd, check=True)


def analysis():
    # read log 
    with open("performance.log") as f:
        logs = [json.loads(line) for line in f]

    df = pd.json_normalize(logs)
    df["message"] = df["record.message"].apply(ast.literal_eval)
    df = pd.concat([df, df["message"].apply(pd.Series)[["step", "duration", "file"]]], axis=1)
    df = df[["step", "duration", "file"]]

    print(df.head())

    # TODO: read log aes


def main():
#    run_encryption_decryption()
#    run_encryption_decryption_aes()
    analysis()


if __name__ == "__main__":
    main()

