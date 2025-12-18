<template>
    <section class="w-full flex flex-col gap-8">
        <div class="section-header">
            <!-- Composant de filtrage -->
            <div class="filter__header w-2/3">
                <filterFamily @filter-change="handleFilterChange"/>
            </div>
            
            <div class="section-stats" v-if="!dossierStore.loading && !dossierStore.error">
                <span class="stat-badge">{{ totalItems }} dossier(s)</span>
                <span v-if="dossierStore.stats && dossierStore.stats.total" class="stat-badge ml-2">
                    {{ dossierStore.stats.total }} total
                </span>
                <span v-if="activeFilterCount > 0" class="stat-badge ml-2 bg-yellow-100 text-yellow-800">
                    {{ activeFilterCount }} filtre(s) actif(s)
                </span>
                <button 
                    v-if="activeFilterCount > 0" 
                    @click="clearFilters" 
                    class="clear-all-btn ml-2"
                >
                    Effacer les filtres
                </button>
            </div>
        </div>

        <!-- État de chargement -->
        <div v-if="dossierStore.loading" class="w-full">
            <skeleton :isLoading="true"/>
        </div>

        <!-- État d'erreur -->
        <div v-else-if="dossierStore.error" class="error-state w-full">
            <div class="error-icon">
                <img src="../../assets/undraw_no-data_ig65.svg" alt="Aucun dossier">
            </div>
            <p class="error-message">{{ dossierStore.error }}</p>
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
                    :datefin="dossier.date_echeance"
                    :dossier="dossier"
                    :typeDossier="dossier.type_dossier"
                    :avancement="dossier.taux_avancement"
                    :documentsCount="dossier.documents_count"
                    :est-archive="dossier.est_archive"
                    :est-en-retard="dossier.est_en_retard"
                    :priorite="dossier.priorite"
                    @view="goToFolderDetail(dossier)"
                    @archive="archiveFolder(dossier)"
                    @mark-as-done="handleMarkAsDone(dossier)"
                    @delete="showDeleteModal(dossier)"
                    class="dossier-card"
                />
            </div>
            
            <!-- Message si aucun dossier -->
            <div v-if="paginatedDossiers.length === 0" class="empty-state">
                <div class="empty-icon">📁</div>
                <p class="empty-message">Aucun dossier trouvé</p>
                <p v-if="activeFilterCount > 0" class="empty-subtitle">
                    Essayez de modifier vos critères de recherche
                </p>
                <p v-else class="empty-subtitle">
                    Créez votre premier dossier pour commencer
                </p>
                <button v-if="activeFilterCount > 0" @click="clearFilters" class="retry-btn mt-4">
                    Effacer les filtres
                </button>
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

        <notificationPopup 
            :visible="notificationPopup.isVisible"
            :duration="notificationPopup.duration"
            :message="notificationPopup.message"
            :type="notificationPopup.type"
            @close="()=>notificationPopup.isVisible = false"
        />

        <editModale 
            :is-open="isModalOpen"
            @close="()=>isModalOpen = false"
            :customer="dossierStore.currentDossier"
        />

        <deleteModale 
            :is-open="isDeleteModaleOpen"
            :document="dossierStore.currentDossier"
            :item-to-delete="dossierToDelete"
            message="Ce dossier peut comporter des documents!!! Voulez-vous vraiment supprimer ce dossier?"
            @confirm="handleDeleteFolder" @close="()=>isDeleteModaleOpen = false"
        />
    </section>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import cardAffairsFolder from '../cards/cardAffairsFolder.vue';
import pagination from '../tools/pagination.vue';
import { useDossierStore } from '@/stores/dossierStore';
import notificationPopup from '../tools/notificationPopup.vue';
import skeleton from '../tools/skeleton.vue';
import filterFamily from '../input/filterFamily.vue';
import editModale from '../modales/editModale.vue';
import deleteModale from '../modales/deleteModale.vue';
import folderCard from '../cards/folderCard.vue';
import newCardsAffairs from '../cards/newCardsAffairs.vue';

export default {
    name: 'AffairIndexSection',
    components: {
        cardAffairsFolder,
        pagination,
        notificationPopup,
        skeleton,
        filterFamily,
        editModale,
        deleteModale,
        folderCard,
        newCardsAffairs
    },

    setup() {
        const router = useRouter();
        const dossierStore = useDossierStore();

        // États de pagination
        const currentPage = ref(1);
        const pageSize = ref(9); // 3x3 grid

        // Filtres actifs
        const activeFilters = ref({});
        const activeFilterCount = computed(() => {
            return Object.keys(activeFilters.value).filter(key => {
                const value = activeFilters.value[key];
                return value !== '' && value !== null && value !== undefined;
            }).length;
        });

        // Computed properties
        const totalItems = computed(() => dossierStore.dossiers.length);
        
        const paginatedDossiers = computed(() => {
            const startIndex = (currentPage.value - 1) * pageSize.value;
            const endIndex = startIndex + pageSize.value;
            return dossierStore.dossiers.slice(startIndex, endIndex);
        });

        const totalPages = computed(() => Math.ceil(totalItems.value / pageSize.value));

        // Notification
        const notificationPopup = ref({
            type: "success",
            isVisible: false,
            message: "",
            duration: 5000
        });

        // Gestion des filtres
        const handleFilterChange = async (filters) => {
            console.log('🔍 Filtres reçus:', filters);
            activeFilters.value = filters;
            currentPage.value = 1; // Retour à la première page
            
            // Nettoyer les filtres vides
            const cleanFilters = {};
            Object.keys(filters).forEach(key => {
                if (filters[key] !== '' && filters[key] !== null && filters[key] !== undefined) {
                    cleanFilters[key] = filters[key];
                }
            });
            
            console.log('🔍 Filtres nettoyés:', cleanFilters);
            await dossierStore.fetchDossiers(cleanFilters);
        };

        const clearFilters = async () => {
            activeFilters.value = {};
            currentPage.value = 1;
            await dossierStore.fetchDossiers();
        };


        // Manage all modales
        const isModalOpen = ref(false);
        const showModal = (currentAffair)=>{
            dossierStore.currentDossier = currentAffair
            isModalOpen.value = true;
            console.log(currentAffair)
        };

        // Delete modal
        const isDeleteModaleOpen = ref(false);
        const showDeleteModal = (doc) =>{
            isDeleteModaleOpen.value =  true;
            dossierToDelete.value = doc;
            console.log('Dossier sélectionné', doc)
        }
        const dossierToDelete = ref(null);

        // Méthodes existantes pour gérer les options sur le dossier 
        const goToFolderDetail = async (dossier) => {
            try {
                router.push(`/dashboard/customer/affairs/`);
                console.log('Chargement du dossier:', dossier.id);
                await dossierStore.fetchDossierById(dossier.id);
                console.log('Dossier chargé avec succès');
            } catch (error) {
                console.error('Erreur lors du chargement du dossier:', error);
                // Peut-être afficher une notification d'erreur
            }
        };

        const handleMarkAsDone = async(dossier) => {
            const formData = {
                statut: "CLOTURE"
            };
            
            try {
                await dossierStore.updateDossier(dossier?.id, formData, true);
                
                notificationPopup.value.isVisible = true;
                notificationPopup.value.message = "Dossier clôturé avec succès";
                notificationPopup.value.type = "success";
                
                setTimeout(() => {
                    notificationPopup.value.isVisible = false;
                }, 5000);
                
                await refreshData();
            } catch (error) {
                console.error("❌ Erreur lors du marquage:", error);
                notificationPopup.value.isVisible = true;
                notificationPopup.value.message = "Une erreur est survenue";
                notificationPopup.value.type = "error";
                
                setTimeout(() => {
                    notificationPopup.value.isVisible = false;
                }, 5000);
            }
        };

        const archiveFolder = async(dossier) => {
            const formData = {
                titre: dossier?.titre,
                type_dossier: dossier?.type_dossier,
                client: dossier?.client?.id,
                est_archive: true
            };
            
            try {
                await dossierStore.updateDossier(dossier?.id, formData, true);
                
                console.log("📁 Dossier archivé avec succès:", dossier?.reference_dossier);
                notificationPopup.value.isVisible = true;
                notificationPopup.value.message = "Dossier archivé avec succès";
                notificationPopup.value.type = "success";
                
                setTimeout(() => {
                    notificationPopup.value.isVisible = false;
                }, 5000);
                
                await refreshData();
            } catch (error) {
                console.error("❌ Erreur lors de l'archivage:", error);
                notificationPopup.value.isVisible = true;
                notificationPopup.value.message = "Une erreur est survenue lors de l'archivage";
                notificationPopup.value.type = "error";
                
                setTimeout(() => {
                    notificationPopup.value.isVisible = false;
                }, 5000);
            }
        };

        const handleDeleteFolder = async(dossier) => {

            try{
                await dossierStore.deleteDossier(dossier?.id);
                notificationPopup.value.isVisible = true;
                notificationPopup.value.message = "Dossier supprimé avec succès";
                notificationPopup.value.type = "success";
                setTimeout(() => {
                    notificationPopup.value.isVisible = false;
                }, 5000);
            } catch(error){
                console.error("❌ Erreur lors de la suppression du dossier", error);
                notificationPopup.value.isVisible = true;
                notificationPopup.value.message = "Une erreur est survenue lors de la suppression";
                notificationPopup.value.type = "error";
                
                setTimeout(() => {
                    notificationPopup.value.isVisible = false;
                }, 5000);
            } finally {
                // IMPORTANT : Fermer et nettoyer l'état de la modale après succès ou erreur
                isDeleteModaleOpen.value = false;
                dossierToDelete.value = null;
            }
        }

        const handlePageChange = (page) => {
            currentPage.value = page;
            scrollToTop();
        };

        const handlePageSizeChange = (size) => {
            pageSize.value = size;
            currentPage.value = 1;
        };

        const refreshData = async () => {
            try {
                await dossierStore.fetchDossiers(activeFilters.value);
                currentPage.value = 1;
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
        });

        return {

            // About modale
            isModalOpen,
            showModal,
            isDeleteModaleOpen,
            showDeleteModal,
            
            //
            dossierStore,
            paginatedDossiers,
            dossierToDelete,
            totalItems,
            currentPage,
            pageSize,
            activeFilters,
            activeFilterCount,
            notificationPopup,
            handleFilterChange,
            clearFilters,

            // Actions
            handleMarkAsDone,
            handleDeleteFolder,
            archiveFolder,
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
    margin-bottom: 1rem;
    flex-wrap: wrap;
    gap: 1rem;
}

.section-stats {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.stat-badge {
    background: #e0f2fe;
    color: #0369a1;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
}

.clear-all-btn {
    background: #f3f4f6;
    color: #374151;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
    border: 1px solid #e5e7eb;
    cursor: pointer;
    transition: all 0.2s;
}

.clear-all-btn:hover {
    background: #e5e7eb;
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
    width: 100%;
    border-radius: 12px;
}

.error-icon img {
    width: 300px;
    height: 300px;
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
    max-width: 300px;
    margin: 0 auto;
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
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
}

@media (min-width: 1024px) {
    .dossiers-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

.dossier-card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
}

.dossier-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Pagination */
.pagination-section {
    margin-top: 2rem;
}

/* Responsive */
@media (max-width: 1024px) {
    .dossiers-grid {
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1rem;
    }
}

@media (max-width: 768px) {
    .section-header {
        flex-direction: column;
        align-items: stretch;
        gap: 1rem;
    }
    
    .dossiers-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .section-stats {
        justify-content: flex-start;
    }
}

@media (max-width: 640px) {
    .loading-state,
    .error-state,
    .empty-state {
        padding: 2rem;
    }
    
    .error-icon img {
        width: 240px;
        height: 240px;
    }
}
</style>