<template>
    <div class="layout">
        <!-- Header avec le brand -->
        <header class="layout__header">
            <brand class="layout__brand"/>
        </header>

        <!-- Contenu principal -->
        <main class="layout__main">
            <!-- Étape 1: Sélection du type de personne -->
            <div v-if="currentStep === 1" class="step-container">
                
                <choicesFamily
                    v-model="entityType"
                    label="Type de client"
                    :required="true"
                    :disabled="false"
                    error="Veuillez sélectionner un type"
                    help-text="Choisissez le type de personne selon votre situation"
                    @next="goToNextStep"
                />
            </div>

            <!-- Étape 2: Formulaire selon le type sélectionné -->
            <div v-else-if="currentStep === 2" class="step-container">
                <div class="form__title">
                    <h4>Nouveau client</h4>
                    <p>Personne physique</p>
                </div>
                <customerForm 
                    :entity-type="entityType"
                    @prevstep="goToPreviousStep"
                    @submit="handleFormSubmit"
                />
            </div>

            <!-- Indicateur de progression -->
            <div class="progress-indicator">
                <div class="progress-steps">
                    <div 
                        v-for="step in totalSteps" 
                        :key="step"
                        class="step-dot"
                        :class="{
                            'step-dot--active': step === currentStep,
                            'step-dot--completed': step < currentStep
                        }"
                    ></div>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
import customerForm from '../forms/customerForm.vue';
import brand from '../navigation/brand.vue';
import choicesFamily from '../input/choicesFamily.vue';
import { ref } from 'vue';

export default {
    name: 'CustomerLayout',
    components: {
        customerForm,
        brand,
        choicesFamily
    },
    setup() {
        const entityType = ref(null);
        const currentStep = ref(1);
        const totalSteps = ref(2);

        const goToNextStep = (selectedType) => {
            console.log('Type sélectionné:', selectedType);
            entityType.value = selectedType;
            currentStep.value = 2;
        };

        const goToPreviousStep = () => {
            currentStep.value = 1;
        };

        const handleFormSubmit = (formData) => {
            console.log('Données du formulaire:', formData);
            console.log('Type d\'entité:', entityType.value);
            
            // Ici vous pouvez envoyer les données à votre API
            // et rediriger vers une page de confirmation
            alert('Client créé avec succès !');
            
            // Réinitialiser pour un nouveau client
            // resetForm();
        };

        const resetForm = () => {
            entityType.value = null;
            currentStep.value = 1;
        };

        return {
            entityType,
            currentStep,
            totalSteps,
            goToNextStep,
            goToPreviousStep,
            handleFormSubmit,
            resetForm
        };
    }
};
</script>

<style scoped>
.layout {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: #ffffff;
    overflow: hidden;
}

.layout__header {
    width: 100%;
    padding: 1rem 1.5rem;
    background: #ffffff;
    border-bottom: 1px solid #f3f4f6;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    z-index: 10;
    flex-shrink: 0;
}

.layout__brand {
    display: flex;
    align-items: center;
}

.layout__main {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    overflow-y: auto;
    background: #f8fafc;
    height: 100vh;
}

.step-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    max-width: 900px;
    animation: fadeIn 0.3s ease;
}

.form__title {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: start;
    gap: 1rem;
}

.form__title h4{
    font-size: 1.5rem;
    font-weight: 500;
    color: var(--primary-color);
}

.form__title p{
    font-size: 1rem;
    font-weight: 500;
    color: var(--adn-gray-color);
}

/* Responsive */
@media (max-width: 768px) {
    .layout__header {
        padding: 0.75rem 1rem;
    }
    
    .layout__main {
        padding: 1rem;
    }
}

@media (max-width: 480px) {
    .layout__header {
        padding: 0.5rem 0.75rem;
    }
    
    .layout__main {
        padding: 0.75rem;
    }
}

/* Animation d'entrée */
.layout-enter-active {
    transition: all 0.3s ease;
}

.layout-enter-from {
    opacity: 0;
    transform: translateY(10px);
}
</style>