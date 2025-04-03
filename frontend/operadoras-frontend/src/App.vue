<template>
  <div class="fullscreen-app">
    <header class="app-header">
      <h1 class="app-title">Busca de Operadoras de Saúde</h1>
    </header>

    <main class="app-content">      
      <section class="search-section vintage-panel" v-if="dataLoaded">
        <h2 class="section-title">Buscar Operadoras</h2>
        <div class="search-controls">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Digite sua busca..." 
            class="vintage-input"
          />
          <select v-model="searchField" class="vintage-select">
            <option value="">Todos os campos</option>
            <option v-for="field in fields" :value="field" :key="field">{{ field }}</option>
          </select>
          <select v-model="searchUF" class="vintage-select">
            <option value="">Todos os estados</option>
            <option v-for="uf in ufs" :value="uf" :key="uf">{{ uf }}</option>
          </select>
          <select v-model="searchModalidade" class="vintage-select">
            <option value="">Todas modalidades</option>
            <option v-for="modalidade in modalidades" :value="modalidade" :key="modalidade">{{ modalidade }}</option>
          </select>
          <button @click="searchOperadoras" class="vintage-button">Buscar</button>
        </div>
        
        <div v-if="loading" class="loading-indicator">
          <div class="spinner"></div>
          <span>Carregando...</span>
        </div>
        
        <div v-if="searchResults.length > 0" class="results-container">
          <div class="results-header">
            <h3 class="results-title">Resultados ({{ totalResults }} encontrados)</h3>
          </div>
          <div class="table-wrapper">
            <table class="vintage-table">
              <thead>
                <tr>
                  <th>Registro ANS</th>
                  <th>Razão Social</th>
                  <th>Nome Fantasia</th>
                  <th>Modalidade</th>
                  <th>UF</th>
                  <th>Cidade</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="item in paginatedResults" 
                  :key="item.Registro_ANS" 
                  @click="showDetails(item)" 
                  class="clickable-row"
                >
                  <td>{{ item.Registro_ANS }}</td>
                  <td>{{ item.Razao_Social }}</td>
                  <td>{{ item.Nome_Fantasia }}</td>
                  <td>{{ item.Modalidade }}</td>
                  <td>{{ item.UF }}</td>
                  <td>{{ item.Cidade }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <div v-else-if="searchPerformed" class="no-results">
          <img src="https://cdn-icons-png.flaticon.com/512/4076/4076478.png" alt="Nenhum resultado" class="no-results-icon" />
          <p>Nenhum resultado encontrado.</p>
        </div>
      </section>
    </main>

    <footer class="app-footer" v-if="searchResults.length > 0">
      <div class="pagination-controls">
        <button @click="prevPage" :disabled="currentPage === 1">Anterior</button>
        <span>Página {{ currentPage }} de {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">Próxima</button>
      </div>
    </footer>
    
    <div v-if="selectedOperadora" class="vintage-modal" @click.self="selectedOperadora = null">
      <div class="modal-content">
        <button class="close-button" @click="selectedOperadora = null">×</button>
        <h2 class="modal-title">Detalhes da Operadora</h2>
        <div class="details-container">
          <div v-for="(value, key) in selectedOperadora" :key="key" class="detail-item">
            <strong class="detail-label">{{ key }}:</strong> 
            <span class="detail-value">{{ value }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      dataLoaded: false,
      uploadMessage: '',
      searchQuery: '',
      searchField: '',
      searchUF: '',
      searchModalidade: '',
      searchResults: [],
      paginatedResults: [],
      totalResults: 0,
      loading: false,
      searchPerformed: false,
      currentPage: 1,
      itemsPerPage: 15,
      fields: [
        'Razao_Social', 
        'Nome_Fantasia', 
        'Modalidade', 
        'Cidade', 
        'UF', 
        'Representante'
      ],
      ufs: [],
      modalidades: [],
      selectedOperadora: null
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.searchResults.length / this.itemsPerPage);
    }
  },
  watch: {
    currentPage() {
      this.updatePaginatedResults();
    },
    searchResults() {
      this.currentPage = 1;
      this.updatePaginatedResults();
    }
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:8000/operadoras/?limit=1');
      this.dataLoaded = true;
      this.loadUFs();
      this.loadModalidades();
    } catch (error) {
      console.log('Ainda não há dados carregados no servidor');
    }
  },
  methods: {
    updatePaginatedResults() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      this.paginatedResults = this.searchResults.slice(start, end);
    },
    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    async handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      const formData = new FormData();
      formData.append('file', file);
      
      try {
        this.uploadMessage = 'Enviando arquivo...';
        const response = await axios.post(
          'http://localhost:8000/upload-csv/',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        );
        
        this.uploadMessage = response.data.message;
        this.dataLoaded = true;
        this.loadUFs();
        this.loadModalidades();
      } catch (error) {
        this.uploadMessage = 'Erro ao carregar arquivo: ' + error.response?.data?.detail || error.message;
      }
    },
    async searchOperadoras() {
      if (!this.searchQuery.trim()) {
        alert('Por favor, digite um termo de busca');
        return;
      }
      
      this.loading = true;
      this.searchPerformed = true;
      
      try {
        const params = {
          query: this.searchQuery,
          limit: 500
        };
        
        if (this.searchField) params.campo = this.searchField;
        if (this.searchUF) params.uf = this.searchUF;
        if (this.searchModalidade) params.modalidade = this.searchModalidade;
        
        const response = await axios.get('http://localhost:8000/operadoras/search/', { params });
        
        this.searchResults = response.data.data;
        this.totalResults = response.data.total_results;
      } catch (error) {
        console.error('Erro na busca:', error);
        alert('Erro ao buscar operadoras');
      } finally {
        this.loading = false;
      }
    },
    async loadUFs() {
      try {
        const response = await axios.get('http://localhost:8000/operadoras/ufs/');
        this.ufs = response.data.ufs;
      } catch (error) {
        console.error('Erro ao carregar UFs:', error);
      }
    },
    async loadModalidades() {
      try {
        const response = await axios.get('http://localhost:8000/operadoras/modalidades/');
        this.modalidades = response.data.modalidades;
      } catch (error) {
        console.error('Erro ao carregar modalidades:', error);
      }
    },
    showDetails(item) {
      this.selectedOperadora = item;
    }
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600&family=EB+Garamond:wght@400;600&display=swap');

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden;
  background-color: #f5f1e6;
}

.fullscreen-app {
  width: 80vw;
  height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr auto;
  background-color: #f5f1e6;
  color: #3a3226;
  font-family: 'EB Garamond', serif;
  overflow: hidden;
}

.app-header {
  padding: 15px 20px;
  background-color: #8b5a2b;
  color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.app-title {
  font-family: 'Crimson Pro', serif;
  font-size: 2rem;
  margin: 0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
  letter-spacing: 1px;
}

.app-content {
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.app-footer {
  padding: 12px 20px;
  background-color: #8b5a2b;
  color: white;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.pagination-controls button {
  background: white;
  color: #8b5a2b;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-family: 'Crimson Pro', serif;
  min-width: 100px;
  font-size: 0.9rem;
}

.pagination-controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-controls span {
  font-size: 0.9rem;
}

.vintage-panel {
  width: 100%;
  background: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #d4c9a8;
}

.section-title {
  font-family: 'Crimson Pro', serif;
  color: #8b5a2b;
  margin-bottom: 15px;
  font-size: 1.3rem;
  border-bottom: 1px dashed #d4c9a8;
  padding-bottom: 6px;
}

.vintage-input, .vintage-select {
  padding: 8px 12px;
  border: 1px solid #d4c9a8;
  border-radius: 3px;
  background: #f5f1e6;
  font-family: 'EB Garamond', serif;
  font-size: 0.95rem;
  color: #3a3226;
  width: 100%;
}

.vintage-input:focus, .vintage-select:focus {
  outline: none;
  border-color: #8b5a2b;
  box-shadow: 0 0 0 2px rgba(139, 90, 43, 0.2);
}

.vintage-button {
  padding: 8px 16px;
  background: #8b5a2b;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-family: 'Crimson Pro', serif;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.vintage-button:hover {
  background: #7a4c24;
  transform: translateY(-1px);
}

.search-controls {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 20px;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(139, 90, 43, 0.2);
  border-top-color: #8b5a2b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.results-container {
  margin-top: 20px;
}

.results-header {
  margin-bottom: 15px;
}

.results-title {
  font-size: 1.1rem;
  color: #8b5a2b;
}

.table-wrapper {
  overflow-x: auto;
  max-height: calc(100vh - 400px);
}

.vintage-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.vintage-table th {
  background: #8b5a2b;
  color: white;
  padding: 10px 12px;
  text-align: left;
  font-family: 'Crimson Pro', serif;
  position: sticky;
  top: 0;
}

.vintage-table td {
  padding: 8px 12px;
  border-bottom: 1px solid #d4c9a8;
}

.vintage-table tr:nth-child(even) {
  background-color: rgba(139, 90, 43, 0.05);
}

.clickable-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.clickable-row:hover {
  background-color: #e8d8b8 !important;
}

.no-results {
  text-align: center;
  padding: 30px 20px;
}

.no-results-icon {
  width: 70px;
  opacity: 0.6;
  margin-bottom: 10px;
}

.no-results p {
  font-size: 1rem;
  color: #8b5a2b;
}

.vintage-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
}

.modal-content {
  background: #f5f1e6;
  padding: 25px;
  border-radius: 5px;
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  border: 1px solid #d4c9a8;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 22px;
  cursor: pointer;
  color: #8b5a2b;
}

.modal-title {
  font-family: 'Crimson Pro', serif;
  color: #8b5a2b;
  margin-bottom: 15px;
  font-size: 1.3rem;
}

.details-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 12px;
}

.detail-item {
  padding: 8px;
  border-bottom: 1px dashed #d4c9a8;
}

.detail-label {
  font-family: 'Crimson Pro', serif;
  color: #8b5a2b;
  display: block;
  margin-bottom: 2px;
  font-size: 0.9rem;
}

.detail-value {
  display: block;
  padding-left: 8px;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .app-header {
    padding: 12px 15px;
  }
  
  .app-title {
    font-size: 1.5rem;
  }
  
  .app-content {
    padding: 15px;
  }
  
  .search-controls {
    grid-template-columns: 1fr;
  }
  
  .pagination-controls {
    gap: 10px;
  }
  
  .pagination-controls button {
    padding: 6px 12px;
    min-width: 80px;
  }
  
  .details-container {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    width: 95%;
    padding: 15px;
  }
  
  .table-wrapper {
    max-height: calc(100vh - 350px);
  }
}
</style>