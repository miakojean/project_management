<template>
  <div class="aesthetic-timeline-container">
    <div class="timeline-wrapper">
      <div class="progress-track"></div>
      <div class="progress-bar" :style="progressBarStyle"></div>

      <div
        v-for="item in steps"
        :key="item.id"
        :class="getStepClass(item.id)"
        class="timeline-step"
      >
        <button
          @click="goToStep(item.id)"
          :disabled="item.id > currentStep"
          class="step-button"
        >
          <div class="step-icon">
            <span v-if="!isCompleted(item.id)" class="step-number">{{ item.id }}</span>
            <svg
              v-else
              class="checkmark-icon"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
            >
              <path d="M20 6L9 17l-5-5" />
            </svg>
          </div>
          <div class="step-label">
            <h4 class="step-title">{{ item.title }}</h4>
            <p class="step-subtitle">{{ item.subtitle }}</p>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, computed } from "vue";

export default defineComponent({
  name: "AestheticTimeline",
  props: {
    currentStep: {
      type: Number,
      required: true,
    },
    steps: { 
      type: Array,
      default: () => [
        { id: 1, title: "Étape 1", subtitle: "Envoie d'email" },
        { id: 2, title: "Étape 2", subtitle: "Vérification" },
      ]
    }
  },
  emits: ['step-change'],
  setup(props, { emit }) {
    const isCompleted = (stepId) => stepId < props.currentStep;

    const getStepClass = (stepId) => {
      if (stepId < props.currentStep) return "completed";
      if (stepId === props.currentStep) return "active";
      return "";
    };

    const goToStep = (stepId) => {
      // Autorise le retour uniquement vers les étapes déjà complétées
      if (stepId < props.currentStep) {
        emit('step-change', stepId);
      }
    };

    const progressBarStyle = computed(() => {
      const stepCount = props.steps.length;
      const progressPercentage = ((props.currentStep - 1) / (stepCount - 1)) * 100;
      return {
        height: `${progressPercentage}%`
      }
    });

    return {
      isCompleted,
      getStepClass,
      goToStep,
      progressBarStyle
    };
  },
});
</script>

<style scoped>
/* Votre CSS existant reste identique */
:root {
  --timeline-primary-color: #4a90e2;
  --timeline-success-color: #50e3c2;
  --timeline-inactive-color: #dcdfe6;
  --timeline-bg-color: #ffffff;
  --timeline-text-primary: #303133;
  --timeline-text-secondary: #909399;
  --timeline-text-light: #ffffff;
}

.aesthetic-timeline-container {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  padding: 2rem;
  width: 320px;
  background: white;
  border-right: 1px solid #eaeaea;
}

.timeline-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 50px;
}

.progress-track, .progress-bar {
  position: absolute;
  left: 15px;
  top: 16px;
  bottom: 16px;
  width: 2px;
  z-index: 1;
}

.progress-track {
  background-color: var(--timeline-inactive-color);
}

.progress-bar {
  background-color: var(--timeline-success-color);
  height: 0%;
  transition: height 0.5s cubic-bezier(0.65, 0, 0.35, 1);
}

.timeline-step {
  position: relative;
  z-index: 2;
}

.step-button {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  padding: 0;
  text-align: left;
  width: 100%;
  cursor: pointer;
}

.step-button:disabled {
  cursor: not-allowed;
}

.step-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: var(--timeline-bg-color);
  border: 2px solid var(--timeline-inactive-color);
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 1rem;
  flex-shrink: 0;
  transition: all 0.4s ease;
  font-weight: 500;
  color: var(--timeline-text-secondary);
}

.step-label {
  transition: transform 0.3s ease;
}

.step-title, .step-subtitle {
  margin: 0;
  transition: color 0.4s ease;
}

.step-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--timeline-text-secondary);
}

.step-subtitle {
  font-size: 0.85rem;
  color: var(--timeline-text-secondary);
}

.step-button:not(:disabled):not(.active *):hover .step-icon {
  border-color: var(--timeline-primary-color);
}
.step-button:not(:disabled):not(.active *):hover .step-title {
  color: var(--timeline-primary-color);
}

.timeline-step.active .step-icon {
  background-color: var(--timeline-primary-color);
  border-color: var(--timeline-primary-color);
  color: var(--timeline-text-light);
  transform: scale(1.1);
  box-shadow: 0 0 15px rgba(74, 144, 226, 0.5);
}

.timeline-step.active .step-title {
  color: var(--timeline-text-primary);
  font-weight: 700;
}
.timeline-step.active .step-subtitle {
  color: var(--timeline-text-primary);
}

.timeline-step.completed .step-icon {
  background-color: transparent;
  border-color: var(--timeline-success-color);
}

.timeline-step.completed .step-title {
  color: var(--timeline-text-primary);
}

.timeline-step.completed .step-subtitle {
  color: var(--timeline-text-secondary);
}

.timeline-step.completed .step-button:hover .step-icon {
    transform: scale(1.1);
    background-color: rgba(80, 227, 194, 0.1);
}

.checkmark-icon {
  width: 16px;
  height: 16px;
  stroke-width: 3;
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke: var(--timeline-step-completed-icon-color, var(--timeline-text-light));
}

.timeline-step.completed .checkmark-icon {
    stroke: var(--timeline-success-color);
}
</style>