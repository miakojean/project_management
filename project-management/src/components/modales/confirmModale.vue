<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="close">
    <div class="modal-container">
      
      <div class="modal-header">
        <h2 class="modal-title">{{ title }}</h2>
        <button @click="close" class="close-button" aria-label="Fermer">
          &times;
        </button>
      </div>

      <div class="modal-content">
        <p>{{ message }}</p>
      </div>

      <div class="modal-footer">
        <prevButton @click="close" :label="cancelText"/>
        <mainButton @click="confirm" :label="confirmText"/>
      </div>

    </div>
  </div>
</template>

<script setup>
import prevButton from '../button/prevButton.vue';
import mainButton from '../button/mainButton.vue';

// Props
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Confirmer l\'action'
  },
  message: {
    type: String,
    default: 'Êtes-vous sûr de vouloir continuer ?'
  },
  confirmText: {
    type: String,
    default: 'Confirmer'
  },
  cancelText: {
    type: String,
    default: 'Annuler'
  }
});

// Emits
const emit = defineEmits(['confirm', 'close']);

const close = () => {
  emit('close');
};

const confirm = () => {
  emit('confirm');
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
  animation: slideIn 0.3s ease-out;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
}

.close-button {
  background: none;
  border: none;
  font-size: 2rem;
  line-height: 1;
  color: #9ca3af;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s;
}

.close-button:hover {
  color: #374151;
}

.modal-content {
  padding: 1.5rem;
  color: #4b5563;
  line-height: 1.6;
}

.modal-content p {
  margin: 0;
}

.modal-footer {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  padding: 1.5rem;
  background-color: #f9fafb;
  border-top: 1px solid #e5e7eb;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
}

@keyframes slideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>