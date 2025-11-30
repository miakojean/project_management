<template>
    <div class="stepper-wrapper">
        <div 
            v-for="(step, index) in steps" 
            :key="index"
            class="stepper-item"
            :class="{ 
                'stepper-item--completed': index + 1 < currentStep,
                'stepper-item--active': index + 1 === currentStep 
            }"
        >
            <div v-if="index > 0" class="step-line"></div>

            <div class="step-content">
                <div class="step-circle">
                    <span v-if="index + 1 < currentStep">✓</span>
                    <span v-else>{{ index + 1 }}</span>
                </div>
                <div class="step-label">{{ step.label }}</div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'StepperComponent',
    props: {
        steps: {
            type: Array,
            required: true,
            // Format attendu: [{ label: 'Nom étape' }, ...]
        },
        currentStep: {
            type: Number,
            required: true
        }
    }
}
</script>

<style scoped>
.stepper-wrapper {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    width: 100%;
    max-width: 600px; /* Ajustable selon besoin */
    margin: 0 auto 2rem auto;
}

.stepper-item {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
}

/* Ligne de connexion */
.step-line {
    position: absolute;
    top: 20px; /* Centre verticalement par rapport au cercle (40px/2) */
    left: -50%;
    right: 50%;
    height: 2px;
    background-color: #e5e7eb;
    z-index: 0;
    transition: background-color 0.3s ease;
}

/* Ajustement pour que la ligne parte du milieu de l'item précédent */
.stepper-item:first-child .step-line {
    display: none;
}

.step-content {
    position: relative;
    z-index: 1; /* Pour être au-dessus de la ligne */
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
}

/* Cercle */
.step-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #ffffff;
    border: 2px solid #e5e7eb;
    color: #6b7280;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    transition: all 0.3s ease;
}

/* Label */
.step-label {
    font-size: 0.875rem;
    color: #9ca3af;
    font-weight: 500;
    text-align: center;
    transition: color 0.3s ease;
}

/* --- États --- */

/* État Actif */
.stepper-item--active .step-circle {
    border-color: var(--primary-color, #3b82f6);
    color: var(--primary-color, #3b82f6);
    background-color: #eff6ff;
    transform: scale(1.1);
}

.stepper-item--active .step-label {
    color: var(--primary-color, #3b82f6);
    font-weight: 700;
}

.stepper-item--active .step-line {
    /* La ligne menant à l'actif reste grise ou devient bleue selon préférence */
    background-color: var(--primary-color, #3b82f6);
}

/* État Complété */
.stepper-item--completed .step-circle {
    background-color: var(--primary-color, #3b82f6);
    border-color: var(--primary-color, #3b82f6);
    color: white;
}

.stepper-item--completed .step-label {
    color: var(--primary-color, #3b82f6);
}

/* La ligne d'un item complété est colorée */
.stepper-item--completed .step-line {
    background-color: var(--primary-color, #3b82f6);
}

/* Responsive */
@media (max-width: 600px) {
    .step-label {
        font-size: 0.75rem;
    }
    .step-circle {
        width: 32px;
        height: 32px;
        font-size: 0.875rem;
    }
    .step-line {
        top: 16px;
    }
}
</style>