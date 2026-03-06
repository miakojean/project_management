<template>
    <div class="dossier-card" :class="{'urgent-card': isUrgent}" @click="handleCardClick">
        <div class="card-header">
            <div class="header-left">
                <div class="client-avatar">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6" v-if="!clientImage">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
                    </svg>

                    <img v-else :src="clientImage" :alt="clientNom" />
                </div>
                <div class="dossier-info">
                    <h3 class="dossier-title">{{ titre }}</h3>
                    <p class="dossier-reference">{{ reference }}</p>
                    <span class="dossier-type">{{ typeText }}</span>
                </div>
            </div>

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
                                <span>Voir le dossier</span>
                            </li>
                            <li class="dropdown-item" @mousedown="handleDropdownAction('mark-as-done')">
                                <span>Marquer comme clôturé</span>
                            </li>
                            <li class="dropdown-divider"></li>
                            <li class="dropdown-item dropdown-item-danger" @mousedown="handleDropdownAction('archive')">
                                <span>Archiver</span>
                            </li>
                        </ul>
                    </div>
                </transition>
            </div>
        </div>

        <div class="progress-section">
            <div class="progress-header">
                <span>Progression</span>
                <span class="priority-tag" v-if="priorite !== 'NORMALE'">
                    {{ prioriteText }}
                </span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" :style="`width: ${avancement}%`"></div>
            </div>
            <div class="progress-percentage">{{ avancement }}%</div>
        </div>

        <div class="card-essential-info">
            <div class="info-item">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="info-icon">
                <path fill-rule="evenodd" d="M7.5 6a4.5 4.5 0 1 1 9 0 4.5 4.5 0 0 1-9 0ZM3.751 20.105a8.25 8.25 0 0 1 16.498 0 .75.75 0 0 1-.437.695A18.683 18.683 0 0 1 12 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 0 1-.437-.695Z" clip-rule="evenodd" />
                </svg>
                <span>{{ clientNom }}</span>
            </div>
        
            <div class="info-item">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="info-icon">
                <path fill-rule="evenodd" d="M6.75 2.25A.75.75 0 0 1 7.5 3v1.5h9V3A.75.75 0 0 1 18 3v1.5h.75a3 3 0 0 1 3 3v11.25a3 3 0 0 1-3 3H5.25a3 3 0 0 1-3-3V7.5a3 3 0 0 1 3-3H6V3a.75.75 0 0 1 .75-.75Zm13.5 9a1.5 1.5 0 0 0-1.5-1.5H5.25a1.5 1.5 0 0 0-1.5 1.5v7.5a1.5 1.5 0 0 0 1.5 1.5h13.5a1.5 1.5 0 0 0 1.5-1.5v-7.5Z" clip-rule="evenodd" />
                </svg>
                <span>Ouvert le {{ dateOuverture }}</span>
            </div>
        
            <div class="info-item countdown-container" v-if="!is_archived">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="info-icon">
                    <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25ZM12.75 6a.75.75 0 0 0-1.5 0v6c0 .414.336.75.75.75h4.5a.75.75 0 0 0 0-1.5h-3.75V6Z" clip-rule="evenodd" />
                </svg>
                
                <span 
                    v-if="countdownData"
                    class="countdown-display"
                    :class="countdownData.class"
                    :title="countdownData.tooltip"
                > 
                    <span class="countdown-label">{{ countdownData.label }}</span>
                    {{ countdownData.text }}
                </span>
                <span v-else class="countdown-display countdown-loading">
                    Chargement...
                </span>
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
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useCountdownStore } from '@/stores/counter';

export default {
    name: 'DossierCard',
    props: {
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
        clientNom: {
            type: String,
            default: 'Nom du client'
        },
        clientImage: {
            type: String,
            default: ''
        },
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
        dateOuverture: {
            type: String,
            default: '01/01/2024'
        },
        datefin: {
            type: String,
            default: '31/12/2024'
        },
        avancement: {
            type: Number,
            default: 0,
            validator: (value) => value >= 0 && value <= 100
        },
        documentsCount: {
            type: Number,
            default: 0
        },
        priorite: {
            type: String,
            default: 'NORMALE',
            validator: (value) => ['BASSE', 'NORMALE', 'HAUTE', 'URGENTE'].includes(value)
        },
        es_en_retard:{
            type:Boolean,
            default: false
        },
        is_archived:{
            type:Boolean,
            default: false,
        }
    },
    emits: ['dossier-action', 'view', 'edit', 'mark-as-done', 'archive', 'delete', 'card-click'],
    
    setup(props, { emit }) {
        const showDropdown = ref(false);
        const dropdownRef = ref(null);
        let clickOutsideHandler = null;
        
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
        
        const toggleDropdown = () => {
            showDropdown.value = !showDropdown.value;
            if (showDropdown.value) {
                setTimeout(() => {
                    clickOutsideHandler = (event) => {
                        if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
                            closeDropdown();
                        }
                    };
                    document.addEventListener('mousedown', clickOutsideHandler);
                }, 0);
            } else {
                if (clickOutsideHandler) {
                    document.removeEventListener('mousedown', clickOutsideHandler);
                    clickOutsideHandler = null;
                }
            }
        };
        
        const closeDropdown = () => {
            showDropdown.value = false;
            if (clickOutsideHandler) {
                document.removeEventListener('mousedown', clickOutsideHandler);
                clickOutsideHandler = null;
            }
        };
        
        const handleCardClick = (event) => {
            if (event.target.closest('.options-container') || event.target.closest('.card-actions')) return;
            
            emit('card-click', {
                dossierId: props.dossierId,
                reference: props.reference,
                titre: props.titre
            });
            emit('view', {
                dossierId: props.dossierId,
                reference: props.reference,
                titre: props.titre
            });
        };
        
        const handleDropdownAction = (action) => {
            const dossierData = {
                dossierId: props.dossierId,
                reference: props.reference,
                titre: props.titre,
                action: action
            };
            emit('dossier-action', dossierData);
            switch(action) {
                case 'view': emit('view', dossierData); break;
                case 'mark-as-done': emit('mark-as-done', dossierData); break;
                case 'archive': emit('archive', dossierData); break;
                case 'delete': emit('delete', dossierData); break;
            }
            closeDropdown();
        };
        
        const handleEscapeKey = (event) => {
            if (event.key === 'Escape' && showDropdown.value) closeDropdown();
        };

        // --- GESTION COMPTE A REBOURS & RETARD ---
        const countdownStore = useCountdownStore();
        const countdownData = ref(null);
        const countdownId = computed(() => `dossier-${props.dossierId}`);

        // Fonction pour analyser la date et surcharger les données si en retard
        const processCountdownData = (storeData) => {
            // SI LE DOSSIER EST ARCHIVÉ, NE PAS AFFICHER LE COMPTE À REBOURS
            if (props.estArchive) {
                return {
                    label: 'Archivé',
                    text: '',
                    class: 'countdown-archived',
                    tooltip: 'Dossier archivé'
                };
            }

            if (!storeData) return null;

            // Si le store indique que c'est expiré (retard)
            if (storeData.urgency === 'expired' || storeData.raw?.expired) {
                const days = storeData.raw?.overdue || 0;
                return {
                    ...storeData,
                    label: 'Retard :',
                    text: `${days} jour${days > 1 ? 's' : ''}`, 
                    class: 'countdown-overdue',
                    tooltip: `Dossier en retard de ${days} jours`
                };
            }
            
            // Si ce n'est pas en retard
            return {
                ...storeData,
                label: 'Échéance :'
            };
        };

        const initCountdown = () => {
            // MODIFICATION ICI : On ajoute !props.is_archived dans la condition
            if (props.datefin && !props.is_archived) {
                
                // 1. Récupération initiale immédiate (pour ne pas attendre 1 seconde)
                const staticData = countdownStore.getStaticCountdown(props.datefin);
                // Utilisation directe des données du store (formatées par counter.js)
                countdownData.value = staticData; 
                
                // 2. Lancement du monitoring temps réel
                countdownStore.startCountdown(
                    countdownId.value,
                    props.datefin,
                    (updatedData) => {
                        countdownData.value = updatedData;
                    }
                );
            } else {
                // Si pas de date ou si archivé, on s'assure que c'est vide
                countdownData.value = null;
            }
        };

        watch(() => props.is_archived, (newVal) => {
            if (newVal) {
                // Si le dossier devient archivé, on coupe le compteur
                countdownStore.stopCountdown(countdownId.value);
                countdownData.value = null;
            } else {
                // S'il est désarchivé, on relance
                initCountdown();
            }
        });

        
        onMounted(() => {
            document.addEventListener('keydown', handleEscapeKey);
            initCountdown();
        });
        
        onUnmounted(() => {
            document.removeEventListener('keydown', handleEscapeKey);
            if (clickOutsideHandler) document.removeEventListener('mousedown', clickOutsideHandler);
            countdownStore.stopCountdown(countdownId.value);
        });
        
        return {
            showDropdown,
            dropdownRef,
            statusText,
            statusClass,
            typeText,
            prioriteText,
            isUrgent,
            countdownData,
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
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #e8ecef;
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    max-width: 400px;
    margin: 0 auto;
}

.dossier-card:hover {
    box-shadow: 0 6px 24px rgba(0, 83, 128, 0.15);
    transform: translateY(-4px);
}

.urgent-card {
    border-top: 4px solid #e53e3e;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 1.25rem 1.25rem 1rem;
    background: linear-gradient(135deg, #67acf1 0%, #f1f5f9 100%);
}

.header-left {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    flex: 1;
}

.client-avatar {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #005380 0%, #0077b3 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    border: 3px solid #e6f2f8;
    flex-shrink: 0;
    overflow: hidden;
}

.client-avatar svg {
    width: 30px;
    height: 30px;
    color: white;
}

.client-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.dossier-info {
    flex: 1;
}

.dossier-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #00334d;
    margin: 0 0 4px 0;
    line-height: 1.2;
}

.dossier-reference {
    color: #0077b3;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 0 0 8px 0;
}

.dossier-type {
    display: inline-block;
    font-size: 0.9rem;
    color: #005380;
    font-weight: 500;
    padding: 4px 12px;
    background: #e6f2f8;
    border-radius: 12px;
}

.options-container {
    position: relative;
    z-index: 10;
}

.options-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 8px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
    color: #718096;
}

.options-btn:hover {
    background-color: #edf2f7;
    color: #005380;
}

.options-btn svg {
    width: 24px;
    height: 24px;
}

.dropdown-menu {
    position: absolute;
    top: 100%;
    right: 0;
    z-index: 1000;
    min-width: 200px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    border: 1px solid #e2e8f0;
    margin-top: 8px;
    overflow: hidden;
}

.dropdown-list {
    list-style: none;
    padding: 8px 0;
    margin: 0;
}

.dropdown-item {
    padding: 12px 16px;
    cursor: pointer;
    transition: background-color 0.2s;
    font-size: 0.9rem;
    color: #4a5568;
    font-weight: 500;
}

.dropdown-item:hover {
    background-color: #f7fafc;
    color: #005380;
}

.dropdown-divider {
    height: 1px;
    background: #e2e8f0;
    margin: 8px 0;
}

.dropdown-item-danger {
    color: #e53e3e;
}

.dropdown-item-danger:hover {
    background-color: #fed7d7;
}

.progress-section {
    padding: 1.2rem 1.5rem 0.8rem;
}

.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    font-size: 0.9rem;
    color: #4a5568;
    font-weight: 600;
}

.priority-tag {
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 700;
    background: #fee;
    color: #e53e3e;
}

.progress-bar {
    width: 100%;
    height: 8px;
    background: #e2e8f0;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 8px;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #005380, #0077b3);
    border-radius: 4px;
    transition: width 0.5s ease;
}

.progress-percentage {
    text-align: right;
    font-size: 0.9rem;
    color: #005380;
    font-weight: 600;
}

.card-essential-info {
    padding: 1rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 10px;
    border-top: 1px solid #eaeaea;
}

.info-item {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #555;
    font-size: 0.9rem;
}

.info-icon {
    width: 18px;
    height: 18px;
    color: #005380;
    flex-shrink: 0;
}

/* Styles spécifiques pour le compte à rebours */
.countdown-container {
    margin-top: 2px;
}

.countdown-display {
    display: flex;
    align-items: center;
    gap: 5px;
}

.countdown-label {
    opacity: 0.9;
}

.countdown-loading {
    color: #999;
    font-style: italic;
    font-size: 0.85rem;
}

/* Style pour le RETARD */
.countdown-overdue {
    background-color: #ffeaea;
    color: #d32f2f;
    border: 1px solid #ffcdd2;
    padding: 2px 8px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.85rem;
    margin-left: -8px; /* Compenser le padding pour l'alignement visuel */
    animation: pulse-red 2s infinite ease-in-out;
}

@keyframes pulse-red {
    0% { box-shadow: 0 0 0 0 rgba(229, 62, 62, 0.4); }
    70% { box-shadow: 0 0 0 6px rgba(229, 62, 62, 0); }
    100% { box-shadow: 0 0 0 0 rgba(229, 62, 62, 0); }
}

.card-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid #eaeaea;
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
    color: #005380;
}

.status-badge {
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    color: white;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-nouveau { background: #3498db; }
.status-en_cours { background: #2ecc71; }
.status-en_attente { background: #f39c12; }
.status-bloque { background: #e74c3c; }
.status-termine { background: #27ae60; }
.status-cloture { background: #95a5a6; }
.status-annule { background: #7f8c8d; }

@media (max-width: 480px) {
    .dossier-card {
        max-width: 100%;
    }
    
    .card-header {
        flex-direction: column;
        gap: 1rem;
    }
    
    .card-footer {
        flex-direction: column;
        gap: 0.75rem;
        align-items: stretch;
    }
    
    .documents-info {
        justify-content: center;
    }
    
    .status-badge {
        align-self: center;
    }
    
    .dropdown-menu {
        position: fixed;
        right: 1rem;
        left: 1rem;
        bottom: 1rem;
        top: auto;
        max-height: 50vh;
        overflow-y: auto;
    }
}
</style>