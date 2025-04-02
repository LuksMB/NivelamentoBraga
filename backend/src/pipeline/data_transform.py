import pandas as pd
import pdfplumber
import zipfile
import time
import re
from pathlib import Path

INPUT_PDF = Path("../../data/raw/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")
OUTPUT_CSV = Path("../../data/processed/anexo_1.csv")
START_PAGE = 3
OUTPUT_ZIP = Path("../../data/processed/Teste_Lucas_M_Braga.zip")


TABLE_SETTINGS = {
    'vertical_strategy': 'lines',
    'horizontal_strategy': 'lines',
    'snap_tolerance': 10,
    'join_tolerance': 10
}

def clean_text(text):
    if text is None:
        return ""
    return re.sub(r'\s+', ' ', str(text).replace('\n', ' ')).strip()

def compress_files(files: list[Path], output_name: Path):
    with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            zipf.write(file, file.name)

    print(f"Finalizado: Arquivos compactados como {output_name.name}\n")

def pdf_tables_to_csv(pdf_path: Path, output_csv: Path, end_page: int = None, start_page: int = 3):
    all_data = []
    headers = None

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        end_page = end_page if (end_page is not None) else total_pages
        print(f"\nIniciando leitura de {total_pages} páginas no pdf, começando da página {start_page}...\n")
        start_time = time.time()

        for i in range(start_page - 1, min(end_page, total_pages)):
            try:
                page = pdf.pages[i]
                tables = page.extract_tables(TABLE_SETTINGS)

                for table in tables:
                    if not table or len(table) < 2:
                        continue

                    cleaned_table = []
                    for row in table:
                        cleaned_row = []
                        for cell in row:
                            cell_value = clean_text(cell)

                            if cell_value == 'OD':
                                cell_value = 'Seg. Odontológica'
                            elif cell_value == 'AMB':
                                cell_value = 'Seg. Ambulatorial'
                            
                            cleaned_row.append(cell_value)
                        cleaned_table.append(cleaned_row)

                    if headers is None:
                        headers = cleaned_table[0]

                    for row in cleaned_table[1:]:
                        all_data.append(row)

                print(f"Progresso: Página {i+1}/{total_pages}: dados extraídos com sucesso")
                
            except Exception as e:
                print(f"Erro na página {i+1}: {str(e)}")
                continue

    if all_data and headers:
        final_df = pd.DataFrame(all_data, columns=headers)
        final_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        final_time = time.time() - start_time

        print(f"\nCSV gerado com sucesso: {output_csv.name} | Tempo: {round(final_time, 2)}s")
        print(f"Total de registros: {len(final_df)}")
        return True
    else:
        print("Nenhuma tabela válida encontrada.")
        return False
    

# Execução principal
if __name__ == "__main__":
    pdf_tables_to_csv(
        pdf_path=INPUT_PDF,
        output_csv=OUTPUT_CSV,
        start_page=START_PAGE
    )
    compress_files([OUTPUT_CSV], OUTPUT_ZIP)