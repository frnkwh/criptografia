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
        input_file = f"livros/{book}.txt"
        for i in range(10):
            print(f"Running with {book}, attempt {i+1}/10")
            cmd = f'./aes/aes {key} {input_file} >> performanceAES.log'
            subprocess.run(cmd, check=True, shell=True)


def analysis():
    # read log 
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


def plot_algorithm_comparison(csv_file, output_image='comparison_plot.png'):
    df = pd.read_csv(csv_file)
    
    median_data = df.groupby(['file', 'algorithm', 'step'])['duration'].median().reset_index()
    
    sns.set_style("whitegrid")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), sharey=True)
    
    encryption_data = median_data[median_data['step'] == 'encryption']
    sns.barplot(data=encryption_data, x='file', y='duration', hue='algorithm', ax=ax1)
    ax1.set_title('Tempo Médio de Criptografia por Arquivo e Algoritmo')
    ax1.set_xlabel('Livro')
    ax1.set_ylabel('Duração Média (segundos)')
    ax1.set_yscale('log')
    ax1.tick_params(axis='x', rotation=45)
    
    decryption_data = median_data[median_data['step'] == 'decryption']
    sns.barplot(data=decryption_data, x='file', y='duration', hue='algorithm', ax=ax2)
    ax2.set_title('Tempo Médio de Descriptografia por Arquivo e Algoritmo')
    ax2.set_xlabel('Livro')
    ax2.set_ylabel('Duração Média (segundos)')
    ax2.set_yscale('log')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    ax2.legend_.remove()
    ax1.legend(title='Algoritmo')
    
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    print(f"Plot saved as {output_image}")
    

def main():
#    run_encryption_decryption()
#    run_encryption_decryption_aes()
#    analysis()
    plot_algorithm_comparison('results.csv', 'comparison_plot.png')

if __name__ == "__main__":
    main()

