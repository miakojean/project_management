<template>
  <div class="filters-container">
    <div class="filter-row">
      <!-- Filtre par statut -->
      <div class="input__family">
        <label>Statut</label>
        <select 
          v-model="filters.statut"
          @change="applyFilters"
        >
          <option value="">Tous les statuts</option>
          <option value="NOUVEAU">Nouveau</option>
          <option value="EN_COURS">En cours</option>
          <option value="EN_ATTENTE">En attente</option>
          <option value="TERMINE">Terminé</option>
          <option value="CLOTURE">Clôturé</option>
          <option value="ANNULE">Annulé</option>
        </select>
      </div>

      <!-- Filtre par archive -->
        <div class="input__family">
            <label>État</label>
            <select 
                v-model="filters.est_archive"
                @change="applyFilters"
            >
                <option value="">Tous</option>
                <option :value="false">Actifs</option>
                <option :value="true">Archivés</option>
            </select>
        </div>

      <!-- Recherche par texte -->
      
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useDossierStore } from '@/stores/dossierStore';

export default {
  name: 'filterFamily',
  
  setup() {
    const dossierStore = useDossierStore();
    const filters = ref({
      statut: '',
      type_dossier: '',
      est_archive: '',
      search: ''
    });

    let debounceTimer = null;

    const applyFilters = async () => {
      // Nettoyer les filtres vides
      const cleanFilters = {};
      Object.keys(filters.value).forEach(key => {
        if (filters.value[key] !== '' && filters.value[key] !== null) {
          cleanFilters[key] = filters.value[key];
        }
      });

      // console.log('🔍 Appliquer filtres:', cleanFilters);
      
      try {
        await dossierStore.fetchDossiers(cleanFilters);
      } catch (error) {
        // console.error('Erreur lors du filtrage:', error);
      }
    };

    const debounceApplyFilters = () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        applyFilters();
      }, 300); // Délai de 300ms
    };

    const clearFilters = async () => {
      filters.value = {
        statut: '',
        type_dossier: '',
        est_archive: '',
        search: ''
      };
      await dossierStore.fetchDossiers();
    };

    return {
      filters,
      applyFilters,
      debounceApplyFilters,
      clearFilters
    };
  }
}
</script>

<style scoped>
.filters-container {
  width: 100%;
  margin-bottom: 2rem;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: flex-end;
}

.input__family {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 200px;
}

.input__family.search-box {
  flex-grow: 1;
  max-width: 300px;
}

.search-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 0.9rem 2.5rem 0.9rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  border-color: #2563eb;
  outline: none;
}

.clear-btn {
  position: absolute;
  right: 0.5rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0 0.5rem;
  line-height: 1;
  transition: color 0.2s;
}

.clear-btn:hover {
  color: #dc2626;
}

label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

select {
  padding: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem;
  width: 100%;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
  background-color: white;
}

select:focus {
  border-color: #2563eb;
  outline: none;
}

@media (max-width: 768px) {
  .filter-row {
    flex-direction: column;
  }
  
  .input__family {
    width: 100%;
    max-width: none;
  }
  
  .input__family.search-box {
    max-width: none;
  }
}
</style>