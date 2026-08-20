<template>
  <Teleport to="body">
    <Transition name="modal-fade" :duration="300">
      <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
        <div class="modal-card" role="dialog" aria-modal="true">

          <div class="modal-header">
            <h3 class="modal-title">Partager le lien</h3>
            <button class="close-btn" @click="closeModal" aria-label="Fermer la modale">
              &times;
            </button>
          </div>

          <div class="modal-body">
            <p class="share-description">
              Toute personne disposant de ce lien pourra accéder à ce document.
            </p>

            <div class="link-input-group">
              <input
                type="text"
                :value="link"
                class="link-input"
                readonly
                ref="linkInputRef"
                @focus="$event.target.select()"
              />
              <button
                class="btn-copy"
                :class="{ 'is-copied': isCopied }"
                @click="copyToClipboard"
              >
                <svg v-if="!isCopied" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon">
                  <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon check-icon">
                  <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                </svg>
                {{ isCopied ? 'Copié !' : 'Copier' }}
              </button>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal">Fermer</button>
          </div>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, onUnmounted } from 'vue';

const props = withDefaults(
  defineProps<{
    isOpen: boolean;
    link?: string;
  }>(),
  {
    isOpen: false,
    link: 'https://docsira.com/app/share/doc-12345'
  }
);

const emit = defineEmits(['close']);

const isCopied = ref(false);
const linkInputRef = ref<HTMLInputElement | null>(null);

// Fonction pour copier le lien
const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(props.link);
    isCopied.value = true;

    // Sélectionner le texte visuellement
    if (linkInputRef.value) {
      linkInputRef.value.select();
    }

    // Remettre le bouton à l'état normal après 2 secondes
    setTimeout(() => {
      isCopied.value = false;
    }, 2000);
  } catch (err) {
    console.error('Échec de la copie :', err);
  }
};

const closeModal = () => {
  emit('close');
  // Réinitialiser l'état de copie si on ferme très vite
  setTimeout(() => {
    isCopied.value = false;
  }, 300);
};

// Gestion du scroll
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

/* --- Contenu : Partage --- */
.modal-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.share-description {
  margin: 0;
  font-size: 0.9rem;
  color: #6b7280;
  line-height: 1.4;
}

.link-input-group {
  display: flex;
  align-items: center;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 0.25rem;
  transition: border-color 0.2s ease;
}

.link-input-group:focus-within {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.link-input {
  flex: 1;
  background: transparent;
  border: none;
  padding: 0.5rem 0.75rem;
  font-size: 0.9rem;
  color: #374151;
  width: 100%;
  outline: none;
}

.btn-copy {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background-color: #ffffff;
  border: 1px solid #d1d5db;
  color: #374151;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn-copy:hover {
  background-color: #f3f4f6;
}

.btn-copy.is-copied {
  background-color: #16a34a;
  border-color: #16a34a;
  color: #ffffff;
}

.icon {
  width: 16px;
  height: 16px;
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

/* --- Responsive Ordinateur --- */
@media (min-width: 1024px) {
  .modal-card {
    width: 32%;
    max-width: 450px;
  }
}
</style>

<style>
/* Les styles globaux (.modal-overlay, transitions) sont supposés être déjà dans votre fichier principal ou dans les autres composants modales, je ne les répète pas ici pour éviter les conflits CSS. Si besoin, rajoutez-les. */
</style>
