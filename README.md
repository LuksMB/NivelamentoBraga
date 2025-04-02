# **📊 Data Pipeline: Processamento e Visualização de Dados**  

Sistema integrado para coleta, processamento, armazenamento e visualização de dados com suporte a **PostgreSQL** e **MySQL**, incluindo **API REST** (FastAPI) e **interface web** (Vue.js).

---

## 🌟 **Recursos Principais**
- **Extração de dados** de múltiplas fontes
- **Processamento** com Pandas (CSV, JSON)
- **Armazenamento flexível** (PostgreSQL ou MySQL)
- **API documentada** com FastAPI
- **Dashboard interativo** em Vue.js
- **100% containerizável** com Docker

---

## 🛠️ **Tecnologias**

| Componente       | Tecnologias                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **Backend**      | Python 3.10+, FastAPI, SQLAlchemy, Pandas, Alembic (migrations)             |
| **Frontend**     | Vue 3, Vite, Axios, Chart.js, Tailwind CSS                                  |
| **Bancos**       | PostgreSQL (psycopg2), MySQL (mysql-connector-python)                       |
| **Infra**        | Docker, Docker-Compose, Poetry (gerenciamento de dependências)                              |
| **Testes**       | pytest (backend), Vitest (frontend)                                         |

---

## 🚀 **Começando**

### **Pré-requisitos**
- Python 3.10+
- Node.js 18+
- Docker (opcional)
- Poetry (`pip install poetry`)

---

### **1. Configuração Inicial**

```bash
# Clone o repositório
git clone https://github.com/LuksMB/data-pipeline.git
cd data-pipeline

# Configure as variáveis de ambiente
cp .env.example .env
```

Edite o `.env` com suas credenciais:

```ini
# Escolha UM banco principal ou use ambos
DATABASE_TYPE="postgresql"  # ou "mysql"

# PostgreSQL
POSTGRES_URL="postgresql://user:password@localhost:5432/db_name"

# MySQL
MYSQL_URL="mysql+mysqlconnector://user:password@localhost:3306/db_name"

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

### **3. Execução com Docker (Recomendado)**

```bash
# Inicie todos os serviços
docker-compose up -d

# Ou para desenvolvimento:
docker-compose -f docker-compose.dev.yml up --build
```

---

### **4. Execução Manual**

#### **Backend**
```bash
cd backend
poetry run alembic upgrade head  # Aplica migrations
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
│   │   ├── db/                     # Configurações de banco
|   |   |   ├── connections/
│   │   │   │   ├── postgres.py     # Conexão PostgreSQL
│   │   │   │   ├── mysql.py        # Conexão MySQL
│   │   │   └── models.py           # Modelos SQLAlchemy
│   │   ├── api/                    # Endpoints FastAPI
│   │   ├── pipeline/               # ETL (extract, transform, load)
│   │   └── main.py                 # Ponto de entrada
│   ├── migrations/                 # Scripts Alembic
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── composables/            # Lógica reutilizável
│   │   ├── stores/                 # Pinia (gerenciamento de estado)
│   │   ├── views/                  # Páginas
│   │   └── main.js                 # Inicialização Vue
│   └── vite.config.js
├── data/                           # Dados processados
├── docker-compose.yml              # Produção
├── docker-compose.dev.yml          # Desenvolvimento
├── pyproject.toml                  # Dependências do backend
├── package.json                    # Dependências do frontend
├── LICENSE
└── README.md
```

---

## 🔍 **Endpoints da API**

| Método | Rota               | Descrição                      |
|--------|--------------------|--------------------------------|
| GET    | `/api/data`        | Lista todos os registros       |
| GET    | `/api/data/{id}`   | Detalhes de um registro        |
| POST   | `/api/search`      | Busca textual nos dados        |
| GET    | `/api/stats`       | Métricas gerais                |

Acesse a documentação interativa em:  
`http://localhost:8000/docs`

---

## 🧪 **Testes**

```bash
# Backend
cd backend
poetry run pytest

# Frontend
cd ../frontend
npm run test:unit
```

---

## 🐳 **Docker Compose**

Dois arquivos disponíveis:

1. **`docker-compose.yml`** (Produção):
   - PostgreSQL + MySQL
   - Backend otimizado
   - Frontend buildado

2. **`docker-compose.dev.yml`** (Desenvolvimento):
   - Hot-reload para Vue.js
   - Banco de dados com volumes persistentes
   - Monitoramento de logs

---

## 📌 **Dicas Importantes**

1. **Migrações de Banco**:
   ```bash
   alembic revision --autogenerate -m "descrição"
   alembic upgrade head
   ```

2. **Switching Databases**:
   ```python
   # Use SQLAlchemy Core para queries complexas
   from sqlalchemy import text
   result = db.execute(text("SELECT * FROM data WHERE ..."))
   ```

3. **Frontend-Backend**:
   ```javascript
   // frontend/src/composables/useApi.js
   import axios from 'axios';
   
   export default function useApi() {
     const search = async (query) => {
       return await axios.get('/api/search', { params: { query } });
     };
     return { search };
   }
   ```

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

**Desenvolvido por** [Lucas M. Braga]  
📧 [seu@email.com](lucasmb.7@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/lucas-braga-dev/)  

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Vue](https://img.shields.io/badge/Vue.js-3.x-green)](https://vuejs.org)
[![License](https://img.shields.io/badge/License-MIT-red)](LICENSE)

---