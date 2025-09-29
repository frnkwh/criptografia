import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import subprocess
import ast
import os

def run_encryption_decryption():
    key1 = "milena"
    key2 = "frank"
    books = ["RipVanWinkle", "BlackBeauty", "TheBrothersKaramazov"]

    for book in books:
        for i in range(10):
            print(f"Running with {book}, attempt {i+1}/10")
            cmd = ["uv", "run", "main.py", key1, key2, book]
            subprocess.run(cmd, check=True)


def run_encryption_decryption_aes():
    key = "milenalinda"
    books = ["RipVanWinkle", "BlackBeauty", "TheBrothersKaramazov"]

    for book in books:
        input_file = f"livros/{book}.txt"
        for i in range(10):
            print(f"Running with {book}, attempt {i+1}/10")
            cmd = f'./aes/aes {key} {input_file} >> performanceAES.log'
            subprocess.run(cmd, check=True, shell=True)


def analysis():
    with open("performanceFCC.log") as f:
        logs = [json.loads(line) for line in f]

    df1 = pd.json_normalize(logs)
    df1["message"] = df1["record.message"].apply(ast.literal_eval)
    df1 = pd.concat([df1, df1["message"].apply(pd.Series)[["step", "duration", "file"]]], axis=1)
    df1 = df1[["step", "duration", "file"]]
    df1["algorithm"] = "FCC"


    with open("performanceAES.log") as f:
            logs = [json.loads(line) for line in f]
    
    df2 = pd.DataFrame(logs)[["step", "duration", "file"]]
    df2["algorithm"] = "AES"
    df = pd.concat([df1, df2], ignore_index=True)

    df["run"] = df.groupby(["file", "algorithm", "step"]).cumcount() + 1
    df.to_csv("results.csv", index=False)
    print(df)


def plot_algorithm_comparison(csv_file, encryption_output='encryption_plot.png', decryption_output='decryption_plot.png'):
    df = pd.read_csv(csv_file)
    
    book_order = ['RipVanWinkle', 'BlackBeauty', 'TheBrothersKaramazov']
    size_labels = {'RipVanWinkle': '<10kb', 'BlackBeauty': '<100kb', 'TheBrothersKaramazov': '>1mb'}
    
    df['file_with_size'] = df['file'].map(lambda x: f"{x} ({size_labels[x]})")
    
    df['file_with_size'] = pd.Categorical(df['file_with_size'], 
                                         categories=[f"{book} ({size_labels[book]})" for book in book_order], 
                                         ordered=True)
    
    median_data = df.groupby(['file_with_size', 'algorithm', 'step'], observed=False)['duration'].median().reset_index()
    
    sns.set_style("whitegrid")
    
    encryption_data = median_data[median_data['step'] == 'encryption']
    plt.figure(figsize=(8, 6))
    sns.barplot(data=encryption_data, x='file_with_size', y='duration', hue='algorithm')
    plt.title('Tempo Médio de Criptografia por Arquivo e Algoritmo')
    plt.xlabel('Livro')
    plt.ylabel('Duração Média (segundos)')
    plt.yscale('log')
    plt.xticks(rotation=45)
    plt.legend(title='Algoritmo')
    plt.tight_layout()
    plt.savefig(encryption_output, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Encryption plot saved as {encryption_output}")
    
    decryption_data = median_data[median_data['step'] == 'decryption']
    plt.figure(figsize=(8, 6))
    sns.barplot(data=decryption_data, x='file_with_size', y='duration', hue='algorithm')
    plt.title('Tempo Médio de Descriptografia por Arquivo e Algoritmo')
    plt.xlabel('Livro')
    plt.ylabel('Duração Média (segundos)')
    plt.yscale('log')
    plt.xticks(rotation=45)
    plt.legend(title='Algoritmo')
    plt.tight_layout()
    plt.savefig(decryption_output, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Decryption plot saved as {decryption_output}")


def main():
#    run_encryption_decryption()
#    run_encryption_decryption_aes()
#    analysis()
    plot_algorithm_comparison('results.csv', 'encryption_plot.png', 'decryption_plot.png')

if __name__ == "__main__":
    main()

