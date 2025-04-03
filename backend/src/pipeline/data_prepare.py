import requests
import os
import time
import zipfile
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse

URL_CSV = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
URLS_ZIP = [
    'https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023/',
    'https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/'
]

def download_csv(url : str, output_dir : Path = Path("../../data/processed")):
    print("Progresso: Iniciando download do arquivo csv...")
    
    start_time = time.time()
    parsed_url = urlparse(url)
    filename = Path(parsed_url.path).name.lower()

    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    file_path = output_dir / filename

    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192): 
            if chunk:
                f.write(chunk)

    download_time = time.time() - start_time
    print(f"Progresso: Download concluído em {download_time:.2f}s")

def download_zip_and_consolidate_csv(urls : list, output_dir : Path = Path("../../data/processed")):
    print("\nProgresso: Iniciando processo de busca e download dos arquivos...")
    start_time = time.time()
    links = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.endswith('.zip'):
                full_link = requests.compat.urljoin(url, href)
                links.append(full_link)

    dfs = []
    print("Iniciando extração e consolidação dos arquivos csv...")
    for link in links:
        zip_name = os.path.join(output_dir, link.split('/')[-1])
        csv_name = os.path.join(output_dir, zip_name.replace('.zip', '.csv'))

        with open(zip_name, 'wb') as f:
            f.write(requests.get(link).content)

        with zipfile.ZipFile(zip_name, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

        # Adicionado conversão de vírgula para ponto nas colunas 5 e 6, para correção de decimais
        df = pd.read_csv(csv_name, sep=';', converters={
            4: lambda x: x.replace(',', '.') if isinstance(x, str) else x,
            5: lambda x: x.replace(',', '.') if isinstance(x, str) else x
        })
        dfs.append(df)

        os.remove(zip_name)
        os.remove(csv_name)

    output_file = os.path.join(output_dir, 'dados_consolidados.csv')
    pd.concat(dfs).to_csv(output_file, index=False)
    
    final_time = time.time() - start_time
    print(f"Processo concluído! Arquivo final: dados_consolidados.csv | Tempo: {round(final_time, 2)}s ")

if __name__ == "__main__":
    download_zip_and_consolidate_csv(URLS_ZIP)
    download_csv(URL_CSV)

