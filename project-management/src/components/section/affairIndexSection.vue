<template>
    <section class="w-full flex flex-col gap-8">
        <div class="section-header">
            <h2 class="section-title">Dossiers récents</h2>
            <div class="section-stats" v-if="!dossierStore.loading && !dossierStore.error">
                <span class="stat-badge">{{ totalItems }} dossier(s)</span>
            </div>
        </div>

        <!-- État de chargement -->
        <div v-if="dossierStore.loading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Chargement des dossiers...</p>
        </div>

        <!-- État d'erreur -->
        <div v-else-if="dossierStore.error" class="error-state">
            <div class="error-icon">⚠️</div>
            <p class="error-message">Erreur: {{ dossierStore.error }}</p>
            <button @click="refreshData" class="retry-btn">Réessayer</button>
        </div>

        <!-- Données chargées -->
        <div v-else class="dossiers-container">
            <!-- Grille des dossiers -->
            <div class="dossiers-grid">
                <cardAffairsFolder 
                    v-for="dossier in paginatedDossiers" 
                    :key="dossier.id"
                    :titre="dossier.titre" 
                    :reference="dossier.reference_dossier"
                    :clientNom="dossier.client_nom"
                    :statut="dossier.statut"
                    :dateOuverture="dossier.date_creation_formatee"
                    :date-echeance="dossier.date_echeance"
                    :dossier="dossier"
                    :typeDossier="dossier.type_dossier"
                    :avancement="dossier.taux_avancement"
                    :documentsCount="dossier.documents_count"
                    @view="goToFolderDetail(dossier)"
                    @edit="handleEditDossier"
                    @duplicate="handleDuplicateDossier"
                    @archive="handleArchiveDossier"
                    @delete="handleDeleteDossier"
                    @dossier-action="handleDossierAction"
                    @card-click="handleCardClick"
                    class="dossier-card"
                />
            </div>
            
            <!-- Message si aucun dossier -->
            <div v-if="paginatedDossiers.length === 0" class="empty-state">
                <div class="empty-icon">📁</div>
                <p class="empty-message">Aucun dossier trouvé</p>
                <p class="empty-subtitle">Créez votre premier dossier pour commencer</p>
            </div>

            <!-- Pagination -->
            <pagination
                v-if="totalItems > 0"
                :total-items="totalItems"
                :current-page="currentPage"
                :page-size="pageSize"
                :show-page-size="true"
                :max-visible-pages="5"
                @page-change="handlePageChange"
                @page-size-change="handlePageSizeChange"
                class="pagination-section"
            />
        </div>
    </section>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import cardAffairsFolder from '../cards/cardAffairsFolder.vue';
import pagination from '../tools/pagination.vue'; // Assurez-vous du bon chemin
import { useDossierStore } from '@/stores/dossierStore';

export default {
    name: 'AffairIndexSection',
    components: {
        cardAffairsFolder,
        pagination,
    },

    setup() {
        const router = useRouter();
        const dossierStore = useDossierStore();

        // États de pagination
        const currentPage = ref(1);
        const pageSize = ref(9); // 3x3 grid

        // Computed properties
        const totalItems = computed(() => dossierStore.dossiers.length);
        
        const paginatedDossiers = computed(() => {
            const startIndex = (currentPage.value - 1) * pageSize.value;
            const endIndex = startIndex + pageSize.value;
            return dossierStore.dossiers.slice(startIndex, endIndex);
        });

        const totalPages = computed(() => Math.ceil(totalItems.value / pageSize.value));

        // Méthodes

        const goToFolderDetail = (dossier) => { //View
            router.push(`/dashboard/customer/affairs/`);
            dossierStore.attachAffair(dossier);
            console.log('Le dossier selectionné',dossier)
        };

        const updateFolder = async(dossierData) => { // Archive
            await dossierStore.updateDossier()
        }

        const handlePageChange = (page) => {
            currentPage.value = page;
            scrollToTop();
        };

        const handlePageSizeChange = (size) => {
            pageSize.value = size;
            currentPage.value = 1; // Retour à la première page
        };

        const refreshData = async () => {
            try {
                await dossierStore.fetchDossiers();
                currentPage.value = 1; // Reset à la première page
            } catch (error) {
                console.error('Erreur lors du rafraîchissement:', error);
            }
        };

        const scrollToTop = () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        };

        // Watchers
        watch(
            () => dossierStore.dossiers,
            () => {
                // Réinitialiser la pagination si les données changent
                if (currentPage.value > totalPages.value) {
                    currentPage.value = Math.max(1, totalPages.value);
                }
            }
        );

        // Lifecycle
        onMounted(async () => {
            console.log('📂 Chargement des dossiers pour affairIndexSection...');
            
            if (dossierStore.dossiers.length === 0) {
                await dossierStore.fetchDossiers();
            }
            
            console.log('✅ Dossiers disponibles:', dossierStore.dossiers.length);
            if (dossierStore.dossiers.length > 0) {
                console.log('📋 Structure d\'un dossier:', dossierStore.dossiers[0]);
            }
        });

        return {
            dossierStore,
            paginatedDossiers,
            totalItems,
            currentPage,
            pageSize,
            goToFolderDetail,
            handlePageChange,
            handlePageSizeChange,
            refreshData,
        };
    }
}
</script>

<style scoped>
.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1f2937;
    margin: 0;
}

.section-stats {
    display: flex;
    gap: 0.5rem;
}

.stat-badge {
    background: #e0f2fe;
    color: #0369a1;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
}

/* États de chargement, erreur et vide */
.loading-state,
.error-state,
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    text-align: center;
    background: #f8fafc;
    border-radius: 12px;
    border: 2px dashed #e2e8f0;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #e2e8f0;
    border-top: 4px solid #3b82f6;
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

.error-message,
.empty-message {
    font-size: 1.125rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 0.5rem;
}

.empty-subtitle {
    color: #6b7280;
    font-size: 0.875rem;
}

.retry-btn {
    margin-top: 1rem;
    padding: 0.5rem 1.5rem;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
}

.retry-btn:hover {
    background: #2563eb;
}

/* Conteneur principal */
.dossiers-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

/* Grille des dossiers */
.dossiers-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1.5rem;
}

.dossier-card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.dossier-card:hover {
    transform: translateY(-2px);
}

/* Pagination */
.pagination-section {
    margin-top: 2rem;
}

/* Responsive */
@media (max-width: 1024px) {
    .dossiers-grid {
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
    }
}

@media (max-width: 768px) {
    .section-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }
    
    .dossiers-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .section-title {
        font-size: 1.25rem;
    }
}

@media (max-width: 640px) {
    .loading-state,
    .error-state,
    .empty-state {
        padding: 2rem;
    }
    
    .error-icon,
    .empty-icon {
        font-size: 2.5rem;
    }
}
</style>