<template>
  <Teleport to="body">
    <Transition name="modal-fade" :duration="300">
      <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
        <div class="modal-card" role="dialog" aria-modal="true">

          <div class="modal-header">
            <div class="title-container">
              <span class="header-icon-box is-archive">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon">
                  <path d="M20.54 5.23l-1.39-1.68C18.88 3.21 18.47 3 18 3H6c-.47 0-.88.21-1.16.55L3.46 5.23C3.17 5.57 3 6.02 3 6.5V19c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6.5c0-.48-.17-.93-.46-1.27zM6.24 5h11.52l.81.97H5.44l.8-.97zM5 19V8h14v11H5zm6.5-5H8l4 4 4-4h-3.5v-4h-3v4z"/>
                </svg>
              </span>
              <h3 class="modal-title">Archiver le {{ isFolder ? 'dossier' : 'fichier' }}</h3>
            </div>
            <button class="close-btn" @click="closeModal" aria-label="Fermer la modale">
              &times;
            </button>
          </div>

          <div class="modal-body">
            <p class="archive-description">
              Êtes-vous sûr de vouloir archiver <strong>{{ itemName }}</strong> ?
            </p>
            <p class="archive-subtext">
              Cet élément ne sera plus visible dans cet espace de travail, mais vous pourrez toujours le retrouver et le restaurer depuis la section <strong>Archives</strong>.
            </p>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal">Annuler</button>
            <button class="btn btn-archive" @click="confirmArchive">
              Oui, archiver
            </button>
          </div>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { watch, onUnmounted } from 'vue';

const props = withDefaults(
  defineProps<{
    isOpen: boolean;
    itemName?: string;
    isFolder?: boolean;
  }>(),
  {
    isOpen: false,
    itemName: 'Élément sélectionné',
    isFolder: true
  }
);

const emit = defineEmits(['close', 'archive']);

const closeModal = () => {
  emit('close');
};

const confirmArchive = () => {
  emit('archive');
  closeModal();
};

// Gestion du blocage du scroll en arrière-plan
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});

onUnmounted(() => {
  document.body.style.overflow = '';
});
</script>

<style scoped>
/* --- Structure de base --- */
.modal-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
  width: 85%; /* 85% de la largeur sur mobile */
  position: relative;
  z-index: 101;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* --- En-tête --- */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.title-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-icon-box {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-icon-box.is-archive {
  background-color: #fef3c7;
  color: #d97706; /* Un ton ambre/orange pour signaler une mise à l'écart */
}

.header-icon-box .icon {
  width: 22px;
  height: 22px;
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

/* --- Corps de la modale --- */
.modal-body {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.archive-description {
  margin: 0;
  font-size: 1rem;
  color: #1f2937;
  line-height: 1.4;
}

.archive-subtext {
  margin: 0;
  font-size: 0.85rem;
  color: #6b7280;
  line-height: 1.4;
}

/* --- Pied de page --- */
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

.btn-secondary {
  background-color: #f3f4f6;
  color: #4b5563;
}

.btn-secondary:hover {
  background-color: #e5e7eb;
}

/* Bouton spécifique pour l'archivage */
.btn-archive {
  background-color: #d97706; /* Ambre foncé */
  color: white;
}

.btn-archive:hover {
  background-color: #b45309;
}

/* --- Responsive Ordinateur --- */
@media (min-width: 1024px) {
  .modal-card {
    width: 32%; /* Passe à 32% sur grand écran */
    max-width: 450px;
  }
}
</style>

<style>
/* ⚡️ Transitions ciblées uniquement sur la carte pour que l'overlay apparaisse sans transition */
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
