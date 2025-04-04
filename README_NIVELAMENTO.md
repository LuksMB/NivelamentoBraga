# README_NIVELAMENTO

## Estrutura do Projeto para Análise das Questões
Este documento complementar descreve a estrutura básica do projeto para fins de análise e avaliação do nivelamento proposto, indicando onde cada questão está sendo tratada no código e onde os arquivos resultantes são armazenados.

## Observação: As questões devem ser executadas em ordem para o correto funcionamento

### Questão 1 - Extração de Dados
- **Arquivo de implementação**: `backend/src/pipeline/data_fetch.py`  
- **Destino dos arquivos**:
  - PDFs baixados → `backend/data/raw/`
  - Arquivos ZIP → `backend/data/raw/`

### Questão 2 - Transformação de Dados  
- **Arquivo de implementação**: `backend/src/pipeline/data_transform.py`  
- **Destino dos arquivos**:
  - CSVs processados → `backend/data/processed/`  
  - Zips transformados → `backend/data/processed/`

### Questão 3 - Consolidação Final  
- **Código de preparação**: `backend/src/pipeline/data_prepare.py`  
- **Saídas geradas**:
  - `dados_consolidados.csv` (últimos 2 anos) → `backend/data/processed/`  
  - `relatorio_cadop.csv` (dados cadastrais) → `backend/data/processed/`
- **Códigos de sql**: `backend/migrations/`

### Questão 4 - Interface + API
- **Código da API**: `backend/src/api/main.py`  
- **Códigos da interface**: `frontend/`
- **Testes no Postman/Insomnia**: `backend/src/api/HTTP Collection for Tests`

Esta estrutura foi planejada para manter uma separação clara entre as etapas do processo e facilitar a avaliação do projeto sem danificar sua estrutura.