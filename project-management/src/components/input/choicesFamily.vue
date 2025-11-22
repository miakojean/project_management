<template>
    <div class="entity-type-selector">
        <!-- Label -->
        <label v-if="label" class="entity-type__label">
            {{ label }}
            <span v-if="required" class="required-asterisk">*</span>
        </label>

        <!-- Conteneur des options -->
        <div class="entity-type__options">
            <!-- Option Personne Physique -->
            <div 
                class="entity-option"
                :class="{
                    'entity-option--selected': selectedValue === 'physical',
                    'entity-option--disabled': disabled
                }"
                @click="selectOption('physical')"
            >
                <div class="entity-option__icon">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                    </svg>
                </div>
                <div class="entity-option__content">
                    <h4 class="entity-option__title">Personne Physique</h4>
                    <p class="entity-option__description">Client individuel</p>
                </div>
                <div class="entity-option__indicator">
                    <div class="indicator" :class="{ 'indicator--active': selectedValue === 'physical' }"></div>
                </div>
            </div>

            <!-- Option Personne Morale -->
            <div 
                class="entity-option"
                :class="{
                    'entity-option--selected': selectedValue === 'legal',
                    'entity-option--disabled': disabled
                }"
                @click="selectOption('legal')"
            >
                <div class="entity-option__icon">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008Zm0 3h.008v.008h-.008v-.008Zm0 3h.008v.008h-.008v-.008Z" />
                    </svg>
                </div>
                <div class="entity-option__content">
                    <h4 class="entity-option__title">Personne Morale</h4>
                    <p class="entity-option__description">Entreprise, Société, Association</p>
                </div>
                <div class="entity-option__indicator">
                    <div class="indicator" :class="{ 'indicator--active': selectedValue === 'legal' }"></div>
                </div>
            </div>
        </div>

        <!-- Message d'erreur -->
        <div v-if="error" class="entity-type__error">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
            </svg>
            {{ error }}
        </div>

        <!-- Message d'aide -->
        <div v-if="helpText" class="entity-type__help">
            {{ helpText }}
        </div>

        <!-- Bouton Next - Affiché seulement quand une option est sélectionnée -->
        <div v-if="selectedValue" class="btn__frame">
            <nextButton @click="handleNext" />
        </div>
    </div>
</template>

<script>
import mainButton from '../button/mainButton.vue';
import nextButton from '../button/nextButton.vue';

export default {
    name: 'EntityTypeSelector',
    components: { mainButton, nextButton },
    props: {
        // Valeur sélectionnée
        modelValue: {
            type: String,
            default: null,
            validator: (value) => [null, 'physical', 'legal'].includes(value)
        },
        // Label du champ
        label: {
            type: String,
            default: 'Type de personne'
        },
        // Champ obligatoire
        required: {
            type: Boolean,
            default: false
        },
        // Désactiver le composant
        disabled: {
            type: Boolean,
            default: false
        },
        // Message d'erreur
        error: {
            type: String,
            default: null
        },
        // Texte d'aide
        helpText: {
            type: String,
            default: null
        },
        // Options personnalisées
        options: {
            type: Object,
            default: () => ({
                physical: {
                    title: 'Personne Physique',
                    description: 'Client individuel',
                    icon: null
                },
                legal: {
                    title: 'Personne Morale',
                    description: 'Entreprise, Société, Association',
                    icon: null
                }
            })
        }
    },
    emits: ['update:modelValue', 'change', 'next'],
    computed: {
        selectedValue: {
            get() {
                return this.modelValue
            },
            set(value) {
                this.$emit('update:modelValue', value)
                this.$emit('change', value)
            }
        }
    },
    methods: {
        selectOption(value) {
            if (this.disabled) return
            
            if (this.selectedValue === value) {
                // Permettre de désélectionner si non requis
                if (!this.required) {
                    this.selectedValue = null
                }
            } else {
                this.selectedValue = value
            }
        },
        
        handleNext() {
            // Émettre l'événement next avec la valeur sélectionnée
            this.$emit('next', this.selectedValue)
        }
    }
}
</script>

<style scoped>
.entity-type-selector {
    width: 100%;
    max-width: 700px;
}

.entity-type__label {
    display: block;
    margin-bottom: 0.75rem;
    font-weight: 600;
    font-size: 0.875rem;
    color: #374151;
}

.required-asterisk {
    color: #ef4444;
    margin-left: 0.25rem;
}

.entity-type__options {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    width: 100%;
    max-width: 700px;
}

.entity-option {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.25rem;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    background: #ffffff;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.entity-option:hover:not(.entity-option--disabled) {
    border-color: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.entity-option--selected {
    border-color: #3b82f6;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(37, 99, 235, 0.02) 100%);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.entity-option--disabled {
    opacity: 0.5;
    cursor: not-allowed;
    background: #f9fafb;
}

.entity-option__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    background: #f8fafc;
    border-radius: 8px;
    color: #6b7280;
    flex-shrink: 0;
    transition: all 0.3s ease;
}

.entity-option__icon svg {
    width: 24px;
    height: 24px;
}

.entity-option--selected .entity-option__icon {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: #ffffff;
}

.entity-option__content {
    flex: 1;
    min-width: 0;
}

.entity-option__title {
    font-size: 1rem;
    font-weight: 600;
    color: #1f2937;
    margin: 0 0 0.25rem 0;
    transition: color 0.3s ease;
}

.entity-option--selected .entity-option__title {
    color: #1e40af;
}

.entity-option__description {
    font-size: 0.875rem;
    color: #6b7280;
    margin: 0;
    line-height: 1.4;
}

.entity-option__indicator {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    flex-shrink: 0;
}

.indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #d1d5db;
    border-radius: 50%;
    transition: all 0.3s ease;
}

.indicator--active {
    border-color: #3b82f6;
    background: #3b82f6;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}

.entity-type__error {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.5rem;
    font-size: 0.875rem;
    color: #ef4444;
}

.entity-type__error svg {
    width: 16px;
    height: 16px;
    flex-shrink: 0;
}

.entity-type__help {
    margin-top: 0.5rem;
    font-size: 0.75rem;
    color: #6b7280;
    line-height: 1.4;
}

.btn__frame{
    width: 100%;
    display: flex;
    justify-content: end;
}

/* Responsive */
@media (max-width: 640px) {
    .entity-type__options {
        grid-template-columns: 1fr;
    }
    
    .entity-option {
        padding: 1rem;
    }
    
    .entity-option__icon {
        width: 40px;
        height: 40px;
    }
    
    .entity-option__icon svg {
        width: 20px;
        height: 20px;
    }
}

/* Animation */
.entity-option {
    animation: fadeInUp 0.5s ease;
}

/* Animation d'apparition du bouton */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>