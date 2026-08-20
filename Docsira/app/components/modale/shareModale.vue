<template>
  <Teleport to="body">
    <Transition name="modal-fade" :duration="300">
      <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
        <div class="modal-card" role="dialog" aria-modal="true">

          <div class="modal-header">
            <h3 class="modal-title">Partager avec des collaborateurs</h3>
            <button class="close-btn" @click="closeModal" aria-label="Fermer la modale">
              &times;
            </button>
          </div>

          <div class="modal-body">
            <div class="invite-section">
              <div class="input-group">
                <input
                  type="text"
                  v-model="inviteEmail"
                  class="text-input"
                  placeholder="Ajouter des personnes (email ou nom)..."
                  @keyup.enter="handleInvite"
                />
                <select v-model="inviteRole" class="role-select">
                  <option value="viewer">Lecteur</option>
                  <option value="editor">Éditeur</option>
                </select>
              </div>
              <button
                class="btn btn-primary btn-invite"
                :disabled="!inviteEmail.trim()"
                @click="handleInvite"
              >
                Inviter
              </button>
            </div>

            <hr class="divider" />

            <div class="collaborators-section">
              <h4 class="section-title">Personnes ayant accès</h4>

              <div class="collaborator-list">
                <div class="collaborator-row">
                  <div class="collab-info">
                    <span class="avatar-circle owner-avatar">{{ getInitials(owner.name) }}</span>
                    <div class="collab-details">
                      <span class="collab-name">{{ owner.name }} (Vous)</span>
                      <span class="collab-email">{{ owner.email }}</span>
                    </div>
                  </div>
                  <span class="role-text owner-role">Propriétaire</span>
                </div>

                <div
                  v-for="collab in collaborators"
                  :key="collab.id"
                  class="collaborator-row"
                >
                  <div class="collab-info">
                    <span class="avatar-circle">{{ getInitials(collab.name) }}</span>
                    <div class="collab-details">
                      <span class="collab-name">{{ collab.name }}</span>
                      <span class="collab-email">{{ collab.email }}</span>
                    </div>
                  </div>

                  <div class="collab-actions">
                    <select
                      v-model="collab.role"
                      class="role-select compact"
                      @change="updateRole(collab)"
                    >
                      <option value="viewer">Lecteur</option>
                      <option value="editor">Éditeur</option>
                      <option value="remove" class="text-danger">Retirer l'accès</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal">Terminé</button>
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
  }>(),
  { isOpen: false }
);

const emit = defineEmits(['close', 'invite', 'update-role', 'remove']);

// --- États du formulaire d'invitation ---
const inviteEmail = ref('');
const inviteRole = ref('viewer');

// --- Données factices (à remplacer par vos props/API) ---
const owner = ref({ name: 'Docsira Admin', email: 'admin@docsira.com' });
const collaborators = ref([
  { id: 1, name: 'Kaba Niale', email: 'kaba.niale@example.com', role: 'editor' },
  { id: 2, name: 'Jean Dupont', email: 'j.dupont@example.com', role: 'viewer' }
]);

// --- Méthodes ---
const closeModal = () => {
  emit('close');
  inviteEmail.value = ''; // Reset à la fermeture
};

const handleInvite = () => {
  if (!inviteEmail.value.trim()) return;
  emit('invite', { email: inviteEmail.value, role: inviteRole.value });
  // Simuler l'ajout UI pour l'exemple
  collaborators.value.unshift({
    id: Date.now(),
    name: inviteEmail.value.split('@')[0], // Pseudo nom
    email: inviteEmail.value,
    role: inviteRole.value
  });
  inviteEmail.value = ''; // Reset input
};

const updateRole = (collab: any) => {
  if (collab.role === 'remove') {
    collaborators.value = collaborators.value.filter(c => c.id !== collab.id);
    emit('remove', collab.id);
  } else {
    emit('update-role', { id: collab.id, role: collab.role });
  }
};

const getInitials = (name: string): string => {
  if (!name) return 'D';
  return name.split(' ').map(part => part[0]).join('').substring(0, 2).toUpperCase();
};

// --- Gestion du scroll (identique aux autres modales) ---
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
/* --- Structure Modale (Identique) --- */
.modal-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
  width: 90%;
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
  align-items: center;
}

.modal-title { margin: 0; font-size: 1.15rem; font-weight: 700; color: #1f2937; }
.close-btn { background: transparent; border: none; font-size: 1.75rem; cursor: pointer; color: #9ca3af; padding: 0; transition: color 0.2s ease; }
.close-btn:hover { color: #ef4444; }

/* --- Section Invitation --- */
.invite-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.input-group {
  display: flex;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  overflow: hidden;
  transition: border-color 0.2s ease;
}

.input-group:focus-within {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.text-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: none;
  font-size: 0.95rem;
  color: #1f2937;
  outline: none;
}

.role-select {
  background-color: #f9fafb;
  border: none;
  border-left: 1px solid #e5e7eb;
  padding: 0 1rem;
  color: #4b5563;
  font-size: 0.9rem;
  cursor: pointer;
  outline: none;
}

.btn-invite {
  align-self: flex-end;
  padding: 0.6rem 1.2rem;
}

.divider {
  border: none;
  border-top: 1px solid #f3f4f6;
  margin: 0.5rem 0;
}

/* --- Section Collaborateurs --- */
.section-title {
  margin: 0 0 1rem 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #4b5563;
}

.collaborator-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.collaborator-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.collab-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.avatar-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #3b82f6;
  color: white;
  font-size: 0.85rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.owner-avatar { background: #6b7280; }

.collab-details {
  display: flex;
  flex-direction: column;
}

.collab-name { font-size: 0.9rem; font-weight: 600; color: #111827; }
.collab-email { font-size: 0.8rem; color: #6b7280; }

.role-text { font-size: 0.85rem; color: #6b7280; font-weight: 500; padding-right: 0.5rem; }

.role-select.compact {
  background: transparent;
  border: none;
  border-left: none;
  padding: 0.2rem;
  font-size: 0.85rem;
  color: #4b5563;
  text-align: right;
}

.role-select.compact:hover { background: #f3f4f6; border-radius: 6px; }
.text-danger { color: #ef4444; font-weight: 600; }

/* --- Boutons globaux --- */
.modal-footer { display: flex; justify-content: flex-end; margin-top: 0.5rem; }
.btn { padding: 0.65rem 1.25rem; border-radius: 10px; font-weight: 600; font-size: 0.9rem; cursor: pointer; border: none; transition: all 0.2s ease; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-primary { background-color: #2563eb; color: white; }
.btn-primary:not(:disabled):hover { background-color: #1d4ed8; }
.btn-secondary { background-color: #f3f4f6; color: #4b5563; width: 100%; }
.btn-secondary:hover { background-color: #e5e7eb; }

/* --- Responsive Ordinateur --- */
@media (min-width: 1024px) {
  .modal-card { width: 35%; max-width: 500px; }
  .btn-invite { width: auto; }
}
</style>
