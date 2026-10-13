<template>
  <Teleport to="body">
    <Transition name="modal-fade" :duration="300">
      <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
        <div class="modal-card" role="dialog" aria-modal="true">

          <div class="modal-header">
            <div class="title-container">
              <span class="header-icon-box is-danger">
                <!-- Icône Corbeille -->
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon">
                  <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM8 9h8v10H8V9zm7.5-5l-1-1h-5l-1 1H5v2h14V4h-3.5z"/>
                </svg>
              </span>
              <h3 class="modal-title">Supprimer le {{ isFolder ? 'dossier' : 'fichier' }}</h3>
            </div>
            <button class="close-btn" @click="closeModal" aria-label="Fermer la modale">
              &times;
            </button>
          </div>

          <div class="modal-body">
            <p class="delete-description">
              Êtes-vous sûr de vouloir supprimer définitivement <strong>{{ itemName }}</strong> ?
            </p>
            <p class="delete-subtext">
              Attention, cette action est <strong>irréversible</strong>. Cet élément sera supprimé pour vous et pour tous les collaborateurs qui y ont accès.
            </p>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal">Annuler</button>
            <button class="btn btn-danger" @click="confirmDelete">
              Oui, supprimer
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

const emit = defineEmits(['close', 'delete']);

const closeModal = () => {
  emit('close');
};

const confirmDelete = () => {
  emit('delete');
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
  width: 85%;
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

/* Thème Alerte / Danger */
.header-icon-box.is-danger {
  background-color: #fee2e2; /* Rouge très clair */
  color: #dc2626; /* Rouge vif */
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

.delete-description {
  margin: 0;
  font-size: 1rem;
  color: #1f2937;
  line-height: 1.4;
}

.delete-subtext {
  margin: 0;
  font-size: 0.85rem;
  color: #ef4444; /* Texte rouge pour insister sur l'aspect irréversible */
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

/* Bouton spécifique pour la suppression */
.btn-danger {
  background-color: #dc2626; /* Rouge vif */
  color: white;
}

.btn-danger:hover {
  background-color: #b91c1c; /* Rouge plus foncé au survol */
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
/* ⚡️ Transitions ciblées uniquement sur la carte pour que l'overlay apparaisse instantanément */
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
