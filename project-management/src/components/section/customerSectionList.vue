<template>
    <div class="customer-container">
        <!-- Loading State " -->
        <div v-if="store.loading"  class="loading-container">
            <skeleton :isLoading="true"/>
        </div>

        <!-- Error State -->
        <div v-else-if="store.error" class="error-container">
            <div class="error-icon">
                <img src="../../assets/undraw_no-data_ig65.svg" alt="Aucun dossier">
            </div>
            <p>{{ store.error }}</p>
            <button @click="refreshData" class="retry-btn">Réessayer</button>
        </div>

        <!-- Empty State -->
        <div v-else-if="displayedCustomers.length === 0" class="empty-container">
            <div class="error-icon">
                <img src="../../assets/undraw_no-data_ig65.svg" alt="Aucun dossier">
            </div>
            <button @click="refreshData" class="retry-btn">Actualiser</button>
        </div>

        <!-- Data Display -->
        <div v-else>
            <div class="customer__cards__container">
                <customerCards 
                    v-for="customer in displayedCustomers" 
                    :key="customer.id" 
                    :customer="customer"
                    :customerName="customer.nom_complet"
                    :description="customer.reference_client"
                    :typeClient="mapType(customer.type_client)"
                    :location="customer.ville"
                    :email="customer.email"
                    @handle-customer="openModal(customer)"
                    @handle-edit="goToCustomerDetails(customer)"
                />
            </div>
            
            <!-- Pagination -->
            <div class="pagination-container">
                <div class="pagination-info">
                    Affichage de {{ startIndex + 1 }} à {{ endIndex }} sur {{ totalCustomers }} clients
                </div>
                
                <div class="pagination-controls">
                    <button 
                        class="pagination-btn pagination-prev"
                        @click="prevPage"
                        :disabled="currentPage === 1"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                        </svg>
                        Précédent
                    </button>
                    
                    <div class="pagination-pages">
                        <button
                            v-for="page in visiblePages"
                            :key="page"
                            class="pagination-page"
                            :class="{ 'active': page === currentPage }"
                            @click="goToPage(page)"
                        >
                            {{ page }}
                        </button>
                        
                        <span v-if="showEllipsis" class="pagination-ellipsis">...</span>
                    </div>
                    
                    <button 
                        class="pagination-btn pagination-next"
                        @click="nextPage"
                        :disabled="currentPage === totalPages"
                    >
                        Suivant
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                        </svg>
                    </button>
                </div>
                
                <div class="pagination-size">
                    <label for="pageSize">Clients par page :</label>
                    <select 
                        id="pageSize"
                        v-model="pageSize" 
                        @change="onPageSizeChange"
                        class="page-size-select"
                    >
                        <option value="6">6</option>
                        <option value="12">12</option>
                        <option value="24">24</option>
                        <option value="48">48</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Modale -->
        <customerModale 
            :is-open="isOpen"
            :customer="selectedCustomer"
            @update:is-open="isOpen = $event"
            @close="closeModal"
        />
    </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import customerCards from '../cards/customerCards.vue';
import { useCustomerStore } from '@/stores/custumerStore';
import customerModale from '../modales/customerModale.vue';
import skeleton from '../tools/skeleton.vue';
import { useSearchStore } from '@/stores/searchStore';
import { useRouter } from 'vue-router';

export default {
    components: {
        customerCards,
        customerModale,
        skeleton
    },
    setup() {

        const router = useRouter();

        const isLoading = ref(true);

        const store = useCustomerStore();

        // Données réactives
        const currentPage = ref(1);
        const pageSize = ref(6);

        // Gestion de la modale
        const isOpen = ref(false);
        const selectedCustomer = ref(null);

        // Computed properties basées sur le store
        const totalCustomers = computed(() => store.customers.length);
        
        const displayedCustomers = computed(() => {
            const start = (currentPage.value - 1) * pageSize.value;
            const end = start + pageSize.value;
            return store.customers.slice(start, end);
        });

        const totalPages = computed(() => Math.ceil(totalCustomers.value / pageSize.value));
        
        const startIndex = computed(() => (currentPage.value - 1) * pageSize.value);
        
        const endIndex = computed(() => {
            const end = startIndex.value + pageSize.value;
            return end > totalCustomers.value ? totalCustomers.value : end;
        });
        
        const visiblePages = computed(() => {
            const pages = [];
            const maxVisible = 5;
            let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2));
            let end = Math.min(totalPages.value, start + maxVisible - 1);
            
            if (end - start + 1 < maxVisible) {
                start = Math.max(1, end - maxVisible + 1);
            }
            
            for (let i = start; i <= end; i++) {
                pages.push(i);
            }
            
            return pages;
        });
        
        const showEllipsis = computed(() => {
            return totalPages.value > visiblePages.value.length && 
                   visiblePages.value[visiblePages.value.length - 1] < totalPages.value;
        });

        // Methods
        const goToPage = (page) => {
            if (page >= 1 && page <= totalPages.value) {
                currentPage.value = page;
                scrollToTop();
            }
        };

        const goToCustomerDetails = (customer) => {
            // Logique pour naviguer vers les détails du client

            // Attacher le client selectionné au store avant la navigation
            store.attachCustomer(customer);

            // Debug log
            console.log('Naviguer vers les détails du client:', customer);
            router.push('/dashboard/customer-info')
        };
        
        const nextPage = () => {
            if (currentPage.value < totalPages.value) {
                currentPage.value++;
                scrollToTop();
            }
        };
        
        const prevPage = () => {
            if (currentPage.value > 1) {
                currentPage.value--;
                scrollToTop();
            }
        };
        
        const onPageSizeChange = () => {
            currentPage.value = 1;
        };
        
        const scrollToTop = () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        };

        const refreshData = async () => {
            try {
                await store.fetchCustomers();
                currentPage.value = 1; // Retour à la première page
            } catch (error) {
                console.error('Erreur lors du rafraîchissement:', error);
            }
        };

        // React to global search queries
        const searchStore = useSearchStore();

        watch(
            () => searchStore.query,
            async (newQuery) => {
                try {
                    if (!newQuery) {
                        // Clear search filter
                        store.setFilters({ search: '' });
                        await store.fetchCustomers();
                        currentPage.value = 1;
                        return;
                    }

                    // Apply search filter and reload customers
                    store.setFilters({ search: newQuery });
                    await store.fetchCustomers();
                    currentPage.value = 1;
                } catch (err) {
                    console.error('Erreur lors de l\'application du filtre de recherche clients:', err);
                }
            }
        );

        // Méthodes pour la modale
        const openModal = (customer) => {
            selectedCustomer.value = customer;
            isOpen.value = true;
            store.attachCustomer(customer);
            console.log('Client selectionné',customer)
        };

        // Mappe les types internes en labels lisibles
        const mapType = (type) => {
            if (!type) return '';
            if (type === 'PERSONNE_MORALE') return 'entreprise';
            if (type === 'PERSONNE_PHYSIQUE') return 'particulier';
            return type;
        };

        const closeModal = () => {
            isOpen.value = false;
            selectedCustomer.value = null;
        };

        // Watcher pour reset la pagination si les données changent
        watch(
            () => store.customers,
            () => {
                // Si on a moins de pages après un changement de données, on ajuste la page courante
                if (currentPage.value > totalPages.value) {
                    currentPage.value = Math.max(1, totalPages.value);
                }
            }
        );

        return {
            // Router
            router,

            // Gestion modale
            isLoading,
            isOpen,
            selectedCustomer,
            openModal,
            closeModal,

            // Pagination et données
            store,
            currentPage,
            pageSize,
            totalCustomers,
            totalPages,
            startIndex,
            endIndex,
            displayedCustomers,
            visiblePages,
            showEllipsis,
            goToPage,
            goToCustomerDetails,
            nextPage,
            prevPage,
            onPageSizeChange,
            refreshData
            ,
            mapType
        };
    }
}
</script>

<style scoped>
.customer-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.customer__cards__container {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1rem;
    flex: 1;
}

/* Loading, Error & Empty States */
.loading-container,
.error-container,
.empty-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    text-align: center;
    width: 100%;
}

.error-icon img{
    width: 320px;
    height: 320px;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #e2e8f0;
    border-top: 4px solid #0081C6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.error-icon,
.empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.retry-btn {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background: #0081C6;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s;
}

.retry-btn:hover {
    background: #0081C6;
}

/* Pagination Styles (garder les styles précédents) */
.pagination-container {
    margin-top: 2rem;
    padding: 1.5rem;
    background: #f8fafc;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.pagination-info {
    color: #64748b;
    font-size: 0.875rem;
    font-weight: 500;
}

.pagination-controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.pagination-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border: 1px solid #d1d5db;
    background: white;
    color: #374151;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
    background: #0081C6;
    color: white;
    border-color: #0081C6;
}

.pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.pagination-btn svg {
    width: 1rem;
    height: 1rem;
}

.pagination-pages {
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.pagination-page {
    min-width: 2.5rem;
    height: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #d1d5db;
    background: white;
    color: #374151;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}

.pagination-page:hover {
    background: #f1f5f9;
    border-color: #0081C6;
}

.pagination-page.active {
    background: #0081C6;
    color: white;
    border-color: #0081C6;
}

.pagination-ellipsis {
    padding: 0 0.5rem;
    color: #64748b;
    font-weight: 500;
}

.pagination-size {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.pagination-size label {
    color: #64748b;
    font-size: 0.875rem;
    font-weight: 500;
}

.page-size-select {
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    background: white;
    color: #374151;
    font-size: 0.875rem;
    cursor: pointer;
}

/* Responsive Design */
@media (max-width: 1024px) {
    .customer__cards__container {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 768px) {
    .customer__cards__container {
        grid-template-columns: 1fr;
    }
    
    .pagination-container {
        flex-direction: column;
        align-items: stretch;
        text-align: center;
    }
}
</style>