<template>
    <div class="search-container">
        <div class="search-input-wrapper">
            <input 
                type="search" 
                :placeholder="placeholder"
                v-model="searchQuery"
                @input="handleSearch"
                @focus="showResults = true"
                @keydown.enter="selectFirstResult"
                class="search-input"
                ref="searchInput"
            />
            <div v-if="loading" class="loading-spinner"></div>
        </div>

        <div v-if="showResults && searchQuery" class="search-results">
            <!-- Loading state -->
            <div v-if="loading" class="loading-results">
                Recherche en cours...
            </div>

            <!-- No results -->
            <div v-else-if="!loading && searchResults.length === 0" class="no-results">
                Aucun résultat pour "{{ searchQuery }}"
            </div>

            <!-- Results -->
            <div v-else class="results-list">
                <div v-if="dossiersList.length">
                    <div class="results-section-title">Dossiers</div>
                    <div v-for="item in dossiersList" :key="'dossier-'+item.id" class="result-item" @click="selectResult(item)">
                        <div class="dossier-info">
                            <div class="dossier-title"><strong>{{ item.titre || item.reference_dossier }}</strong></div>
                            <div class="dossier-meta">
                                <span v-if="item.reference_dossier">Réf: {{ item.reference_dossier }}</span>
                                <span v-if="item.client_nom">• Client: {{ item.client_nom }}</span>
                                <span v-if="item.statut">• Statut: {{ getStatusLabel(item.statut) }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="clientsList.length">
                    <div class="results-section-title">Clients</div>
                    <div v-for="item in clientsList" :key="'client-'+item.id" class="result-item" @click="selectResult(item)">
                        <div class="client-info">
                            <div class="client-name">
                                <strong>{{ item.nom_complet || item.raison_sociale }}</strong>
                                <span class="client-type" :class="item.type_client">{{ getClientTypeLabel(item.type_client) }}</span>
                            </div>
                            <div class="client-details">
                                <span v-if="item.reference_client" class="ref">Réf: {{ item.reference_client }}</span>
                                <span v-if="item.email" class="email">{{ item.email }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, watch, onMounted, onUnmounted, computed } from 'vue';
import { useCustomerStore } from '@/stores/custumerStore';
import { useDossierStore } from '@/stores/dossierStore';
import { useRouter } from 'vue-router';

export default {
    name: 'SearchInput',
    
    props: {
        placeholder: {
            type: String,
            default: "Trouver un client..."
        },
        debounceTime: {
            type: Number,
            default: 300
        }
    },
    
    emits: ['select', 'search'],
    
    setup(props, { emit }) {
        const searchQuery = ref('');
        const searchResults = ref([]);
        const showResults = ref(false);
        const loading = ref(false);
        const searchInput = ref(null);
        let debounceTimer = null;

        // Router
        const router = useRouter()
        
        // Utilisation des stores
        const customerStore = useCustomerStore();
        const dossierStore = useDossierStore();
        
        // Types de clients
        const clientTypes = {
            'PERSONNE_PHYSIQUE': 'Personne physique',
            'PERSONNE_MORALE': 'Personne morale'
        };
        
        // Statuts
        const statusLabels = {
            'ACTIF': 'Actif',
            'PROSPECT': 'Prospect',
            'INACTIF': 'Inactif'
        };
        
        // Gestion de la recherche avec debounce
        const handleSearch = () => {
            clearTimeout(debounceTimer);
            
            if (!searchQuery.value.trim()) {
                searchResults.value = [];
                emit('clear');
                return;
            }
            
            loading.value = true;
            
            debounceTimer = setTimeout(async () => {
                try {
                    // Lancer les deux recherches en parallèle (clients + dossiers)
                    const q = searchQuery.value;
                    const [clientsRes, dossiersRes] = await Promise.allSettled([
                        customerStore.searchCustomers(q),
                        dossierStore.searchDossiers(q)
                    ]);

                    const clients = (clientsRes.status === 'fulfilled') ? (clientsRes.value || []) : [];
                    const dossiers = (dossiersRes.status === 'fulfilled') ? (dossiersRes.value || []) : [];

                    // Normaliser les résultats (ajouter un type)
                    const normalizedClients = clients.map(c => ({ ...c, _type: 'client' }));
                    const normalizedDossiers = dossiers.map(d => ({ ...d, _type: 'dossier' }));

                    // Fusionner: dossiers d'abord puis clients (ou configurable)
                    searchResults.value = [...normalizedDossiers, ...normalizedClients];

                    // Émission de l'événement
                    emit('search', {
                        query: q,
                        results: searchResults.value
                    });

                } catch (error) {
                    console.error('Erreur lors de la recherche combinée:', error);
                    searchResults.value = [];
                } finally {
                    loading.value = false;
                }
            }, props.debounceTime);
        };
        
        // Sélection d'un résultat (client ou dossier)
        const selectResult = (item) => {
            if (item._type === 'client') {
                customerStore.attachCustomer(item);
            } else if (item._type === 'dossier') {
                dossierStore.attachAffair(item);
            }

            // Émettre l'événement + fermer
            emit('select', item);
            searchQuery.value = '';
            showResults.value = false;
            searchInput.value?.focus();
        };
        
        // Sélection du premier résultat avec Entrée
        const selectFirstResult = () => {
            if (searchResults.value.length > 0 && !loading.value) {
                selectClient(searchResults.value[0]);
            }
        };
        
        // Effacer la recherche
        const clearSearch = () => {
            searchQuery.value = '';
            searchResults.value = [];
            showResults.value = false;
            emit('clear');
            searchInput.value?.focus();
        };
        
        // Fermer les résultats en cliquant en dehors
        const handleClickOutside = (event) => {
            if (!event.target.closest('.search-container')) {
                showResults.value = false;
            }
        };
        
        // Labels
        const getClientTypeLabel = (type) => clientTypes[type] || type;
        const getStatusLabel = (status) => statusLabels[status] || status;
        
        // Watcher pour détecter les changements de recherche
        watch(() => searchQuery.value, () => {
            if (searchQuery.value) {
                showResults.value = true;
            }
        });
        
        // Lifecycle
        onMounted(() => {
            document.addEventListener('click', handleClickOutside);
        });
        
        onUnmounted(() => {
            clearTimeout(debounceTimer);
            document.removeEventListener('click', handleClickOutside);
        });
        
        const dossiersList = computed(() => searchResults.value.filter(i => i._type === 'dossier'));
        const clientsList = computed(() => searchResults.value.filter(i => i._type === 'client'));

        return {
            router,
            searchQuery,
            searchResults,
            showResults,
            loading,
            searchInput,
            handleSearch,
            selectResult,
            selectFirstResult,
            clearSearch,
            dossiersList,
            clientsList,
            getClientTypeLabel,
            getStatusLabel
        };
    }
};
</script>

<style scoped>
.search-container {
    position: relative;
    width: 400px;
}

.search-input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}

.search-input {
    width: 100%;
    padding: 10px 40px 10px 15px;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 14px;
    transition: all 0.3s ease;
    outline: none;
    background: white;
}

.search-input:focus {
    border-color: #007bff;
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.clear-btn {
    position: absolute;
    right: 10px;
    background: none;
    border: none;
    font-size: 20px;
    color: #999;
    cursor: pointer;
    padding: 0;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.2s ease;
}

.clear-btn:hover {
    background: #f0f0f0;
    color: #666;
}

.loading-spinner {
    position: absolute;
    right: 35px;
    width: 20px;
    height: 20px;
    border: 2px solid #f3f3f3;
    border-top: 2px solid #007bff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.search-results {
    position: absolute;
    top: calc(100% + 5px);
    left: 0;
    right: 0;
    max-height: 400px;
    overflow-y: auto;
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 1000;
}

.results-list {
    padding: 10px 0;
}

.result-item {
    padding: 12px 15px;
    cursor: pointer;
    transition: all 0.2s ease;
    border-bottom: 1px solid #f5f5f5;
}

.result-item:hover {
    background: #f8f9fa;
}

.result-item:last-child {
    border-bottom: none;
}

.client-info {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.client-name {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.client-type {
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: 600;
}

.client-type.PERSONNE_PHYSIQUE {
    background: #e3f2fd;
    color: #1565c0;
}

.client-type.PERSONNE_MORALE {
    background: #f3e5f5;
    color: #7b1fa2;
}

.client-details {
    display: flex;
    gap: 15px;
    font-size: 12px;
    color: #666;
    flex-wrap: wrap;
}

.ref, .email, .phone {
    display: flex;
    align-items: center;
    gap: 4px;
}

.client-status {
    align-self: flex-start;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: 600;
    margin-top: 5px;
}

.client-status.ACTIF {
    background: #e8f5e9;
    color: #2e7d32;
}

.client-status.PROSPECT {
    background: #fff3e0;
    color: #f57c00;
}

.client-status.INACTIF {
    background: #f5f5f5;
    color: #757575;
}

.loading-results,
.no-results {
    padding: 30px 20px;
    text-align: center;
    color: #666;
    font-size: 14px;
}

.no-results {
    color: #999;
}

/* Scrollbar styling */
.search-results::-webkit-scrollbar {
    width: 6px;
}

.search-results::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.search-results::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 3px;
}

.search-results::-webkit-scrollbar-thumb:hover {
    background: #aaa;
}
</style>