<template>
    <div class="empty-folder-card">
        <div class="empty-folder__icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 6V18C3 19.6569 4.34315 21 6 21H18C19.6569 21 21 19.6569 21 18V9C21 7.34315 19.6569 6 18 6H13L11 4H6C4.34315 4 3 4.34315 3 6Z" 
                    stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
                />
                <path d="M15 13L12 16M12 16L9 13M12 16V10" 
                    stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
                />
            </svg>
        </div>
        
        <div class="empty-folder__content">
            <h3 class="empty-folder__title">{{ title }}</h3>
            <p class="empty-folder__description">{{ description }}</p>
            
            <div v-if="showAction && actionText" class="empty-folder__actions">
                <button @click="handleAction" class="empty-folder__btn" :class="buttonVariant">
                    {{ actionText }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
    title: {
        type: String,
        default: 'Dossier vide'
    },
    description: {
        type: String,
        default: 'Aucun élément à afficher pour le moment.'
    },
    actionText: {
        type: String,
        default: 'Ajouter un élément'
    },
    showAction: {
        type: Boolean,
        default: true
    },
    variant: {
        type: String,
        default: 'primary', // 'primary', 'secondary', 'outline'
        validator: (value) => ['primary', 'secondary', 'outline'].includes(value)
    },
    iconSize: {
        type: String,
        default: 'medium', // 'small', 'medium', 'large'
        validator: (value) => ['small', 'medium', 'large'].includes(value)
    }
})

// Emits
const emit = defineEmits(['action'])

// Computed
const buttonVariant = computed(() => `empty-folder__btn--${props.variant}`)
const iconSizeClass = computed(() => `empty-folder__icon--${props.iconSize}`)

// Methods
const handleAction = () => {
    emit('action')
}
</script>

<style scoped>
.empty-folder-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 3rem 2rem;
    background: white;
    border: 2px dashed #e2e8f0;
    border-radius: 12px;
    transition: all 0.3s ease;
    min-height: 300px;
    cursor: default;
}

.empty-folder-card:hover {
    border-color: #cbd5e1;
    background: #f8fafc;
}

.empty-folder__icon {
    color: #94a3b8;
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}

.empty-folder-card:hover .empty-folder__icon {
    color: #64748b;
    transform: scale(1.05);
}

.empty-folder__icon--small {
    width: 48px;
    height: 48px;
}

.empty-folder__icon--medium {
    width: 64px;
    height: 64px;
}

.empty-folder__icon--large {
    width: 80px;
    height: 80px;
}

.empty-folder__content {
    max-width: 300px;
}

.empty-folder__title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1e293b;
    margin: 0 0 0.75rem 0;
    line-height: 1.4;
}

.empty-folder__description {
    color: #64748b;
    font-size: 0.95rem;
    line-height: 1.5;
    margin: 0 0 1.5rem 0;
}

.empty-folder__actions {
    margin-top: 1rem;
}

.empty-folder__btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.empty-folder__btn--primary {
    background: #3b82f6;
    color: white;
}

.empty-folder__btn--primary:hover {
    background: #2563eb;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.empty-folder__btn--secondary {
    background: #64748b;
    color: white;
}

.empty-folder__btn--secondary:hover {
    background: #475569;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(100, 116, 139, 0.3);
}

.empty-folder__btn--outline {
    background: transparent;
    color: #3b82f6;
    border: 1.5px solid #3b82f6;
}

.empty-folder__btn--outline:hover {
    background: #3b82f6;
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

/* Responsive */
@media (max-width: 768px) {
    .empty-folder-card {
        padding: 2rem 1.5rem;
        min-height: 250px;
    }
    
    .empty-folder__title {
        font-size: 1.125rem;
    }
    
    .empty-folder__description {
        font-size: 0.9rem;
    }
}

/* Animation optionnelle */
@keyframes gentlePulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
}

.empty-folder-card.pulsing {
    animation: gentlePulse 3s ease-in-out infinite;
}
</style>