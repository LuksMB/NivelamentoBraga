# **📊 Data Pipeline: Processamento e Visualização de Dados**  

Sistema integrado para coleta, processamento, armazenamento e visualização de dados com suporte a **MySQL**, incluindo **API REST** (FastAPI) e **interface web** (Vue.js).

---

## 🌟 **Recursos Principais**
- **Extração de dados** de múltiplas fontes
- **Processamento** com Pandas (CSV, JSON)
- **API documentada** com FastAPI
- **Dashboard interativo** em Vue.js

---

## 🛠️ **Tecnologias**

| Componente       | Tecnologias                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **Backend**      | Python 3.10+, FastAPI, Pandas                                               |
| **Frontend**     | Vue 3, Vite, Axios, Chart.js, Tailwind CSS                                  |
| **Bancos**       | Scripts para MySQL                                                          |
| **Infra**        | Poetry (gerenciamento de dependências)                                      |

---

## 🚀 **Começando**

### **Pré-requisitos**
- Python 3.10+
- Node.js 18+
- Poetry (`pip install poetry`)
- MySQL

---

### **1. Configuração Inicial**

```bash
# Clone o repositório
git clone https://github.com/LuksMB/NivelamentoBraga.git
cd NivelamentoBraga

Edite o `.env` com suas credenciais:

```ini
# API
API_HOST="0.0.0.0"
API_PORT=8000

# Frontend
VITE_API_URL="http://localhost:8000"
```

---

### **2. Instalação**

#### **Backend**
```bash
pip install poetry
cd backend
poetry install
```

#### **Frontend**
```bash
cd ../frontend
npm install
```

---

### **4. Execução Manual**

#### **Backend**
```bash
cd backend
poetry run uvicorn src.main:app --reload
```

#### **Frontend**
```bash
cd ../frontend
npm run dev
```

---

## 📂 **Estrutura do Projeto**

```
data-pipeline/
├── backend/
│   ├── src/
│   │   ├── api/                    # Endpoints FastAPI
│   │   └── pipeline/               # fetch, prepare e transform scripts
│   ├── data/                       
│   │   ├── raw/                    # Arquivos brutos
│   │   └── processed/              # Arquivos processados
│   └── migrations/                 # Scripts .sql
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── composables/            # Lógica reutilizável
│   │   ├── stores/                 # Pinia (gerenciamento de estado)
│   │   ├── views/                  # Páginas
│   │   └── main.js                 # Inicialização Vue
│   └── vite.config.js
├── pyproject.toml                  # Dependências do backend
├── package.json                    # Dependências do frontend
├── LICENSE
├── README_NIVELAMENTO.md           #Explicação do projeto com ênfase nas entregas do nivelamento
└── README.md
```

---

## 🔍 **Endpoints da API**

| Método | Rota               | Descrição                               |
|--------|--------------------|-----------------------------------------|
| GET    | `/api/data`        | Lista todos os registros                |
| GET    | `/api/relevant`    | Detalhes de registros relevantes        |
| POST   | `/api/search`      | Busca textual nos dados                 |

Acesse a documentação interativa em:  
`http://localhost:8000/docs`

---

## 📝 **Licença**

MIT License - Consulte o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🤝 **Como Contribuir**

1. Faça um fork do projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

**Desenvolvido por Lucas M. Braga**

📧 [Email](lucasmb.7@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/lucas-braga-dev/)  

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Vue](https://img.shields.io/badge/Vue.js-3.x-green)](https://vuejs.org)
[![License](https://img.shields.io/badge/License-MIT-red)](LICENSE)

---