<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
        <div class="modal-card" role="dialog" aria-modal="true">

          <div class="modal-header">
            <div class="title-container">
              <span class="header-icon-box" :class="item.isFolder ? 'is-folder' : 'is-file'">
                <svg v-if="item.isFolder" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon">
                  <path d="M19.5 21a3 3 0 0 0 3-3v-9a3 3 0 0 0-3-3h-7a1 1 0 0 1-.7-.29L9.4 3.3A2 2 0 0 0 8 2.75H4.5a3 3 0 0 0-3 3v12.25a3 3 0 0 0 3 3h15z"/>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zM13 3.5L18.5 9H13V3.5z"/>
                </svg>
              </span>
              <div>
                <h3 class="modal-title">{{ item.name || 'Détails du dossier' }}</h3>
                <span class="type-badge" :class="item.isFolder ? 'badge-folder' : 'badge-file'">
                  {{ item.isFolder ? 'Dossier' : 'Fichier' }}
                </span>
              </div>
            </div>
            <button class="close-btn" @click="closeModal" aria-label="Fermer la modale">
              &times;
            </button>
          </div>

          <div class="modal-body">
            <div class="preview-banner">
              <div class="banner-icon">
                <svg v-if="item.isFolder" xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2z"/>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
                </svg>
              </div>
              <div class="banner-text">
                <p class="banner-filename">{{ item.name }}</p>
                <p class="banner-path">{{ item.path || '/Projets/Docsira' }}</p>
              </div>
            </div>

            <div class="details-grid">
              <div class="detail-row">
                <span class="label">Taille</span>
                <span class="value font-medium">{{ item.size || '14.5 Mo' }}</span>
              </div>
              <div class="detail-row" v-if="item.isFolder">
                <span class="label">Contenu</span>
                <span class="value font-medium">{{ item.fileCount ?? 2 }} fichier(s)</span>
              </div>
              <div class="detail-row">
                <span class="label">Propriétaire</span>
                <div class="owner-pill">
                  <span class="avatar-circle">{{ getInitials(item.owner || 'Docsira') }}</span>
                  <span class="value">{{ item.owner || 'Docsira Admin' }}</span>
                </div>
              </div>
              <div class="detail-row">
                <span class="label">Créé le</span>
                <span class="value">{{ item.createdAt || '19 Août 2026' }}</span>
              </div>
              <div class="detail-row">
                <span class="label">Modifié le</span>
                <span class="value">{{ item.updatedAt || 'Aujourd\'hui à 14:30' }}</span>
              </div>
              <div class="detail-row">
                <span class="label">Accès</span>
                <span class="status-pill" :class="item.isShared ? 'shared' : 'private'">
                  {{ item.isShared ? 'Partagé' : 'Privé' }}
                </span>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal">Fermer</button>
            <button class="btn btn-primary" @click="handlePrimaryAction">
              {{ item.isFolder ? 'Ouvrir le dossier' : 'Télécharger' }}
            </button>
          </div>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
// ⚡️ CORRECTION ICI : Ajout de watch et onUnmounted pour gérer le scroll
import { watch, onUnmounted } from 'vue';

export interface ItemDetails {
  name?: string;
  isFolder?: boolean;
  size?: string;
  fileCount?: number;
  owner?: string;
  createdAt?: string;
  updatedAt?: string;
  path?: string;
  isShared?: boolean;
}

const props = withDefaults(
  defineProps<{
    isOpen: boolean;
    item?: ItemDetails;
  }>(),
  {
    isOpen: false,
    item: () => ({
      name: 'Détails du dossier',
      isFolder: true,
      size: '14.5 Mo',
      fileCount: 2,
      owner: 'Docsira Admin',
      createdAt: '19 Août 2026',
      updatedAt: 'Aujourd\'hui à 14:30',
      path: '/Projets/Docsira',
      isShared: true
    })
  }
);

const emit = defineEmits(['close', 'action']);

const closeModal = () => {
  emit('close');
};

const handlePrimaryAction = () => {
  emit('action', props.item);
};

const getInitials = (name: string): string => {
  if (!name) return 'D';
  return name.split(' ').map(part => part[0]).join('').substring(0, 2).toUpperCase();
};

// ⚡️ CORRECTION ICI : Bloquer/Débloquer le scroll du fond
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden'; // Empêche le scroll derrière
  } else {
    document.body.style.overflow = ''; // Restaure le scroll
  }
});

// Sécurité au cas où le composant est détruit pendant que la modale est ouverte
onUnmounted(() => {
  document.body.style.overflow = '';
});
</script>

<style scoped>
/* Vos styles scoped restent strictement identiques */
.modal-card {
  background: #ffffff;
  border-radius: 4px;
  padding: 1.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
  width: 85%;
  max-height: 85vh;
  overflow-y: auto;
  position: relative;
  z-index: 101;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
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
.header-icon-box.is-folder {
    background-color: #eff6ff;
    color: #2563eb;
}
.header-icon-box.is-file {
    background-color: #f0fdf4;
    color: #16a34a;
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
    line-height: 1.3;
}
.type-badge {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.15rem 0.5rem;
    border-radius: 6px;
    margin-top: 0.2rem;
}
.badge-folder {
    background-color: #dbeafe;
    color: #1e40af;
}
.badge-file {
    background-color: #dcfce7;
    color: #166534;
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
.preview-banner {
    background: #f9fafb;
    border: 1px solid #f3f4f6;
    border-radius: 12px;
    padding: 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.banner-icon { color: #3b82f6; }
.banner-text { overflow: hidden; }
.banner-filename {
    margin: 0;
    font-weight: 600;
    color: #111827;
    font-size: 0.95rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.banner-path { margin: 0; font-size: 0.8rem; color: #6b7280; }
.details-grid { display: flex; flex-direction: column; gap: 0.85rem; }
.detail-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.9rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #f3f4f6;
}
.detail-row:last-child { border-bottom: none; padding-bottom: 0; }
.label { color: #6b7280; }
.value { color: #1f2937; }
.font-medium { font-weight: 600; }
.owner-pill { display: flex; align-items: center; gap: 0.5rem; }
.avatar-circle { width: 24px; height: 24px; border-radius: 50%; background: #2563eb; color: white; font-size: 0.7rem; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.status-pill { padding: 0.2rem 0.6rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.status-pill.shared { background-color: #fef3c7; color: #92400e; }
.status-pill.private { background-color: #f3f4f6; color: #4b5563; }
.modal-footer { display: flex; gap: 0.75rem; margin-top: 0.5rem; }
.btn { flex: 1; padding: 0.65rem 1rem; border-radius: 10px; font-weight: 600; font-size: 0.9rem; cursor: pointer; border: none; transition: all 0.2s ease; }
.btn-secondary { background-color: #f3f4f6; color: #4b5563; }
.btn-secondary:hover { background-color: #e5e7eb; }
.btn-primary { background-color: #2563eb; color: white; }
.btn-primary:hover { background-color: #1d4ed8; }

@media (min-width: 1024px) {
  .modal-card { width: 32%; max-width: 480px; }
}
</style>

<style>
/* Vos styles globaux restent strictement identiques */
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

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.1s ease, transform 0.1s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
