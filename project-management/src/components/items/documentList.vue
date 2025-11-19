<template>
    <div class="document-list-container">
        <!-- Header avec actions globales -->
        <div class="header-section">
            <h4 class="section-title">Documents du dossier</h4>
        </div>

        <!-- Liste des documents -->
        <ul class="document-list">
            <li class="document-item" v-for="doc in documents" :key="doc.id">
                <!-- Icône du document avec indicateur de type -->
                <div class="document-icon" :style="{ background: doc.colorBg }">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" :style="{ color: doc.color }">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                    </svg>
                    <span class="document-extension">{{ doc.extension }}</span>
                </div>

                <!-- Informations du document -->
                <div class="document-info">
                    <div class="document-header">
                        <h4 class="document-title">{{ doc.title }}</h4>
                        <span class="document-badge" :class="doc.statusClass">{{ doc.status }}</span>
                    </div>
                    
                    <!-- Métadonnées -->
                    <div class="document-meta">
                        <span class="meta-item">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-xs">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                            {{ doc.uploadDate }}
                        </span>
                        
                        <span class="meta-item">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-xs">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                            </svg>
                            {{ doc.uploadedBy }}
                        </span>

                        <span class="meta-item">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-xs">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 0 0-1.883 2.542l.857 6a2.25 2.25 0 0 0 2.227 1.932H19.05a2.25 2.25 0 0 0 2.227-1.932l.857-6a2.25 2.25 0 0 0-1.883-2.542m-16.5 0V6A2.25 2.25 0 0 1 6 3.75h3.879a1.5 1.5 0 0 1 1.06.44l2.122 2.12a1.5 1.5 0 0 0 1.06.44H18A2.25 2.25 0 0 1 20.25 9v.776" />
                            </svg>
                            {{ doc.size }}
                        </span>
                    </div>
                </div>

                <!-- Actions du document -->
                <div class="document-actions">
                    <button class="action-btn action-download" @click="downloadDocument(doc.id)" title="Télécharger">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                        </svg>
                    </button>

                    <button class="action-btn action-view" @click="viewDocument(doc.id)" title="Visualiser">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                        </svg>
                    </button>

                    <button class="action-btn action-share" @click="shareDocument(doc.id)" title="Partager">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M7.217 10.907a2.25 2.25 0 1 0 0 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186 9.566-5.314m-9.566 7.5 9.566 5.314m0 0a2.25 2.25 0 1 0 3.935 2.186 2.25 2.25 0 0 0-3.935-2.186Zm0-12.814a2.25 2.25 0 1 0 3.933-2.185 2.25 2.25 0 0 0-3.933 2.185Z" />
                        </svg>
                    </button>

                    <button class="action-btn action-more" @click="toggleMenu(doc.id)" title="Plus d'options">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM12.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM18.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
                        </svg>
                    </button>
                </div>
            </li>
        </ul>

        <!-- État vide -->
        <div v-if="documents.length === 0" class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="empty-icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
            </svg>
            <h3>Aucun document</h3>
            <p>Commencez par ajouter un document à ce dossier</p>
            <button class="btn-primary">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-sm">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                </svg>
                Ajouter le premier document
            </button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DocumentList',
    data() {
        return {
            documents: [
                {
                    id: 1,
                    title: 'Cahier de charges du logiciel de gestion de documents',
                    uploadDate: '19 Nov 2024, 10:58',
                    uploadedBy: 'Jean Kouassi',
                    size: '2.4 Mo',
                    extension: 'PDF',
                    status: 'Validé',
                    statusClass: 'status-validated',
                    color: '#e74c3c',
                    colorBg: 'rgba(231, 76, 60, 0.1)'
                },
                {
                    id: 2,
                    title: 'Statuts de la société ACME SARL',
                    uploadDate: '18 Nov 2024, 14:30',
                    uploadedBy: 'Marie Yao',
                    size: '1.8 Mo',
                    extension: 'PDF',
                    status: 'Signé',
                    statusClass: 'status-signed',
                    color: '#3498db',
                    colorBg: 'rgba(52, 152, 219, 0.1)'
                },
                
            ]
        }
    },
    methods: {
        downloadDocument(id) {
            console.log('Télécharger document:', id);
            // Logique de téléchargement
        },
        viewDocument(id) {
            console.log('Visualiser document:', id);
            // Logique de visualisation
        },
        shareDocument(id) {
            console.log('Partager document:', id);
            // Logique de partage
        },
        toggleMenu(id) {
            console.log('Menu document:', id);
            // Logique du menu contextuel
        }
    }
}
</script>

<style scoped>
.document-list-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    width: 100%;
}

/* Header Section */
.header-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e5e7eb;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #1f2937;
    margin: 0;
}

.header-actions {
    display: flex;
    gap: 0.75rem;
}

/* Buttons */
.btn-primary, .btn-secondary {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.625rem 1.25rem;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
}

.btn-primary {
    background: var(--primary-color, #3b82f6);
    color: white;
}

.btn-primary:hover {
    background: var(--primary-color-dark, #2563eb);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-secondary {
    background: #f3f4f6;
    color: #374151;
}

.btn-secondary:hover {
    background: #e5e7eb;
}

/* Document List */
.document-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    list-style: none;
    padding: 0;
    margin: 0;
}

.document-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1.25rem;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 0.75rem;
    transition: all 0.2s ease;
    cursor: pointer;
}

.document-item:hover {
    border-color: var(--primary-color, #3b82f6);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
}

/* Document Icon */
.document-icon {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 60px;
    height: 60px;
    border-radius: 0.75rem;
    flex-shrink: 0;
}

.document-icon svg {
    width: 28px;
    height: 28px;
}

.document-extension {
    position: absolute;
    bottom: -4px;
    right: -4px;
    background: white;
    padding: 0.125rem 0.375rem;
    border-radius: 0.25rem;
    font-size: 0.625rem;
    font-weight: 600;
    border: 1px solid #e5e7eb;
}

/* Document Info */
.document-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    min-width: 0;
}

.document-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
}

.document-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: #1f2937;
    margin: 0;
    word-break: break-word;
}

.document-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
    white-space: nowrap;
}

.status-validated {
    background: #dcfce7;
    color: #166534;
}

.status-signed {
    background: #dbeafe;
    color: #1e40af;
}

.status-pending {
    background: #fef3c7;
    color: #92400e;
}

.document-description {
    font-size: 0.875rem;
    color: #6b7280;
    margin: 0;
    line-height: 1.5;
}

.document-meta {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    flex-wrap: wrap;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 0.375rem;
    font-size: 0.813rem;
    color: #6b7280;
}

/* Document Actions */
.document-actions {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-shrink: 0;
}

.action-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 0.5rem;
    border: 1px solid #e5e7eb;
    background: white;
    color: #6b7280;
    cursor: pointer;
    transition: all 0.2s ease;
}

.action-btn svg {
    width: 18px;
    height: 18px;
}

.action-btn:hover {
    border-color: var(--primary-color, #3b82f6);
    color: var(--primary-color, #3b82f6);
    background: rgba(59, 130, 246, 0.05);
}

.action-download:hover {
    border-color: #10b981;
    color: #10b981;
    background: rgba(16, 185, 129, 0.05);
}

.action-view:hover {
    border-color: #3b82f6;
    color: #3b82f6;
    background: rgba(59, 130, 246, 0.05);
}

.action-share:hover {
    border-color: #f59e0b;
    color: #f59e0b;
    background: rgba(245, 158, 11, 0.05);
}

/* Icons */
.icon-sm {
    width: 18px;
    height: 18px;
}

.icon-xs {
    width: 16px;
    height: 16px;
}

/* Empty State */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    text-align: center;
}

.empty-icon {
    width: 80px;
    height: 80px;
    color: #d1d5db;
    margin-bottom: 1.5rem;
}

.empty-state h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1f2937;
    margin: 0 0 0.5rem 0;
}

.empty-state p {
    font-size: 0.875rem;
    color: #6b7280;
    margin: 0 0 1.5rem 0;
}

/* Responsive */
@media (max-width: 768px) {
    .header-section {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }

    .header-actions {
        width: 100%;
        flex-direction: column;
    }

    .btn-primary, .btn-secondary {
        width: 100%;
        justify-content: center;
    }

    .document-item {
        flex-direction: column;
        gap: 1rem;
    }

    .document-actions {
        width: 100%;
        justify-content: flex-end;
    }

    .document-meta {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }
}
</style>