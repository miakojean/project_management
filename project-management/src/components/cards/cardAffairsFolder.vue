<template>
    <div class="dossier-card" :class="{'urgent-card': isUrgent}">
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
            <div class="status-badge" :class="statusClass">
                {{ statusText }}
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
                <span class="label">Ouverture:</span>
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
            </div>
        </div>

        <div class="card-footer">
            <div class="documents-info">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="doc-icon">
                    <path d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0 0 16.5 9h-1.875a1.875 1.875 0 0 1-1.875-1.875V5.25A3.75 3.75 0 0 0 9 1.5H5.625Z" />
                </svg>
                {{ documentsCount }} document(s)
            </div>
            <div class="priority-tag" v-if="priorite !== 'NORMALE'">
                {{ prioriteText }}
            </div>
        </div>
    </div>
</template>

<script>
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
    computed: {
        statusText() {
            const statusMap = {
                'NOUVEAU': 'Nouveau',
                'EN_COURS': 'En cours',
                'EN_ATTENTE': 'En attente',
                'BLOQUE': 'Bloqué',
                'TERMINE': 'Terminé',
                'CLOTURE': 'Clôturé',
                'ANNULE': 'Annulé'
            };
            return statusMap[this.statut] || this.statut;
        },
        
        statusClass() {
            return `status-${this.statut.toLowerCase()}`;
        },
        
        typeText() {
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
            return typeMap[this.typeDossier] || this.typeDossier;
        },
        
        prioriteText() {
            const prioriteMap = {
                'BASSE': 'Basse priorité',
                'NORMALE': 'Normale',
                'HAUTE': 'Haute priorité',
                'URGENTE': 'Urgent'
            };
            return prioriteMap[this.priorite] || this.priorite;
        },
        
        isUrgent() {
            return this.priorite === 'URGENTE';
        }
    }
}
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
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.priority-tag {
    background: #fed7d7;
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
}
</style>