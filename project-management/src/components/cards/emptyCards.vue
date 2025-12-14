<template>
    <div class="empty-folder-card" :class="{ 'has-action': showAction }">
        <div class="empty-folder__illustration">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 120" class="empty-folder__svg">
                <!-- Dossier principal -->
                <path d="M40 30h120q8 0 8 8v60q0 8-8 8H40q-8 0-8-8V38q0-8 8-8z" 
                      fill="#e0f2fe" stroke="#0ea5e9" stroke-width="2"/>
                
                <!-- Onglet du dossier -->
                <path d="M50 30h40v-8q0-4 4-4h12q4 0 4 4v8" 
                      fill="#f8fafc" stroke="#0ea5e9" stroke-width="1.5"/>
                
                <!-- Pages vides -->
                    <path d="M60 45h80v50H60z" fill="white" stroke="#cbd5e1" stroke-width="1.2" opacity="0.9"/>
                
                <!-- Page décalée -->
                    <path d="M65 50h70v45H65z" fill="white" stroke="#cbd5e1" stroke-width="1" opacity="0.7"/>
                
                <!-- Icône document vide -->
                <g transform="translate(90 65)">
                    <path d="M5 0h20v15H5z" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1"/>
                    <line x1="8" y1="5" x2="17" y2="5" stroke="#94a3b8" stroke-width="0.8"/>
                    <line x1="8" y1="8" x2="17" y2="8" stroke="#94a3b8" stroke-width="0.8"/>
                    <line x1="8" y1="11" x2="14" y2="11" stroke="#94a3b8" stroke-width="0.8"/>
                </g>
                
                <!-- Point d'interrogation subtil -->
                <g transform="translate(105 75)" opacity="0.3">
                    <circle cx="0" cy="0" r="4" fill="#94a3b8"/>
                    <text x="0" y="1.5" text-anchor="middle" fill="white" font-size="4" font-weight="bold">?</text>
                </g>
                
                <!-- Animation pulse -->
                <circle cx="100" cy="60" r="25" fill="none" stroke="#0ea5e9" stroke-width="1" 
                        stroke-dasharray="3 3" opacity="0.2" class="pulse-circle"/>
            </svg>
        </div>
        
        <div class="empty-folder__content">
            <h3 class="empty-folder__title">{{ title }}</h3>
            <p class="empty-folder__description">{{ description }}</p>
            
            <div v-if="showAction && actionText" class="empty-folder__actions">
                <button @click="handleAction" 
                        class="empty-folder__btn" 
                        :class="buttonVariant"
                        :aria-label="actionText">
                    <svg v-if="showIcon" class="btn-icon" viewBox="0 0 16 16" fill="currentColor">
                        <path d="M8 2a1 1 0 0 1 1 1v4h4a1 1 0 1 1 0 2H9v4a1 1 0 1 1-2 0V9H3a1 1 0 0 1 0-2h4V3a1 1 0 0 1 1-1z"/>
                    </svg>
                    {{ actionText }}
                </button>
                
                <!-- Indicateur subtil -->
                <div v-if="showHint" class="empty-folder__hint">
                    <svg viewBox="0 0 16 16" width="12" height="12" fill="#64748b">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0-1A6 6 0 1 0 8 2a6 6 0 0 0 0 12z"/>
                        <path d="M8 11a1 1 0 0 1-1-1V7a1 1 0 0 1 2 0v3a1 1 0 0 1-1 1zm0-7a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
                    </svg>
                    <span>{{ hintText }}</span>
                </div>
            </div>
        </div>
        
        <!-- Micro-interaction -->
        <div class="empty-folder__micro-interaction" v-if="showMicroInteraction">
            <div class="micro-dot"></div>
            <div class="micro-dot"></div>
            <div class="micro-dot"></div>
        </div>
    </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'

// Props
const props = defineProps({
    title: {
        type: String,
        default: 'Dossier vide'
    },
    description: {
        type: String,
        default: 'Commencez par ajouter votre premier document.'
    },
    actionText: {
        type: String,
        default: 'Ajouter un document'
    },
    showAction: {
        type: Boolean,
        default: true
    },
    variant: {
        type: String,
        default: 'primary',
        validator: (value) => ['primary', 'secondary', 'outline'].includes(value)
    },
    showIcon: {
        type: Boolean,
        default: true
    },
    showHint: {
        type: Boolean,
        default: false
    },
    hintText: {
        type: String,
        default: 'Cliquez pour commencer'
    },
    showMicroInteraction: {
        type: Boolean,
        default: true
    },
    autoAnimate: {
        type: Boolean,
        default: true
    }
})

// Emits
const emit = defineEmits(['action'])

// State
const isHovered = ref(false)

// Computed
const buttonVariant = computed(() => `empty-folder__btn--${props.variant}`)

// Methods
const handleAction = () => {
    // Animation de feedback
    if (props.autoAnimate) {
        const btn = event?.currentTarget
        if (btn) {
            btn.style.transform = 'scale(0.95)'
            setTimeout(() => {
                btn.style.transform = ''
            }, 150)
        }
    }
    emit('action')
}

// Animation au montage
onMounted(() => {
    if (props.autoAnimate) {
        setTimeout(() => {
            isHovered.value = true
        }, 300)
    }
})
</script>

<style scoped>
.empty-folder-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2.5rem 2rem;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border: 2px dashed #cbd5e1;
    border-radius: 16px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    min-height: 280px;
    position: relative;
    overflow: hidden;
    cursor: default;
    width: 100%;
}

.empty-folder-card.has-action {
    cursor: pointer;
}

.empty-folder-card:hover {
    border-color: #0ea5e9;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(14, 165, 233, 0.1);
}

.empty-folder__illustration {
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}

.empty-folder__svg {
    width: 140px;
    height: 84px;
    transition: all 0.4s ease;
}

.empty-folder-card:hover .empty-folder__svg {
    transform: scale(1.05) translateY(-3px);
}

.pulse-circle {
    animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 0.2; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(1.05); }
}

.empty-folder__content {
    max-width: 320px;
}

.empty-folder__title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #0f172a;
    margin: 0 0 0.5rem 0;
    line-height: 1.3;
    background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.empty-folder__description {
    color: #64748b;
    font-size: 0.95rem;
    line-height: 1.5;
    margin: 0 0 1.75rem 0;
    opacity: 0.9;
}

.empty-folder__actions {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
}

.empty-folder__btn {
    padding: 0.75rem 1.75rem;
    border: none;
    border-radius: 10px;
    font-weight: 500;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    position: relative;
    overflow: hidden;
}

.empty-folder__btn::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 5px;
    height: 5px;
    background: rgba(255, 255, 255, 0.5);
    opacity: 0;
    border-radius: 100%;
    transform: scale(1, 1) translate(-50%);
    transform-origin: 50% 50%;
}

.empty-folder__btn:focus:not(:active)::after {
    animation: ripple 1s ease-out;
}

@keyframes ripple {
    0% { transform: scale(0, 0); opacity: 0.5; }
    100% { transform: scale(20, 20); opacity: 0; }
}

.empty-folder__btn--primary {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.empty-folder__btn--primary:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.35);
}

.empty-folder__btn--primary:active {
    transform: translateY(0);
}

.empty-folder__btn--secondary {
    background: linear-gradient(135deg, #64748b 0%, #475569 100%);
    color: white;
}

.empty-folder__btn--secondary:hover {
    background: linear-gradient(135deg, #475569 0%, #334155 100%);
    transform: translateY(-2px);
}

.empty-folder__btn--outline {
    background: transparent;
    color: #3b82f6;
    border: 2px solid #3b82f6;
    font-weight: 600;
}

.empty-folder__btn--outline:hover {
    background: #3b82f6;
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(59, 130, 246, 0.2);
}

.btn-icon {
    width: 16px;
    height: 16px;
    transition: transform 0.2s ease;
}

.empty-folder__btn:hover .btn-icon {
    transform: rotate(90deg);
}

.empty-folder__hint {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: #64748b;
    opacity: 0.7;
    animation: fadeInUp 0.6s ease 0.5s both;
}

.empty-folder__micro-interaction {
    position: absolute;
    bottom: 1rem;
    display: flex;
    gap: 4px;
    opacity: 0;
    animation: fadeIn 0.5s ease 1s both;
}

.micro-dot {
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: #cbd5e1;
    animation: bounce 1.4s ease-in-out infinite;
}

.micro-dot:nth-child(2) { animation-delay: 0.2s; }
.micro-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-5px); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 0.7; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 0.5; }
}

/* Responsive */
@media (max-width: 768px) {
    .empty-folder-card {
        padding: 2rem 1.5rem;
        min-height: 240px;
    }
    
    .empty-folder__svg {
        width: 120px;
        height: 72px;
    }
    
    .empty-folder__title {
        font-size: 1.125rem;
    }
    
    .empty-folder__description {
        font-size: 0.9rem;
    }
    
    .empty-folder__btn {
        padding: 0.7rem 1.5rem;
        font-size: 0.9rem;
    }
}

/* Réduction pour intégration */
@media (max-width: 480px) {
    .empty-folder-card {
        padding: 1.5rem 1rem;
        min-height: 200px;
    }
    
    .empty-folder__svg {
        width: 100px;
        height: 60px;
    }
}

/* Mode sombre support */
@media (prefers-color-scheme: dark) {
    .empty-folder-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-color: #475569;
    }
    
    .empty-folder-card:hover {
        border-color: #38bdf8;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    .empty-folder__title {
        background: linear-gradient(135deg, #f1f5f9 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        background-clip: text;
    }
    
    .empty-folder__description {
        color: #94a3b8;
    }
}
</style>