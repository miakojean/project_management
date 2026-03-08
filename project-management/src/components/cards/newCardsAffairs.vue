<template>
    <div class="dossier-card" :class="{'urgent-card': isUrgent}" @click="handleCardClick">
        <div class="card-header">
            <div class="header-left">
                <div class="folder-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19.5 21a3 3 0 0 0 3-3v-4.5a3 3 0 0 0-3-3h-15a3 3 0 0 0-3 3V18a3 3 0 0 0 3 3h15ZM1.5 10.146V6a3 3 0 0 1 3-3h5.379a2.25 2.25 0 0 1 1.59.659l2.122 2.121c.14.141.331.22.53.22H19.5a3 3 0 0 1 3 3v1.146A4.483 4.483 0 0 0 19.5 9h-15a4.483 4.483 0 0 0-3 1.146Z" />
                    </svg>
                </div>
                <div class="dossier-info">
                    <h3 class="dossier-title">{{ titre }}</h3>
                    <p class="dossier-reference">{{ reference }}</p>
                </div>
            </div>

            <!-- Dropdown intégré directement -->
            <div class="options-container">
                <button 
                    class="options-btn" 
                    @click.stop="toggleDropdown"
                    aria-label="Options du dossier"
                    aria-expanded="showDropdown"
                    aria-haspopup="true"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                    </svg>
                </button>
                
                <transition name="dropdown">
                    <div 
                        v-if="showDropdown" 
                        class="dropdown-menu"
                        ref="dropdownRef"
                        @mousedown.stop
                    >
                        <ul class="dropdown-list">
                            <li class="dropdown-item" @mousedown="handleDropdownAction('view')">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="dropdown-icon">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                </svg>
                                <span>Voir le dossier</span>
                            </li>
                            <li class="dropdown-item" @mousedown="handleDropdownAction('edit')">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="dropdown-icon">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                                </svg>
                                <span>Modifier</span>
                            </li>
                            <li class="dropdown-item" @mousedown="handleDropdownAction('mark-as-done')">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11.35 3.836c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m8.9-4.414c.376.023.75.05 1.124.08 1.131.094 1.976 1.057 1.976 2.192V16.5A2.25 2.25 0 0 1 18 18.75h-2.25m-7.5-10.5H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V18.75m-7.5-10.5h6.375c.621 0 1.125.504 1.125 1.125v9.375m-8.25-3 1.5 1.5 3-3.75" />
                                </svg>
                                <span>Marquer comme clôturé</span>
                            </li>
                            <li class="dropdown-divider"></li>
                            <li class="dropdown-item dropdown-item-danger" @mousedown="handleDropdownAction('archive')">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="dropdown-icon">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="m20.25 7.5-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5m6 4.125 2.25 2.25m0 0 2.25 2.25M12 13.875l2.25-2.25M12 13.875l-2.25 2.25M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z" />
                                </svg>
                                <span>Archiver</span>
                            </li>
                            <li class="dropdown-item dropdown-item-danger" @mousedown="handleDropdownAction('delete')">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="dropdown-icon">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                                </svg>
                                <span>Supprimer</span>
                            </li>
                        </ul>
                    </div>
                </transition>
            </div>
            
        </div>

        <div class="card-content">
            <div class="info-row">
                <span class="label">Client:</span>
                <span class="value">{{ clientNom }}</span>
            </div>
            <div class="info-row">
                <span class="label">Type:</span>
                <span class="value">{{ typeText }}</span>
            </div>
            <div class="info-row">
                <span class="label">Date d'ouverture:</span>
                <span class="value">{{ dateOuverture }}</span>
            </div>
            <div v-if="dateEcheance" class="info-row">
                <span class="label">Échéance:</span>
                <span class="value" :class="{'urgent-text': isUrgent}">{{ dateEcheance }}</span>
            </div>
            
            <div class="progress-section">
                <div class="progress-header">
                    <span>Avancement</span>
                    <span>{{ avancement }}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" :style="`width: ${avancement}%`"></div>
                </div>
                <div class="priority-tag" v-if="priorite !== 'NORMALE'">
                    {{ prioriteText }}
                </div>

            </div>
        </div>

        <div class="card-footer">
            <div class="documents-info">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="doc-icon">
                    <path d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0 0 16.5 9h-1.875a1.875 1.875 0 0 1-1.875-1.875V5.25A3.75 3.75 0 0 0 9 1.5H5.625Z" />
                </svg>
                {{ documentsCount }} document(s)
            </div>
            <div class="status-badge" :class="statusClass">
                {{ statusText }}
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';

export default {
    name: 'DossierCard',
    props: {
        // Données principales
        titre: {
            type: String,
            default: 'Titre du dossier'
        },
        reference: {
            type: String,
            default: 'REF-00000'
        },
        dossierId: {
            type: [String, Number],
            default: null
        },
        
        // Client
        clientNom: {
            type: String,
            default: 'Nom du client'
        },
        
        // Statut et type
        statut: {
            type: String,
            default: 'NOUVEAU',
            validator: (value) => [
                'NOUVEAU', 'EN_COURS', 'EN_ATTENTE', 
                'BLOQUE', 'TERMINE', 'CLOTURE', 'ANNULE'
            ].includes(value)
        },
        typeDossier: {
            type: String,
            default: 'CONSEIL',
            validator: (value) => [
                'CONSTITUTION', 'MODIFICATION', 'DISSOLUTION', 'CONTENTIEUX',
                'CONSEIL', 'CONTRAT', 'AUDIT', 'PROPRIETE_INTELLECTUELLE',
                'FUSION_ACQUISITION', 'RECOUVREMENT', 'AUTRE'
            ].includes(value)
        },
        
        // Dates
        dateOuverture: {
            type: String,
            default: '01/01/2024'
        },
        dateEcheance: {
            type: String,
            default: ''
        },
        
        // Métriques
        avancement: {
            type: Number,
            default: 0,
            validator: (value) => value >= 0 && value <= 100
        },
        documentsCount: {
            type: Number,
            default: 0
        },
        
        // Priorité
        priorite: {
            type: String,
            default: 'NORMALE',
            validator: (value) => ['BASSE', 'NORMALE', 'HAUTE', 'URGENTE'].includes(value)
        }
    },
    emits: ['dossier-action', 'view', 'edit', 'mark-as-done', 'archive', 'delete', 'card-click'],
    
    setup(props, { emit }) {
        // État du dropdown
        const showDropdown = ref(false);
        const dropdownRef = ref(null);
        let clickOutsideHandler = null;
        
        // Computed properties
        const statusText = computed(() => {
            const statusMap = {
                'NOUVEAU': 'Nouveau',
                'EN_COURS': 'En cours',
                'EN_ATTENTE': 'En attente',
                'BLOQUE': 'Bloqué',
                'TERMINE': 'Terminé',
                'CLOTURE': 'Clôturé',
                'ANNULE': 'Annulé'
            };
            return statusMap[props.statut] || props.statut;
        });
        
        const statusClass = computed(() => {
            return `status-${props.statut.toLowerCase()}`;
        });
        
        const typeText = computed(() => {
            const typeMap = {
                'CONSTITUTION': 'Constitution',
                'MODIFICATION': 'Modification',
                'DISSOLUTION': 'Dissolution',
                'CONTENTIEUX': 'Contentieux',
                'CONSEIL': 'Conseil',
                'CONTRAT': 'Contrat',
                'AUDIT': 'Audit',
                'PROPRIETE_INTELLECTUELLE': 'Propriété Intel.',
                'FUSION_ACQUISITION': 'Fusion/Acquisition',
                'RECOUVREMENT': 'Recouvrement',
                'AUTRE': 'Autre'
            };
            return typeMap[props.typeDossier] || props.typeDossier;
        });
        
        const prioriteText = computed(() => {
            const prioriteMap = {
                'BASSE': 'Basse priorité',
                'NORMALE': 'Normale',
                'HAUTE': 'Haute priorité',
                'URGENTE': 'Urgent'
            };
            return prioriteMap[props.priorite] || props.priorite;
        });
        
        const isUrgent = computed(() => {
            return props.priorite === 'URGENTE';
        });
        
        // Méthodes du dropdown
        const toggleDropdown = () => {
            showDropdown.value = !showDropdown.value;
            
            if (showDropdown.value) {
                // Ajouter l'écouteur pour clic à l'extérieur
                setTimeout(() => {
                    clickOutsideHandler = (event) => {
                        if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
                            closeDropdown();
                        }
                    };
                    document.addEventListener('mousedown', clickOutsideHandler);
                }, 0);
            } else {
                // Retirer l'écouteur
                if (clickOutsideHandler) {
                    document.removeEventListener('mousedown', clickOutsideHandler);
                    clickOutsideHandler = null;
                }
            }
        };
        
        const closeDropdown = () => {
            showDropdown.value = false;
            
            // Retirer l'écouteur
            if (clickOutsideHandler) {
                document.removeEventListener('mousedown', clickOutsideHandler);
                clickOutsideHandler = null;
            }
        };
        
        // Gestion des clics sur la carte
        const handleCardClick = (event) => {
            // Empêcher le déclenchement quand on clique sur le dropdown
            if (event.target.closest('.options-container')) {
                return;
            }
            
            //console.log('Clic sur la carte du dossier:', props.reference);
            
            // Émettre l'événement générique
            emit('card-click', {
                dossierId: props.dossierId,
                reference: props.reference,
                titre: props.titre
            });
            
            // Émettre aussi l'événement view
            emit('view', {
                dossierId: props.dossierId,
                reference: props.reference,
                titre: props.titre
            });
        };
        
        // Gestion des actions du dropdown
        const handleDropdownAction = (action) => {
            //console.log('Action dropdown sélectionnée:', action, 'sur le dossier:', props.reference);
            
            const dossierData = {
                dossierId: props.dossierId,
                reference: props.reference,
                titre: props.titre,
                action: action
            };
            
            // Émettre l'événement générique
            emit('dossier-action', dossierData);
            
            // Émettre l'événement spécifique
            switch(action) {
                case 'view':
                    emit('view', dossierData);
                    break;
                case 'edit':
                    emit('edit', dossierData);
                    break;
                case 'mark-as-done':
                    emit('mark-as-done', dossierData);
                    break;
                case 'archive':
                    emit('archive', dossierData);
                    break;
                case 'delete':
                    emit('delete', dossierData);
                    break;
            }
            
            closeDropdown();
        };
        
        // Gestion de la touche Escape
        const handleEscapeKey = (event) => {
            if (event.key === 'Escape' && showDropdown.value) {
                closeDropdown();
            }
        };
        
        // Lifecycle
        onMounted(() => {
            document.addEventListener('keydown', handleEscapeKey);
        });
        
        onUnmounted(() => {
            document.removeEventListener('keydown', handleEscapeKey);
            if (clickOutsideHandler) {
                document.removeEventListener('mousedown', clickOutsideHandler);
            }
        });
        
        return {
            // État
            showDropdown,
            dropdownRef,
            
            // Computed
            statusText,
            statusClass,
            typeText,
            prioriteText,
            isUrgent,
            
            // Méthodes
            toggleDropdown,
            closeDropdown,
            handleCardClick,
            handleDropdownAction
        };
    }
};
</script>

<style scoped>
.dossier-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border: 1px solid #e2e8f0;
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
}

.dossier-card:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
}

.urgent-card {
    border-left: 4px solid #e53e3e;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 1.25rem 1.25rem 1rem;
    background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
    border-bottom: 1px solid #e2e8f0;
}

.header-left {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    flex: 1;
}

.folder-icon {
    color: #4299e1;
    flex-shrink: 0;
    margin-top: 0.25rem;
}

.folder-icon svg {
    width: 1.5rem;
    height: 1.5rem;
}

.dossier-info {
    flex: 1;
}

.dossier-title {
    font-size: 1.125rem;
    font-weight: 700;
    color: #2d3748;
    margin: 0 0 0.25rem 0;
    line-height: 1.3;
}

.dossier-reference {
    color: #718096;
    font-size: 0.875rem;
    font-weight: 500;
    margin: 0;
}

/* Styles du dropdown */
.options-container {
    position: relative;
    display: inline-block;
    z-index: 10;
}

.options-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s;
    color: #718096;
}

.options-btn:hover {
    background-color: #edf2f7;
    color: #4299e1;
}

.options-btn:focus {
    outline: 2px solid #4299e1;
    outline-offset: 2px;
}

.options-btn svg {
    width: 1.5rem;
    height: 1.5rem;
}

.dropdown-menu {
    position: absolute;
    top: 100%;
    right: 0;
    z-index: 1000;
    min-width: 200px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    border: 1px solid #e2e8f0;
    margin-top: 0.25rem;
    overflow: hidden;
}

/* Animation d'entrée/sortie */
.dropdown-enter-active {
    animation: dropdownFadeIn 0.2s ease;
}

.dropdown-leave-active {
    animation: dropdownFadeOut 0.15s ease;
}

@keyframes dropdownFadeIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes dropdownFadeOut {
    from {
        opacity: 1;
        transform: translateY(0);
    }
    to {
        opacity: 0;
        transform: translateY(-10px);
    }
}

.dropdown-list {
    list-style: none;
    padding: 0.5rem 0;
    margin: 0;
}

.dropdown-item {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
    font-size: 0.875rem;
    color: #4a5568;
    gap: 0.75rem;
    user-select: none;
}

.dropdown-item:hover {
    background-color: #f7fafc;
}

.dropdown-item:active {
    background-color: #edf2f7;
}

.dropdown-icon {
    width: 1.25rem;
    height: 1.25rem;
    flex-shrink: 0;
}

.dropdown-divider {
    height: 1px;
    background: #e2e8f0;
    margin: 0.5rem 0;
}

.dropdown-item-danger {
    color: #e53e3e;
}

.dropdown-item-danger:hover {
    background-color: #fed7d7;
}

.dropdown-item-danger:active {
    background-color: #feb2b2;
}

.status-badge {
    padding: 0.375rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    color: white;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
}

.status-nouveau { background: #3498db; }
.status-en_cours { background: #2ecc71; }
.status-en_attente { background: #f39c12; }
.status-bloque { background: #e74c3c; }
.status-termine { background: #27ae60; }
.status-cloture { background: #95a5a6; }
.status-annule { background: #7f8c8d; }

.card-content {
    padding: 1.25rem;
}

.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
    font-size: 0.875rem;
}

.info-row:last-child {
    margin-bottom: 0;
}

.label {
    color: #718096;
    font-weight: 500;
}

.value {
    color: #2d3748;
    font-weight: 600;
    text-align: right;
}

.urgent-text {
    color: #e53e3e;
    font-weight: 700;
}

.progress-section {
    margin-top: 1.25rem;
    padding-top: 1rem;
    border-top: 1px solid #e2e8f0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.progress-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
    color: #4a5568;
    font-weight: 500;
}

.progress-bar {
    width: 100%;
    height: 6px;
    background: #e2e8f0;
    border-radius: 3px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #48bb78, #38a169);
    border-radius: 3px;
    transition: width 0.5s ease;
}

.card-footer {
    padding: 1rem 1.25rem;
    border-top: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f7fafc;
}

.documents-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #718096;
    font-size: 0.875rem;
    font-weight: 500;
}

.doc-icon {
    width: 1rem;
    height: 1rem;
}

.priority-tag {
    padding: 0.25rem 0.5rem;
    border-radius: 16px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    width: auto;
}

.priority-tag {
    background: none;
    color: #c53030;
}

/* Responsive */
@media (max-width: 480px) {
    .card-header {
        flex-direction: column;
        gap: 0.75rem;
    }
    
    .status-badge {
        align-self: flex-start;
    }
    
    .dropdown-menu {
        position: fixed;
        right: 1rem;
        left: 1rem;
        bottom: 1rem;
        top: auto;
        max-height: 60vh;
        overflow-y: auto;
        margin-top: 0;
    }
}
</style>