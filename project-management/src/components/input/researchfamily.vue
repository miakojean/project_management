<template>
    <div class="search-container">
        <div class="search-input-wrapper">
            <input 
                :placeholder="placeholder"
                v-model="searchQuery"
                @input="handleSearch"
                @focus="showResults = true"
                @keydown.enter="selectFirstResult"
                class="search-input"
                ref="searchInput"
            />
            <div v-if="loading" class="loading-spinner"></div>
            <button v-else-if="searchQuery" @click="clearSearch" class="clear-btn">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25Zm-1.72 6.97a.75.75 0 1 0-1.06 1.06L10.94 12l-1.72 1.72a.75.75 0 1 0 1.06 1.06L12 13.06l1.72 1.72a.75.75 0 1 0 1.06-1.06L13.06 12l1.72-1.72a.75.75 0 1 0-1.06-1.06L12 10.94l-1.72-1.72Z" clip-rule="evenodd" />
                </svg>
            </button>
            <button v-else class="search-btn">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path fill-rule="evenodd" d="M10.5 3.75a6.75 6.75 0 1 0 0 13.5 6.75 6.75 0 0 0 0-13.5ZM2.25 10.5a8.25 8.25 0 1 1 14.59 5.28l4.69 4.69a.75.75 0 1 1-1.06 1.06l-4.69-4.69A8.25 8.25 0 0 1 2.25 10.5Z" clip-rule="evenodd" />
                </svg>
            </button>
        </div>

        <transition name="slide-fade">
            <div v-if="showResults && searchQuery" class="search-results">
                <!-- Loading state -->
                <div v-if="loading" class="loading-results">
                    <loader/>
                </div>

                <!-- No results -->
                <div v-else-if="!loading && searchResults.length === 0" class="no-results">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="no-results-icon">
                        <path fill-rule="evenodd" d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003ZM12 8.25a.75.75 0 0 1 .75.75v3.75a.75.75 0 0 1-1.5 0V9a.75.75 0 0 1 .75-.75Zm0 8.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z" clip-rule="evenodd" />
                    </svg>
                    <div class="no-results-content">
                        <div class="no-results-title">Aucun résultat trouvé</div>
                        <div class="no-results-subtitle">Aucun dossier ou client ne correspond à "{{ searchQuery }}"</div>
                    </div>
                </div>

                <!-- Results -->
                <div v-else class="results-container">
                    <!-- Dossiers -->
                    <div v-if="dossiersList.length" class="results-section">
                        <div class="results-section-header">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                                <path d="M19.5 21a3 3 0 0 0 3-3v-4.5a3 3 0 0 0-3-3h-15a3 3 0 0 0-3 3V18a3 3 0 0 0 3 3h15ZM1.5 10.146V6a3 3 0 0 1 3-3h5.379a2.25 2.25 0 0 1 1.59.659l2.122 2.121c.14.141.331.22.53.22H19.5a3 3 0 0 1 3 3v1.146A4.483 4.483 0 0 0 19.5 9h-15a4.483 4.483 0 0 0-3 1.146Z" />
                            </svg>
                            <span class="section-title">Dossiers</span>
                            <span class="section-count">{{ dossiersList.length }}</span>
                        </div>
                        <div class="results-list">
                            <div v-for="item in dossiersList" 
                                 :key="'dossier-'+item.id" 
                                 class="result-item dossier-item"
                                 @click="selectResult(item)">
                                <div class="item-icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                                        <path d="M19.5 21a3 3 0 0 0 3-3v-4.5a3 3 0 0 0-3-3h-15a3 3 0 0 0-3 3V18a3 3 0 0 0 3 3h15ZM1.5 10.146V6a3 3 0 0 1 3-3h5.379a2.25 2.25 0 0 1 1.59.659l2.122 2.121c.14.141.331.22.53.22H19.5a3 3 0 0 1 3 3v1.146A4.483 4.483 0 0 0 19.5 9h-15a4.483 4.483 0 0 0-3 1.146Z" />
                                    </svg>
                                </div>
                                <div class="item-content">
                                    <div class="item-title">{{ item.titre || item.reference_dossier }}</div>
                                    <div class="item-details">
                                        <span class="badge reference">{{ item.reference_dossier }}</span>
                                        <span v-if="item.client_nom" class="client">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                <path fill-rule="evenodd" d="M7.5 6a4.5 4.5 0 1 1 9 0 4.5 4.5 0 0 1-9 0ZM3.751 20.105a8.25 8.25 0 0 1 16.498 0 .75.75 0 0 1-.437.695A18.683 18.683 0 0 1 12 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 0 1-.437-.695Z" clip-rule="evenodd" />
                                            </svg>
                                            {{ item.client_nom }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Clients -->
                    <div v-if="clientsList.length" class="results-section">
                        <div class="results-section-header">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                                <path fill-rule="evenodd" d="M8.25 6.75a3.75 3.75 0 1 1 7.5 0 3.75 3.75 0 0 1-7.5 0ZM15.75 9.75a3 3 0 1 1 6 0 3 3 0 0 1-6 0ZM2.25 9.75a3 3 0 1 1 6 0 3 3 0 0 1-6 0ZM6.31 15.117A6.745 6.745 0 0 1 12 12a6.745 6.745 0 0 1 6.709 7.498.75.75 0 0 1-.372.568A12.696 12.696 0 0 1 12 21.75c-2.305 0-4.47-.612-6.337-1.684a.75.75 0 0 1-.372-.568 6.787 6.787 0 0 1 1.019-4.38Z" clip-rule="evenodd" />
                                <path d="M5.082 14.254a8.287 8.287 0 0 0-1.308 5.135 9.687 9.687 0 0 1-1.764-.44l-.115-.04a.563.563 0 0 1-.373-.487l-.01-.121a3.75 3.75 0 0 1 3.57-4.047ZM20.226 19.389a8.287 8.287 0 0 0-1.308-5.135 3.75 3.75 0 0 1 3.57 4.047l-.01.121a.563.563 0 0 1-.373.486l-.115.04c-.567.2-1.156.349-1.764.441Z" />
                            </svg>
                            <span class="section-title">Clients</span>
                            <span class="section-count">{{ clientsList.length }}</span>
                        </div>
                        <div class="results-list">
                            <div v-for="item in clientsList" 
                                 :key="'client-'+item.id" 
                                 class="result-item client-item"
                                 @click="selectResult(item)">
                                <div class="item-icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                                        <path fill-rule="evenodd" d="M18.685 19.097A9.723 9.723 0 0 0 21.75 12c0-5.385-4.365-9.75-9.75-9.75S2.25 6.615 2.25 12a9.723 9.723 0 0 0 3.065 7.097A9.716 9.716 0 0 0 12 21.75a9.716 9.716 0 0 0 6.685-2.653Zm-12.54-1.285A7.486 7.486 0 0 1 12 15a7.486 7.486 0 0 1 5.855 2.812A8.224 8.224 0 0 1 12 20.25a8.224 8.224 0 0 1-5.855-2.438ZM15.75 9a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" clip-rule="evenodd" />
                                    </svg>
                                </div>
                                <div class="item-content">
                                    <div class="item-header">
                                        <div class="item-title">{{ item.nom_complet || item.raison_sociale }}</div>
                                        <span :class="['badge', 'type', item.type_client.toLowerCase()]">
                                            {{ getClientTypeLabel(item.type_client) }}
                                        </span>
                                    </div>
                                    <div class="item-details">
                                        <span v-if="item.reference_client" class="badge reference">
                                            {{ item.reference_client }}
                                        </span>
                                        <span v-if="item.email" class="email">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                <path d="M1.5 8.67v8.58a3 3 0 0 0 3 3h15a3 3 0 0 0 3-3V8.67l-8.928 5.493a3 3 0 0 1-3.144 0L1.5 8.67Z" />
                                                <path d="M22.5 6.908V6.75a3 3 0 0 0-3-3h-15a3 3 0 0 0-3 3v.158l9.714 5.978a1.5 1.5 0 0 0 1.572 0L22.5 6.908Z" />
                                            </svg>
                                            {{ item.email }}
                                        </span>
                                        <span v-if="item.telephone" class="phone">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                <path fill-rule="evenodd" d="M1.5 4.5a3 3 0 0 1 3-3h1.372c.86 0 1.61.586 1.819 1.42l1.105 4.423a1.875 1.875 0 0 1-.694 1.955l-1.293.97c-.135.101-.164.249-.126.352a11.285 11.285 0 0 0 6.697 6.697c.103.038.25.009.352-.126l.97-1.293a1.875 1.875 0 0 1 1.955-.694l4.423 1.105c.834.209 1.42.959 1.42 1.82V19.5a3 3 0 0 1-3 3h-2.25C8.552 22.5 1.5 15.448 1.5 6.75V4.5Z" clip-rule="evenodd" />
                                            </svg>
                                            {{ item.telephone }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </transition>

        <customerModale
            :is-open="isOpen"
            :customer="selectedCustomer"
            @close="isOpen = false"
        />
    </div>
</template>

<script>
// Le script reste exactement le même que votre version
import { ref, watch, onMounted, onUnmounted, computed } from 'vue';
import { useCustomerStore } from '@/stores/custumerStore';
import { useDossierStore } from '@/stores/dossierStore';
import { useSearchStore } from '@/stores/searchStore';
import { useRouter } from 'vue-router';
import customerModale from '../modales/customerModale.vue';
import loader from '../tools/loader.vue';

export default {
    name: 'SearchInput',
    
    props: {
        placeholder: {
            type: String,
            default: "Rechercher un client ou un dossier..."
        },
        debounceTime: {
            type: Number,
            default: 300
        }
    },

    components:{
        customerModale,
        loader
    },
    
    emits: ['select', 'search'],
    
    setup(props, { emit }) {
        const searchQuery = ref('');
        const searchResults = ref([]);
        const showResults = ref(false);
        const loading = ref(false);
        const searchInput = ref(null);
        let debounceTimer = null;

        const isOpen = ref(false);
        const selectedCustomer = ref({});

        const router = useRouter()
        
        const customerStore = useCustomerStore();
        const dossierStore = useDossierStore();
        
        const clientTypes = {
            'PERSONNE_PHYSIQUE': 'Personne',
            'PERSONNE_MORALE': 'Entreprise'
        };
        
        const statusLabels = {
            'ACTIF': 'Actif',
            'PROSPECT': 'Prospect',
            'INACTIF': 'Inactif'
        };
        
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
                    const q = searchQuery.value;
                    const [clientsRes, dossiersRes] = await Promise.allSettled([
                        customerStore.searchCustomers(q),
                        dossierStore.searchDossiers(q)
                    ]);

                    const clients = (clientsRes.status === 'fulfilled') ? (clientsRes.value || []) : [];
                    const dossiers = (dossiersRes.status === 'fulfilled') ? (dossiersRes.value || []) : [];

                    const normalizedClients = clients.map(c => ({ ...c, _type: 'client' }));
                    const normalizedDossiers = dossiers.map(d => ({ ...d, _type: 'dossier' }));

                    searchResults.value = [...normalizedDossiers, ...normalizedClients];

                    // Publish globally so sections can react and filter their tables
                    const searchStore = useSearchStore();
                    searchStore.setSearch(q, searchResults.value);

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

        const goToFolderDetail = async (dossier) => {
            try {
                router.push(`/dashboard/customer/affairs/`);
                console.log('Chargement du dossier:', dossier.id);
                await dossierStore.fetchDossierById(dossier.id);
                console.log('Dossier chargé avec succès');
            } catch (error) {
                console.error('Erreur lors du chargement du dossier:', error);
            }
        };
        
        const selectResult = (item) => {
            if (item._type === 'client') {
                customerStore.attachCustomer(item);
                isOpen.value=true;
                selectedCustomer.value = item;
            } else if (item._type === 'dossier') {
                dossierStore.attachAffair(item);
                goToFolderDetail(item)
            }

            emit('select', item);
            searchQuery.value = '';
            showResults.value = false;
            searchInput.value?.focus();
        };
        
        const selectFirstResult = () => {
            if (searchResults.value.length > 0 && !loading.value) {
                selectResult(searchResults.value[0]);
            }
        };
        
        const clearSearch = () => {
            searchQuery.value = '';
            searchResults.value = [];
            showResults.value = false;
            // clear global search state
            const searchStore = useSearchStore();
            searchStore.clearSearch();
            emit('clear');
            searchInput.value?.focus();
        };
        
        const handleClickOutside = (event) => {
            if (!event.target.closest('.search-container')) {
                showResults.value = false;
            }
        };
        
        const getClientTypeLabel = (type) => clientTypes[type] || type;
        const getStatusLabel = (status) => statusLabels[status] || status;

        watch(() => searchQuery.value, () => {
            if (searchQuery.value) {
                showResults.value = true;
            }
        });
        
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
            isOpen,
            selectedCustomer,
            handleSearch,
            selectResult,
            selectFirstResult,
            clearSearch,
            dossiersList,
            clientsList,
            getClientTypeLabel,
            getStatusLabel,
            goToFolderDetail
        };
    }
};
</script>

<style scoped>
.search-container {
    position: relative;
    width: 100%;
    max-width: 500px;
}

.search-input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.search-input-wrapper:focus-within {
    border-color: #005380;
    box-shadow: 0 4px 20px rgba(0, 83, 128, 0.15);
}

.search-input {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 12px;
    font-size: 15px;
    background: transparent;
    outline: none;
    color: #333;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.search-input::placeholder {
    color: #94a3b8;
    font-weight: 400;
}

.search-btn,
.clear-btn {
    position: absolute;
    right: 12px;
    background: none;
    border: none;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    padding: 0;
    color: #94a3b8;
    transition: all 0.2s ease;
}

.clear-btn:hover {
    color: #005380;
    transform: scale(1.1);
}

.search-btn svg,
.clear-btn svg {
    width: 100%;
    height: 100%;
}

.loading-spinner {
    position: absolute;
    right: 44px;
    width: 18px;
    height: 18px;
    border: 2px solid #e2e8f0;
    border-top: 2px solid #005380;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Results container */
.search-results {
    position: absolute;
    top: calc(100% + 8px);
    left: 0;
    right: 0;
    max-height: 500px;
    overflow-y: auto;
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    z-index: 1000;
    border: 1px solid #e2e8f0;
    animation: slideIn 0.2s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Loading state */
.loading-results {
    padding: 40px 20px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    color: #64748b;
}

.loading-dots {
    display: flex;
    gap: 6px;
}

.dot {
    width: 8px;
    height: 8px;
    background: #005380;
    border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out;
}

.dot:nth-child(2) {
    animation-delay: -0.32s;
}

.dot:nth-child(3) {
    animation-delay: -0.16s;
}

@keyframes bounce {
    0%, 80%, 100% {
        transform: scale(0);
        opacity: 0.3;
    }
    40% {
        transform: scale(1);
        opacity: 1;
    }
}

/* No results */
.no-results {
    padding: 40px 20px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
}

.no-results-icon {
    width: 60px;
    height: 60px;
    color: #cbd5e1;
}

.no-results-content {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.no-results-title {
    font-size: 18px;
    font-weight: 600;
    color: #334155;
}

.no-results-subtitle {
    font-size: 14px;
    color: #64748b;
    line-height: 1.4;
}

/* Results sections */
.results-container {
    padding: 16px 0;
}

.results-section {
    margin-bottom: 24px;
}

.results-section:last-child {
    margin-bottom: 0;
}

.results-section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 20px 12px 20px;
    border-bottom: 1px solid #f1f5f9;
    margin-bottom: 8px;
}

.section-icon {
    width: 18px;
    height: 18px;
    color: #005380;
}

.section-title {
    font-size: 14px;
    font-weight: 600;
    color: #334155;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.section-count {
    font-size: 12px;
    font-weight: 600;
    color: white;
    background: #005380;
    padding: 2px 8px;
    border-radius: 12px;
    min-width: 24px;
    text-align: center;
}

/* Results list */
.results-list {
    padding: 0 8px;
}

.result-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px;
    margin: 0 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid transparent;
}

.result-item:hover {
    background: #f8fafc;
    border-color: #e2e8f0;
    transform: translateX(2px);
}

.item-icon {
    width: 40px;
    height: 40px;
    background: #f1f5f9;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.dossier-item .item-icon {
    background: #e6f2f8;
    color: #005380;
}

.client-item .item-icon {
    background: #f0f9ff;
    color: #0077b3;
}

.item-icon svg {
    width: 20px;
    height: 20px;
}

.item-content {
    flex: 1;
    min-width: 0;
}

.item-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 6px;
}

.item-title {
    font-size: 14px;
    font-weight: 600;
    color: #1e293b;
    line-height: 1.4;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-box-orient: vertical;
}

.item-details {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    font-size: 12px;
    color: #64748b;
}

.detail-icon {
    width: 12px;
    height: 12px;
    margin-right: 4px;
    vertical-align: middle;
}

.email, .phone, .client {
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

/* Badges */
.badge {
    font-size: 11px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 10px;
    display: inline-flex;
    align-items: center;
    white-space: nowrap;
}

.badge.reference {
    background: #e2e8f0;
    color: #475569;
}

.badge.type {
    background: #f0f9ff;
    color: #0077b3;
}

.badge.type.personne_physique {
    background: #e0f2fe;
    color: #0369a1;
}

.badge.type.personne_morale {
    background: #f0f9ff;
    color: #0c4a6e;
}

.badge.status {
    background: #f1f5f9;
    color: #64748b;
}

.badge.status.actif {
    background: #dcfce7;
    color: #166534;
}

.badge.status.prospect {
    background: #fef3c7;
    color: #92400e;
}

.badge.status.inactif {
    background: #f1f5f9;
    color: #64748b;
}

/* Scrollbar */
.search-results::-webkit-scrollbar {
    width: 6px;
}

.search-results::-webkit-scrollbar-track {
    background: #f8fafc;
    border-radius: 0 16px 16px 0;
}

.search-results::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 3px;
}

.search-results::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

/* Animation pour l'apparition */
.slide-fade-enter-active {
    transition: all 0.2s ease-out;
}

.slide-fade-leave-active {
    transition: all 0.15s ease-in;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}
</style>