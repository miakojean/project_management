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
                <div v-if="customer" class="customer-details">
                    <div class="detail-row">
                        <span class="detail-label">Nom complet :</span>
                        <span class="detail-value">{{ customer.nom_complet }}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Type de client :</span>
                        <span class="detail-value">{{ customer.type_client }}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">ID :</span>
                        <span class="detail-value">{{ customer.id }}</span>
                    </div>
                    <!-- Ajoutez d'autres champs selon votre structure de données -->
                </div>
                <div v-else class="no-customer">
                    <p>Aucune information client disponible</p>
                </div>
            </div>

            <!-- Footer -->
            <div class="modal-footer">
                <button @click="closeModal" class="btn-secondary">
                    Fermer
                </button>
                <button v-if="customer" @click="editCustomer" class="btn-primary">
                    Modifier
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

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
const emit = defineEmits(['update:isOpen', 'close'])

// États réactifs
const isMobile = ref(false)

// Méthodes
const closeModal = () => {
    emit('update:isOpen', false)
    emit('close')
}

const handleOverlayClick = (event) => {
    if (event.target.classList.contains('modal-overlay')) {
        closeModal()
    }
}

const editCustomer = () => {
    // Logique pour éditer le client
    console.log('Édition du client:', props.customer)
    // Vous pouvez émettre un événement ou naviguer vers une page d'édition
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

// Watch pour gérer le overflow du body
watch(() => props.isOpen, (newValue) => {
    if (newValue) {
        document.body.style.overflow = 'hidden'
        checkScreenSize()
    } else {
        document.body.style.overflow = ''
    }
})
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