<template>
    <button 
        class="btn-primary" 
        :class="sizeClass"
        @click="$emit('add-document')"
        :style="customStyle"
    >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" :class="iconSizeClass">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
        <span class="btn-label">{{ label }}</span>
    </button>
</template>

<script>
export default {
    name: 'AddDocumentButton',
    props: {
        size: {
            type: String,
            default: 'medium',
            validator: (value) => ['xsmall', 'small', 'medium', 'large', 'xlarge'].includes(value)
        },
        label: {
            type: String,
            default: 'Ajouter client'
        },
        fullWidth: {
            type: Boolean,
            default: false
        },
        customPadding: {
            type: String,
            default: null
        },
        fontSize: {
            type: String,
            default: null
        }
    },
    computed: {
        sizeClass() {
            return `btn-${this.size}`;
        },
        iconSizeClass() {
            const iconSizes = {
                xsmall: 'icon-xs',
                small: 'icon-sm',
                medium: 'icon-md',
                large: 'icon-lg',
                xlarge: 'icon-xl'
            };
            return iconSizes[this.size];
        },
        customStyle() {
            const styles = {};
            if (this.fullWidth) {
                styles.width = '100%';
                styles.justifyContent = 'center';
            }
            if (this.customPadding) {
                styles.padding = this.customPadding;
            }
            if (this.fontSize) {
                styles.fontSize = this.fontSize;
            }
            return styles;
        }
    },
    emits: ['add-document']
}
</script>

<style scoped>
/* Classes de base */
.btn-primary {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    border-radius: 0.5rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    background: var(--primary-color, #3b82f6);
    color: white;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.5;
    white-space: nowrap;
}

.btn-primary:hover {
    background: var(--primary-color-dark, #2563eb);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-primary:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.btn-primary:focus {
    outline: 2px solid var(--primary-color, #3b82f6);
    outline-offset: 2px;
}

.btn-primary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

/* Tailles prédéfinies */

/* Extra Small */
.btn-xsmall {
    padding: 0.375rem 0.75rem;
    font-size: 0.75rem;
    min-height: 28px;
}

/* Small */
.btn-small {
    padding: 0.5rem 1rem;
    font-size: 0.8125rem;
    min-height: 36px;
}

/* Medium (par défaut) */
.btn-medium {
    padding: 0.625rem 1.25rem;
    font-size: 0.875rem;
    min-height: 42px;
}

/* Large */
.btn-large {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    min-height: 48px;
}

/* Extra Large */
.btn-xlarge {
    padding: 1rem 2rem;
    font-size: 1.125rem;
    min-height: 56px;
}

/* Taille des icônes */
.icon-xs {
    width: 12px;
    height: 12px;
    stroke-width: 2;
}

.icon-sm {
    width: 14px;
    height: 14px;
    stroke-width: 1.8;
}

.icon-md {
    width: 16px;
    height: 16px;
    stroke-width: 1.6;
}

.icon-lg {
    width: 18px;
    height: 18px;
    stroke-width: 1.4;
}

.icon-xl {
    width: 20px;
    height: 20px;
    stroke-width: 1.2;
}

/* Label */
.btn-label {
    flex-shrink: 0;
}

/* Variante plein largeur */
.btn-full-width {
    width: 100%;
    justify-content: center;
}

/* Responsive */
@media (max-width: 768px) {
    .btn-xlarge {
        padding: 0.875rem 1.75rem;
        font-size: 1rem;
        min-height: 52px;
    }
    
    .btn-large {
        padding: 0.675rem 1.25rem;
        font-size: 0.9375rem;
        min-height: 44px;
    }
    
    .btn-medium {
        padding: 0.5rem 1rem;
        font-size: 0.8125rem;
        min-height: 38px;
    }
}

/* Animation pour loading state (optionnel) */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.btn-primary.loading {
    animation: pulse 1.5s ease-in-out infinite;
    pointer-events: none;
}
</style>