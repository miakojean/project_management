<template>
    <article class="album-card">
        <!-- Cover (partie image/icône) -->
        <div class="album-card__cover">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="cover-icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008Zm0 3h.008v.008h-.008v-.008Zm0 3h.008v.008h-.008v-.008Z" />
            </svg>
        </div>
        <!-- Informations (partie texte) -->
        <div class="album-card__info">
            <header class="info-header">
                <h3 class="card-title">{{ title }}</h3>
                <span class="card-badge" :class="statusClass">{{ statusText }}</span>
            </header>
            
            <div class="info-content">
                <p class="card-description">{{ description }}</p>
                
                <div class="card-meta">
                    <div class="meta-item">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="meta-icon">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
                        </svg>
                        <span>{{ date }}</span>
                    </div>
                    
                    <div class="meta-item">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="meta-icon">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
                        </svg>
                        <span>{{ clientName }}</span>
                    </div>

                    <div class="meta-item">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="meta-icon">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5c1.657 0 3 1.343 3 3S13.657 10.5 12 10.5 9 9.157 9 7.5s1.343-3 3-3zm0 9c4.418 0 8.25 1.79 8.25 4v1.5H3.75V17.5c0-2.21 3.832-4 8.25-4z" />
                        </svg>
                        <span> Créé par {{ creatorName }}</span>
                    </div>
                </div>
            </div>

            <footer class="info-footer">
                <div class="progress-indicator">
                    <div class="progress-bar">
                        <div class="progress-fill" :style="{ width: progress + '%' }"></div>
                    </div>
                    <span class="progress-text">{{ progress }}% complété</span>
                </div>
            </footer>
        </div>
    </article>
</template>

<script>
export default {
    name: 'AlbumCard',
    props: {
        title: {
            type: String,
            default: "Nom du dossier"
        },
        description: {
            type: String,
            default: "Description courte du dossier ou projet..."
        },
        status: {
            type: String,
            default: "active", // active, completed, pending, cancelled
            validator: (value) => ['active', 'completed', 'pending', 'cancelled'].includes(value)
        },
        date: {
            type: String,
            default: "15 Jan 2024"
        },
        clientName: {
            type: String,
            default: "Client Name"
        },
        creatorName: {
            type: String,
            default: 'Utilisateur'
        },
        progress: {
            type: Number,
            default: 75,
            validator: (value) => value >= 0 && value <= 100
        }
    },
    computed: {
        statusText() {
            const statusMap = {
                active: "En cours",
                completed: "Terminé",
                pending: "En attente",
                cancelled: "Annulé"
            }
            return statusMap[this.status] || this.status
        },
        statusClass() {
            return `badge--${this.status}`
        }
    },
    emits: ['view', 'edit', 'action']
}
</script>

<style scoped>
.album-card {
    max-width: 400px;
    background: #ffffff;
    border-radius: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: all 0.3s ease;
    border: 1px solid #e2e8f0;
}

.album-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

/* Partie Cover */
.album-card__cover {
    position: relative;
    height: 200px;
background: linear-gradient(135deg, #59acd8 20%, #125b82 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.cover-icon {
    width: 80px;
    height: 80px;
    color: rgba(255, 255, 255, 0.9);
}

.cover-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.album-card__cover:hover .cover-overlay {
    opacity: 1;
}

.action-btn {
    background: rgba(255, 255, 255, 0.9);
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
}

.action-btn:hover {
    background: white;
    transform: scale(1.1);
}

.action-icon {
    width: 18px;
    height: 18px;
    color: #333;
}

/* Partie Informations */
.album-card__info {
    padding: 1.5rem;
}

.info-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1a202c;
    margin: 0;
    line-height: 1.3;
}

.card-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.75rem;
    font-weight: 500;
    white-space: nowrap;
}

.badge--active {
    background: #2ECC71;
    color: #ffffff;
}

.badge--completed {
    background: var(--primary-color);
    color: #ffffff;
}

.badge--pending {
    background: #fffaf0;
    color: #744210;
}

.badge--cancelled {
    background: #fed7d7;
    color: #c53030;
}

.info-content {
    margin-bottom: 1.5rem;
}

.card-description {
    color: #718096;
    font-size: 0.9rem;
    line-height: 1.5;
    margin: 0 0 1rem 0;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.card-meta {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #718096;
    font-size: 0.85rem;
}

.meta-icon {
    width: 16px;
    height: 16px;
}

/* Footer */
.info-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.progress-indicator {
    flex: 1;
}

.progress-bar {
    width: 100%;
    height: 6px;
    background: #e2e8f0;
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 0.25rem;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #00a2ff, #0088d4);
    border-radius: 3px;
    transition: width 0.3s ease;
}

.progress-text {
    font-size: 0.8rem;
    color: #718096;
}

.quick-action-btn {
    background: none;
    border: none;
    padding: 0.5rem;
    border-radius: 0.5rem;
    cursor: pointer;
    color: #00a2ff;
    transition: all 0.2s ease;
}

.quick-action-btn:hover {
    background: #f7fafc;
    color: #0088d4;
}

.quick-action-btn .action-icon {
    width: 16px;
    height: 16px;
}
</style>