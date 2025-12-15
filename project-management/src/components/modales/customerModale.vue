<template>
    <div v-if="isOpen" class="modal-overlay" @click="handleOverlayClick">
        <div class="modal-container" :class="{ 'mobile-view': isMobile }">
            <!-- Header -->
            <div class="modal-header">
                <h2 class="modal-title">Détails du client</h2>
                <button class="close-button" @click="closeModal">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </button>
            </div>

            <!-- Content -->
            <div class="modal-content">
                <!-- Loading State -->
                <div v-if="loading" class="loading-state">
                    <div class="loading-spinner"></div>
                    <p>Chargement des dossiers...</p>
                </div>

                <!-- Error State -->
                <div v-else-if="error" class="error-state">
                    <p>Erreur: {{ error }}</p>
                    <button @click="loadCustomerDossiers" class="retry-btn">Réessayer</button>
                </div>

                <!-- Data Display -->
                <div v-else-if="customer" class="customer-details">
                    <!-- Informations client -->
                    <div class="customer-info">
                        <div class="detail-row">
                            <span class="detail-label">Nom complet :</span>
                            <span class="detail-value">{{ customer.nom_complet }}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Type de client :</span>
                            <span class="detail-value">{{ customer.type_client }}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Nombre de dossiers :</span>
                            <span class="detail-value">{{ customerDossiers.length }}</span>
                        </div>
                    </div>

                    <!-- Liste des dossiers -->
                    <div class="dossiers-section">
                        
                        <!-- Si des dossiers existent -->
                        <div v-if="customerDossiers.length > 0" class="dossiers-list">

                            <div class="folder__card grid grid-cols-2 gap-4">
                                <cardAffairsFolder 
                                    v-for="dossier in customerDossiers" :key="dossier.id"
                                    :client-nom="dossier.client_nom"
                                    :avancement="dossier.taux_avancement"
                                    :date-ouverture="dossier.date_creation_formatee"
                                    :documents-count="dossier.documents_count"
                                    :reference="dossier.reference_dossier"
                                    :statut="dossier.statut"
                                    :titre="dossier.titre"
                                    @view="goToFolderDetail(dossier)"
                                />
                            </div>

                        </div>
                        
                        <!-- Si aucun dossier -->
                        <div v-else class="no-dossiers">
                            <emptyCards 
                                title="Aucun dossier"
                                description="Ce client n'a pas encore de dossiers."
                                action-text="Créer un dossier"
                                @action="createNewDossier"
                            />
                        </div>
                    </div>
                </div>

                <!-- Fallback si pas de client -->
                <div v-else class="no-customer">
                    <emptyCards 
                        title="Client non trouvé"
                        description="Les informations du client ne sont pas disponibles."
                        action-text="Fermer"
                        @action="closeModal"
                    />
                </div>
            </div>

            <!-- Footer -->
            <div class="modal-footer">
                <button @click="closeModal" class="btn-secondary">
                    Fermer
                </button>
                <button v-if="customer && !loading && !error" @click="createNewDossier" class="btn-primary">
                    Créer un dossier
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import emptyCards from '../cards/emptyCards.vue'
import { useDossierStore } from '@/stores/dossierStore'
import { useRouter } from 'vue-router';
import { useCustomerStore } from '@/stores/custumerStore';
import cardAffairsFolder from '../cards/cardAffairsFolder.vue';

const router = useRouter();
const dossierStore = useDossierStore();

// Props
const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false
    },
    customer: {
        type: Object,
        default: null
    }
})

// Emits
const emit = defineEmits(['update:isOpen', 'close', 'create-dossier'])

// États réactifs
const isMobile = ref(false)
const loading = ref(false)
const error = ref(null)
const customerDossiers = ref([])

// Computed
const hasDossiers = computed(() => customerDossiers.value.length > 0)

// Méthodes
const closeModal = () => {
    emit('update:isOpen', false)
    emit('close')
    resetStates()
}

const handleOverlayClick = (event) => {
    if (event.target.classList.contains('modal-overlay')) {
        closeModal()
    }
}

const createNewDossier = async () => {
    if (props.customer) {
        emit('create-dossier', props.customer)
        closeModal()
        
        // Attendre le cycle de mise à jour suivant
        await nextTick()
        
        // Naviguer vers la page de création
        router.push('/create-affairs')
    }
}

const loadCustomerDossiers = async () => {
    if (!props.customer?.id) return
    
    loading.value = true
    error.value = null
    
    try {
        await dossierStore.fetchDossiersByClient(props.customer.id)
        customerDossiers.value = dossierStore.customerDossier
    } catch (err) {
        error.value = err.message || 'Erreur lors du chargement des dossiers'
        console.error('Erreur chargement dossiers:', err)
    } finally {
        loading.value = false
    }
}

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

const resetStates = () => {
    loading.value = false
    error.value = null
    customerDossiers.value = []
}

const checkScreenSize = () => {
    isMobile.value = window.innerWidth < 768
}

// Lifecycle
onMounted(() => {
    checkScreenSize()
    window.addEventListener('resize', checkScreenSize)
})

onUnmounted(() => {
    window.removeEventListener('resize', checkScreenSize)
})

// Watchers
watch(() => props.isOpen, (newValue) => {
    if (newValue) {
        document.body.style.overflow = 'hidden'
        checkScreenSize()
        
        if (props.customer?.id) {
            loadCustomerDossiers()
        }
    } else {
        document.body.style.overflow = ''
    }
})

watch(() => props.customer, (newCustomer) => {
    if (newCustomer?.id && props.isOpen) {
        loadCustomerDossiers()
    }
}, { deep: true })
</script>

<style scoped>
/* Reprenez les styles CSS du premier exemple que je vous ai donné */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: flex-end;
    align-items: stretch;
    z-index: 1000;
    animation: fadeIn 0.2s ease-out;
}

.modal-container {
    background: white;
    width: 50%;
    max-width: 600px;
    display: flex;
    flex-direction: column;
    gap:1rem;
    animation: slideIn 0.3s ease-out;
    box-shadow: -4px 0 16px rgba(0, 0, 0, 0.1);
}

.modal-container.mobile-view {
    width: 80%;
    max-width: none;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #e5e7eb;
    flex-shrink: 0;
}

.modal-title {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: #1f2937;
}

.close-button {
    background: none;
    border: none;
    padding: 0.5rem;
    cursor: pointer;
    color: #6b7280;
    border-radius: 0.375rem;
    transition: all 0.2s;
}

.close-button:hover {
    background-color: #f3f4f6;
    color: #374151;
}

.modal-content {
    flex: 1;
    padding: 1.5rem;
    overflow-y: auto;
    max-height: calc(100vh - 120px);
}

.customer-details {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.detail-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f3f4f6;
}

.detail-label {
    font-weight: 600;
    color: #374151;
}

.detail-value {
    color: #6b7280;
}

.modal-footer {
    padding: 1.5rem;
    border-top: 1px solid #e5e7eb;
    flex-shrink: 0;
    display: flex;
    gap: 0.75rem;
    justify-content: flex-end;
}

.btn-primary, .btn-secondary {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.375rem;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s;
}

.btn-primary {
    background-color: #3b82f6;
    color: white;
}

.btn-primary:hover {
    background-color: #2563eb;
}

.btn-secondary {
    background-color: #6b7280;
    color: white;
}

.btn-secondary:hover {
    background-color: #4b5563;
}

/* Animations et responsive - mêmes styles que précédemment */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideIn {
    from { transform: translateX(100%); }
    to { transform: translateX(0); }
}

@media (max-width: 767px) {
    .modal-overlay {
        justify-content: flex-end;
    }
    
    .modal-header {
        padding: 1rem;
    }
    
    .modal-title {
        font-size: 1.25rem;
    }
    
    .modal-content {
        padding: 1rem;
        max-height: calc(100vh - 80px);
    }
    
    .modal-footer {
        padding: 1rem;
    }
    
    .detail-row {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.25rem;
    }
}

@media (max-width: 480px) {
    .modal-container.mobile-view {
        width: 90%;
    }
}
</style>