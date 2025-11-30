<template>
    <div class="layout">
        <header class="layout__header">
            <brand class="layout__brand"/>
        </header>

        <main class="layout__main">

            <div class="stepper-section">
                <stepperComponent 
                    :steps="stepsList" 
                    :current-step="currentStep" 
                />
            </div>

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

            <div v-else-if="currentStep === 2" class="step-container">

                <div class="form__title">
                    <h4>Nouveau client</h4>
                    <p>{{ entityType === 'PERSONNE_PHYSIQUE' ? 'Personne physique' : 'Personne morale' }}</p>
                </div>
                
                <customerForm 
                    v-if="entityType === 'PERSONNE_PHYSIQUE'"
                    :entity-type="entityType"
                    @prevstep="goToPreviousStep"
                    @submit="handleFormSubmit"
                    @notification="handleNotification"
                />
                
                <firmForm 
                    v-else-if="entityType === 'PERSONNE_MORALE'"
                    @prevstep="goToPreviousStep"
                    @submit="handleFormSubmit"
                    @notification="handleNotification"
                />
            </div>

            <notificationPopup 
                :message="notificationMessage"
                :type="notificationType"
                :visible="showNotification"
                :duration="notificationDuration"
                @close="showNotification = false"
            />
        </main>
    </div>
</template>

<script>
import customerForm from '../forms/customerForm.vue';
import customerCompanyForm from '../forms/customerCompanyForm.vue';
import firmForm from '../forms/firmForm.vue';
import brand from '../navigation/brand.vue';
import choicesFamily from '../input/choicesFamily.vue';
import notificationPopup from '../tools/notificationPopup.vue';
import stepperComponent from '../tools/stepperComponent.vue'; // Assurez-vous que ce fichier existe
import { ref } from 'vue';

export default {
    name: 'CustomerLayout',
    components: {
        customerForm,
        customerCompanyForm,
        brand,
        choicesFamily,
        notificationPopup,
        firmForm,
        stepperComponent
    },
    setup() {
        const entityType = ref(null);
        const currentStep = ref(1);

        // 2. DÉFINITION DES ÉTAPES POUR LE STEPPER
        const stepsList = ref([
            { label: 'Type de profil' },
            { label: 'Informations' },
            {label: 'Constitution de dossier'}
        ]);
        
        // Le totalSteps devient dynamique basé sur la liste
        const totalSteps = ref(stepsList.value.length);
        
        // Gestion des notifications
        const showNotification = ref(false);
        const notificationMessage = ref('');
        const notificationType = ref('success');
        const notificationDuration = ref(5000);

        const goToNextStep = (selectedType) => {
            console.log('Type sélectionné:', selectedType);
            entityType.value = selectedType;
            currentStep.value = 2;
        };

        const goToPreviousStep = () => {
            currentStep.value = 1;
        };

        const handleFormSubmit = (formData) => {
            console.log('Données du formulaire soumises avec succès:', formData);
            // Logique de soumission...
        };

        const handleNotification = (notification) => {
            showNotification.value = true;
            notificationMessage.value = notification.message;
            notificationType.value = notification.type;
            notificationDuration.value = notification.duration || 5000;

            setTimeout(() => {
                showNotification.value = false;
            }, notificationDuration.value);
        };

        const resetForm = () => {
            entityType.value = null;
            currentStep.value = 1;
        };

        return {
            entityType,
            currentStep,
            totalSteps,
            stepsList, // <--- IMPORTANT : Retourner la liste pour le template
            showNotification,
            notificationMessage,
            notificationType,
            notificationDuration,
            goToNextStep,
            goToPreviousStep,
            handleFormSubmit,
            handleNotification,
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
    /* 3. MODIFICATION : Column pour empiler Stepper + Formulaire */
    flex-direction: column; 
    align-items: center;
    /* justify-content: center;  <-- On peut enlever ça si on veut que ça commence en haut */
    padding: 2rem;
    overflow-y: auto;
    background: #f8fafc;
}

.stepper-section {
    width: 100%;
    margin-bottom: 1rem;
    display: flex;
    justify-content: center;
}

.step-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    /* padding-top supprimé car géré par le flex gap ou margin du stepper */
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
    margin-bottom: 1.5rem; /* Ajout d'espace sous le titre */
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
    background: #f3f4f6;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
}

/* Responsive */
@media (max-width: 768px) {
    .layout__header {
        padding: 0.75rem 1rem;
    }
    
    .layout__main {
        padding: 1rem;
    }
     
    .form__title {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
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

.layout-enter-active {
    transition: all 0.3s ease;
}

.layout-enter-from {
    opacity: 0;
    transform: translateY(10px);
}
</style>