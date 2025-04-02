import requests
import time
import zipfile
from pathlib import Path
from urllib.parse import urlparse

URLS_ANEXOS = [
    "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf",
    "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"
]
PATHS_ANEXOS = [
    Path("../../data/raw/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"),
    Path("../../data/raw/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf")
]

def compress_files(files: list[Path], output_name: Path = Path("../../data/raw/backup_anexos.zip")):
    with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            zipf.write(file, file.name)

    print(f"Finalizado: Arquivos compactados como {output_name.name}\n")

def download_files(urls: list, output_dir: Path = Path("../../data/raw")):
    total_files = len(urls)
    print(f"Progresso: Iniciando download de {total_files} arquivos...")

    for i, url in enumerate(urls, 1):
        try:
            start_time = time.time()
            parsed_url = urlparse(url)
            filename = Path(parsed_url.path).name or f"file_{i}"
            
            print(f"\nProgresso: Arquivo {i}/{total_files} sendo baixado...")

            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            file_path = output_dir / filename
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192): 
                    if chunk:
                        f.write(chunk)

            download_time = time.time() - start_time
            file_size = file_path.stat().st_size / (1024 * 1024)
            
            print(f"Progresso: Download concluído: {file_size:.2f} MB")
            print(f"    Tempo: {download_time:.2f}s | Velocidade: {file_size/download_time:.2f} MB/s")

        except requests.exceptions.RequestException as e:
            print(f"    Erro: Falha no download: {e}")
            continue
        except Exception as e:
            print(f"    Erro: {e}")
            continue

    print("\nFinalizado: Todos os downloads foram processados!\n")
    return True

# Execução principal
if __name__ == "__main__":
    download_files(URLS_ANEXOS)
    compress_files(PATHS_ANEXOS)