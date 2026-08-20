<template>
  <Teleport to="body">
    <Transition name="modal-fade" :duration="300">
      <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
        <div class="modal-card" role="dialog" aria-modal="true">

          <div class="modal-header">
            <h3 class="modal-title">Renommer le {{ isFolder ? 'dossier' : 'fichier' }}</h3>
            <button class="close-btn" @click="closeModal" aria-label="Fermer la modale">
              &times;
            </button>
          </div>

          <div class="modal-body">
            <label for="renameInput" class="input-label">Nouveau nom</label>
            <input
              id="renameInput"
              type="text"
              v-model="newName"
              class="text-input"
              placeholder="Entrez le nouveau nom..."
              @keyup.enter="submitRename"
              autofocus
            />
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal">Annuler</button>
            <button class="btn btn-primary" @click="submitRename" :disabled="!isNameValid">
              Enregistrer
            </button>
          </div>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, computed, onUnmounted } from 'vue';

const props = defineProps<{
  isOpen: boolean;
  currentName: string;
  isFolder?: boolean;
}>();

const emit = defineEmits(['close', 'rename']);

// État local pour le champ de texte
const newName = ref('');

// Désactiver le bouton d'enregistrement si le champ est vide ou inchangé
const isNameValid = computed(() => {
  return newName.value.trim().length > 0 && newName.value.trim() !== props.currentName;
});

// Synchroniser la valeur de l'input quand la modale s'ouvre
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    newName.value = props.currentName;
    document.body.style.overflow = 'hidden'; // Empêche le scroll derrière
  } else {
    document.body.style.overflow = ''; // Restaure le scroll
  }
});

const closeModal = () => {
  emit('close');
};

const submitRename = () => {
  if (isNameValid.value) {
    emit('rename', newName.value.trim());
    closeModal();
  }
};

// Sécurité : restauration du scroll à la destruction du composant
onUnmounted(() => {
  document.body.style.overflow = '';
});
</script>

<style scoped>
/* --- Structure de base (identique à la modale de détails) --- */
.modal-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
  width: 85%;
  position: relative;
  z-index: 101;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 700;
  color: #1f2937;
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 1.75rem;
  cursor: pointer;
  color: #9ca3af;
  line-height: 1;
  padding: 0;
  transition: color 0.2s ease;
}

.close-btn:hover { color: #ef4444; }

/* --- Styles spécifiques au formulaire --- */
.modal-body {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #4b5563;
}

.text-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 1rem;
  color: #1f2937;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  box-sizing: border-box;
}

.text-input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

/* --- Pied de page et Boutons --- */
.modal-footer {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.btn {
  flex: 1;
  padding: 0.65rem 1rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #f3f4f6;
  color: #4b5563;
}

.btn-secondary:not(:disabled):hover {
  background-color: #e5e7eb;
}

.btn-primary {
  background-color: #2563eb;
  color: white;
}

.btn-primary:not(:disabled):hover {
  background-color: #1d4ed8;
}

/* --- Responsive Ordinateur --- */
@media (min-width: 1024px) {
  .modal-card {
    width: 32%;
    max-width: 450px;
  }
}
</style>

<style>
/* --- Overlay & Transitions Globales (Sans animation sur l'overlay) --- */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(17, 24, 39, 0.35);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-fade-enter-active .modal-card,
.modal-fade-leave-active .modal-card {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.modal-fade-enter-from .modal-card,
.modal-fade-leave-to .modal-card {
  opacity: 0;
  transform: scale(0.95);
}
</style>
