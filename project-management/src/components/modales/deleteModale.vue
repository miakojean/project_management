<template>
    <div v-if="isOpen" class="modal-overlay" @click="handleOverlayClick">
        <div class="modal-container" :class="{ 'mobile-view': isMobile }">
            <!-- Header -->
            <div class="modal-header">
                <div class="header-content">
                    <div class="warning-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.347 16.5c-.77.833.192 2.5 1.732 2.5z" 
                                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <div>
                        <h2 class="modal-title">Confirmer la suppression</h2>
                        <p class="modal-subtitle">Cette action est irréversible</p>
                    </div>
                </div>
                <button class="close-button" @click="closeModal">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </button>
            </div>

            <!-- Content -->
            <div class="modal-content">
                <!-- Message principal -->
                <div class="message-section">
                    <p class="delete-message">
                        {{ message || 'Êtes-vous sûr de vouloir supprimer cet élément ?' }}
                    </p>
                </div>

                <!-- Élément à supprimer -->
                <div v-if="itemToDelete" class="item-preview">
                    <div class="item-content">
                        <div v-if="itemIcon" class="item-icon">
                            {{ itemIcon }}
                        </div>
                        <div class="item-details">
                            <p class="item-name">{{ itemToDelete.name || itemToDelete.title || itemToDelete.titre }}</p>
                            <p v-if="itemToDelete.description" class="item-description">
                                {{ itemToDelete.description }}
                            </p>
                            <p v-if="itemToDelete.reference_dossier" class="item-reference">
                                Référence : {{ itemToDelete.reference_dossier }}
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Confirmation supplémentaire -->
                <div v-if="confirmationRequired" class="confirmation-section">
                    <label class="confirmation-label">
                        <input 
                            type="checkbox" 
                            v-model="confirmed"
                            class="confirmation-checkbox"
                        >
                        <span class="confirmation-text">
                            {{ confirmationText || 'Je confirme vouloir supprimer cet élément' }}
                        </span>
                    </label>
                </div>

                <!-- Message d'erreur -->
                <div v-if="error" class="error-section">
                    <p class="error-message">{{ error }}</p>
                </div>
            </div>

            <!-- Footer -->
            <div class="modal-footer">
                <button @click="closeModal" class="btn-secondary">
                    {{ cancelButtonText || 'Annuler' }}
                </button>
                <dangerButton 
                    @click="confirmDelete"
                />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import dangerButton from '../button/dangerButton.vue'

// Props
const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false
    },
    itemToDelete: {
        type: Object,
        default: null
    },
    itemIcon: {
        type: String,
        default: ''
    },
    title: {
        type: String,
        default: 'Confirmer la suppression'
    },
    message: {
        type: String,
        default: 'Êtes-vous sûr de vouloir supprimer cet élément ?'
    },
    deleteButtonText: {
        type: String,
        default: 'Supprimer'
    },
    cancelButtonText: {
        type: String,
        default: 'Annuler'
    },
    confirmationRequired: {
        type: Boolean,
        default: false
    },
    confirmationText: {
        type: String,
        default: 'Je confirme vouloir supprimer cet élément'
    },
    closeOnBackdropClick: {
        type: Boolean,
        default: true
    },
    documents:{
        type:Object,
        default:()=>[]
    }
})

// Emits
const emit = defineEmits(['update:isOpen', 'close', 'confirm'])

// États réactifs
const isMobile = ref(false)
const loading = ref(false)
const error = ref(null)
const confirmed = ref(false)

// Méthodes
const closeModal = () => {
    emit('update:isOpen', false)
    emit('close')
    resetStates()
}

const handleOverlayClick = (event) => {
    if (props.closeOnBackdropClick && event.target.classList.contains('modal-overlay')) {
        closeModal()
    }
}

const confirmDelete = async () => {
    if (props.confirmationRequired && !confirmed.value) {
        return
    }
    
    loading.value = true
    error.value = null
    
    try {
        // Émettre l'événement de confirmation
        emit('confirm', props.itemToDelete)
        
        // Fermer la modal après un délai pour l'UI
        setTimeout(() => {
            closeModal()
        }, 300)
        
    } catch (err) {
        error.value = err.message || 'Erreur lors de la suppression'
        //console.error('Erreur suppression:', err)
    } finally {
        loading.value = false
    }
}

const resetStates = () => {
    loading.value = false
    error.value = null
    confirmed.value = false
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
        resetStates()
    } else {
        document.body.style.overflow = ''
    }
})

// Reset confirmation quand l'item change
watch(() => props.itemToDelete, () => {
    confirmed.value = false
})
</script>

<style scoped>
/* Variables */
:root {
    --danger-color: #dc2626;
    --danger-hover: #b91c1c;
    --danger-light: #fee2e2;
    --danger-text: #991b1b;
    --danger-disabled: #fca5a5;
    --gray-light: #f3f4f6;
    --gray-border: #e5e7eb;
    --gray-text: #6b7280;
    --gray-dark: #374151;
    --primary-color: #3b82f6;
    --primary-hover: #2563eb;
    --white: #ffffff;
    --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Overlay */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.3);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    animation: fadeIn 0.2s ease-out;
    padding: 20px;
}

/* Container */
.modal-container {
    background: white;
    width: 100%;
    max-width: 500px;
    border-radius: 12px;
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    max-height: 90vh;
    overflow: hidden;
}

.modal-container.mobile-view {
    max-width: 95%;
}

/* Header */
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 24px;
    border-bottom: 1px solid var(--gray-border);
    background-color: var(--danger-light);
}

.header-content {
    display: flex;
    align-items: center;
    gap: 12px;
}

.warning-icon {
    width: 40px;
    height: 40px;
    background-color: var(--white);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--danger-color);
    flex-shrink: 0;
}

.modal-title {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--danger-text);
}

.modal-subtitle {
    margin: 4px 0 0;
    font-size: 0.875rem;
    color: var(--danger-text);
    opacity: 0.8;
}

.close-button {
    background: none;
    border: none;
    padding: 8px;
    cursor: pointer;
    color: var(--gray-text);
    border-radius: 6px;
    transition: all 0.2s;
    flex-shrink: 0;
    margin-left: 8px;
}

.close-button:hover {
    background-color: rgba(0, 0, 0, 0.05);
    color: var(--gray-dark);
}

/* Content */
.modal-content {
    padding: 24px;
    overflow-y: auto;
    flex: 1;
}

.message-section {
    margin-bottom: 20px;
}

.delete-message {
    margin: 0;
    font-size: 1rem;
    line-height: 1.5;
    color: var(--gray-dark);
}

/* Item Preview */
.item-preview {
    background-color: var(--gray-light);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 20px;
    border: 1px solid var(--gray-border);
}

.item-content {
    display: flex;
    align-items: flex-start;
    gap: 12px;
}

.item-icon {
    font-size: 1.25rem;
    color: var(--gray-text);
    flex-shrink: 0;
    margin-top: 2px;
}

.item-details {
    flex: 1;
}

.item-name {
    margin: 0 0 8px 0;
    font-weight: 600;
    font-size: 1rem;
    color: var(--gray-dark);
}

.item-description {
    margin: 0 0 4px 0;
    font-size: 0.875rem;
    color: var(--gray-text);
    line-height: 1.4;
}

.item-reference {
    margin: 0;
    font-size: 0.875rem;
    color: var(--gray-text);
    font-family: monospace;
}

/* Confirmation Section */
.confirmation-section {
    margin: 24px 0;
    padding: 16px;
    background-color: var(--gray-light);
    border-radius: 8px;
    border: 1px solid var(--gray-border);
}

.confirmation-label {
    display: flex;
    align-items: center;
    cursor: pointer;
    margin: 0;
}

.confirmation-checkbox {
    width: 18px;
    height: 18px;
    margin-right: 12px;
    cursor: pointer;
    accent-color: var(--danger-color);
}

.confirmation-text {
    font-size: 0.9375rem;
    color: var(--gray-dark);
    line-height: 1.4;
}

/* Error Section */
.error-section {
    margin-top: 16px;
    padding: 12px;
    background-color: var(--danger-light);
    border-radius: 6px;
    border: 1px solid var(--danger-color);
}

.error-message {
    margin: 0;
    font-size: 0.875rem;
    color: var(--danger-text);
    text-align: center;
}

/* Footer */
.modal-footer {
    padding: 24px;
    border-top: 1px solid var(--gray-border);
    display: flex;
    gap: 12px;
    justify-content: flex-end;
    flex-shrink: 0;
}

/* Buttons */
.btn-secondary, .btn-danger {
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    font-size: 0.9375rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    min-width: 100px;
    text-align: center;
}

.btn-secondary {
    background-color: var(--white);
    color: var(--gray-dark);
    border: 1px solid var(--gray-border);
}

.btn-secondary:hover {
    background-color: var(--gray-light);
}

.btn-danger {
    background-color: var(--danger-color);
    color: var(--white);
    position: relative;
}

.btn-danger:hover:not(.btn-disabled) {
    background-color: var(--danger-hover);
}

.btn-disabled {
    background-color: var(--danger-disabled);
    cursor: not-allowed;
    opacity: 0.7;
}

.btn-disabled:hover {
    background-color: var(--danger-disabled);
}

/* Loading Spinner */
.loading-spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    margin-right: 8px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: var(--white);
    animation: spin 1s ease-in-out infinite;
    vertical-align: middle;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideIn {
    from { transform: translateY(-20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 767px) {
    .modal-overlay {
        padding: 16px;
    }
    
    .modal-header {
        padding: 20px;
    }
    
    .modal-content {
        padding: 20px;
    }
    
    .modal-footer {
        padding: 20px;
        flex-direction: column;
    }
    
    .btn-secondary, .btn-danger {
        width: 100%;
        min-width: 0;
    }
    
    .header-content {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }
    
    .warning-icon {
        align-self: flex-start;
    }
}

@media (max-width: 480px) {
    .modal-container.mobile-view {
        max-width: 100%;
    }
    
    .modal-header {
        padding: 16px;
    }
    
    .modal-content {
        padding: 16px;
    }
    
    .modal-footer {
        padding: 16px;
    }
}
</style>