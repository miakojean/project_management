<template>
  <div class="account-section">
    <header class="section-header">
      <h2>Information du client</h2>
    </header>

    <div class="card">
      <!-- Référence client (non éditable) -->
      <div class="client-reference" v-if="form.reference_client">
        <span class="ref-badge">Référence: {{ form.reference_client }}</span>
        <span class="status-badge" :class="form.statut.toLowerCase()">{{ getStatusLabel(form.statut) }}</span>
      </div>

      <div class="profile-header">
        <div class="avatar-wrapper">
          <div class="avatar">{{ clientInitials }}</div>
          <button class="camera-btn" @click="handleAvatarChange">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
              <circle cx="12" cy="13" r="4"></circle>
            </svg>
          </button>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="form-grid">
        <!-- Type de client -->
        <div class="form-group">
          <div class="label-row">
            <label>Type de client *</label>
          </div>
          <div class="input-wrapper">
            <select v-model="form.type_client" @change="handleClientTypeChange">
              <option value="PERSONNE_PHYSIQUE">Personne Physique</option>
              <option value="PERSONNE_MORALE">Personne Morale</option>
            </select>
            <span class="input-icon chevron">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </span>
          </div>
        </div>

        <!-- Statut du client -->
        <div class="form-group">
          <div class="label-row">
            <label>Statut *</label>
          </div>
          <div class="input-wrapper">
            <select v-model="form.statut">
              <option value="ACTIF">Actif</option>
              <option value="INACTIF">Inactif</option>
              <option value="PROSPECT">Prospect</option>
              <option value="ARCHIVE">Archivé</option>
            </select>
            <span class="input-icon chevron">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </span>
          </div>
        </div>

        <!-- Personne Physique -->
        <template v-if="form.type_client === 'PERSONNE_PHYSIQUE'">
          <inputfamily label="Nom *" identifiant="nom" v-model="form.nom" />
          <inputfamily label="Prénoms *" identifiant="prenoms" v-model="form.prenoms" />
          <inputfamily label="Date de naissance" identifiant="date_naissance" type="date" v-model="form.date_naissance" />
          <inputfamily label="Lieu de naissance" identifiant="lieu_naissance" v-model="form.lieu_naissance" />
        </template>

        <!-- Personne Morale -->
        <template v-else>
          <inputfamily label="Dénomination sociale" identifiant="raison_sociale" v-model="form.raison_sociale" />
          <inputfamily label="Forme juridique" identifiant="forme_juridique" v-model="form.forme_juridique" />
          <inputfamily label="Numéro RCCM" identifiant="numero_rccm" v-model="form.numero_rccm" />
          <inputfamily label="Numéro Compte Contribuable" identifiant="numero_cc" v-model="form.numero_cc" />

          <div class="form-group">
            <div class="label-row">
              <label>Capital social</label>
            </div>
            <div class="input-wrapper">
              <input type="number" v-model="form.capital_social" placeholder="0.00" step="0.01" />
              <span class="input-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2">
                  <line x1="12" y1="1" x2="12" y2="23"></line>
                  <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                </svg>
              </span>
            </div>
          </div>

          <inputfamily label="Représentant légal" identifiant="representant_legal_nom" v-model="form.representant_legal_nom" />
          <inputfamily label="Fonction du représentant" identifiant="representant_legal_fonction" v-model="form.representant_legal_fonction" />
        </template>

        <!-- Coordonnées communes -->
        <div class="form-group full-width">
          <div class="label-row">
            <label>Adresse</label>
          </div>
          <div class="input-wrapper">
            <textarea v-model="form.adresse" placeholder="Adresse complète" rows="2"></textarea>
          </div>
        </div>

        <inputfamily label="Ville" identifiant="ville" v-model="form.ville" />
        <inputfamily label="Commune" identifiant="commune" v-model="form.commune" />

        <!-- Téléphones -->
        <div class="form-group">
          <div class="label-row">
            <label>Téléphone 1 *</label>
            <span class="status-verified" v-if="isPhoneVerified(form.telephone_1)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="none">
                <circle cx="12" cy="12" r="10" fill="#27AE60"></circle>
                <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" fill="white"></path>
              </svg>
              Vérifié
            </span>
          </div>
          <div class="input-wrapper">
            <input type="tel" v-model="form.telephone_1" placeholder="+225 XX XX XX XX" />
            <span class="input-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
              </svg>
            </span>
          </div>
        </div>

        <div class="form-group">
          <div class="label-row">
            <label>Téléphone 2</label>
          </div>
          <div class="input-wrapper">
            <input type="tel" v-model="form.telephone_2" placeholder="+225 XX XX XX XX" />
            <span class="input-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
              </svg>
            </span>
          </div>
        </div>

        <!-- Email -->
        <div class="form-group full-width">
          <div class="label-row">
            <label>Email</label>
            <span class="status-verified" v-if="isEmailVerified(form.email)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="none">
                <circle cx="12" cy="12" r="10" fill="#27AE60"></circle>
                <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" fill="white"></path>
              </svg>
              Vérifié
            </span>
          </div>
          <div class="input-wrapper">
            <input type="email" v-model="form.email" placeholder="email@exemple.com" />
            <span class="input-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
            </span>
          </div>
        </div>

        <!-- Chargé de clientèle -->
        <div class="form-group">
          <div class="label-row">
            <label>Chargé de clientèle</label>
          </div>
          <div class="input-wrapper">
            <select v-model="form.charge_de_clientele" :disabled="!chargeDeClienteleOptions.length">
              <option value="">Non assigné</option>
              <option v-for="user in chargeDeClienteleOptions" :key="user.id" :value="user.id">
                {{ user.nom_complet || user.username }}
              </option>
            </select>
            <span class="input-icon chevron">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </span>
          </div>
        </div>

        <!-- Date premier contact -->
        <div class="form-group">
          <div class="label-row">
            <label>Date premier contact</label>
          </div>
          <div class="input-wrapper">
            <input type="date" v-model="form.date_premier_contact" />
            <span class="input-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
            </span>
          </div>
        </div>

        <!-- Notes (remplace Bio) -->
        <div class="form-group full-width">
          <div class="label-row">
            <label>Notes internes</label>
            <span class="action-link" @click="editNotes = !editNotes">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
              {{ editNotes ? 'Terminer' : 'Éditer' }}
            </span>
          </div>
          <div class="notes-container" :class="{ 'active': editNotes }">
            <textarea 
              v-model="form.notes" 
              :readonly="!editNotes"
              placeholder="Notes internes sur le client..."
              rows="4"
            ></textarea>
          </div>
        </div>

        <!-- Boutons d'action -->
        <div class="form-actions full-width">
          <secondButton @click="handleCancel" label="Annuler"></secondButton>
          <mainButton @click="handleSubmit" :disabled="isSaving" :isLoading="isSaving" label="Enregistrer">
            Enregistrer les modifications
          </mainButton>
        </div>
      </form>
    </div>

    <!-- Modal de confirmation -->
    <div v-if="showConfirmModal" class="modal-overlay">
      <div class="modal">
        <h3>Confirmer l'enregistrement</h3>
        <p>Êtes-vous sûr de vouloir enregistrer les modifications ?</p>
        <div class="modal-actions">
          <prevButton @click="showConfirmModal = false" label='Annuler'/>
          <mainButton @click="confirmSave" label='Confirmer'/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, watch, computed } from 'vue';
import { useRouter } from 'vue-router'; // Import du router pour la redirection si nécessaire
import inputfamily from '../input/inputfamily.vue';
import { useCustomerStore } from '@/stores/custumerStore';
import mainButton from '../button/mainButton.vue';
import prevButton from '../button/prevButton.vue';

export default {
  name: 'CustomerSectionInfo',
  components: {
    inputfamily,
    mainButton,
    prevButton
  },
  props: {
    clientId: {
      type: [Number, String],
      default: null
    }
  },
  setup(props) {
    const router = useRouter();
    const clientStore = useCustomerStore();
    
    const isSaving = ref(false);
    const editNotes = ref(false);
    const showConfirmModal = ref(false);
    const isLoading = ref(false);
    const chargeDeClienteleOptions = ref([]);

    // Modèle de données
    const form = reactive({
      id: null, // Ajout de l'ID pour le suivi
      type_client: 'PERSONNE_PHYSIQUE',
      statut: 'ACTIF',
      reference_client: '',
      
      // Personne Physique
      nom: '',
      prenoms: '',
      date_naissance: '',
      lieu_naissance: '',
      
      // Personne Morale
      raison_sociale: '',
      forme_juridique: '',
      numero_rccm: '',
      numero_cc: '',
      capital_social: '',
      representant_legal_nom: '',
      representant_legal_fonction: '',
      
      // Coordonnées
      adresse: '',
      ville: '',
      commune: '',
      telephone_1: '',
      telephone_2: '',
      email: '',
      
      // Gestion
      date_premier_contact: new Date().toISOString().split('T')[0],
      notes: '',
      charge_de_clientele: '',
    });

    /**
     * Fonction utilitaire pour remplir le formulaire avec un objet données
     */
    const populateForm = (data) => {
        Object.keys(form).forEach(key => {
          if (data[key] !== undefined && data[key] !== null) {
            // Traitement spécial pour les dates
            if (key.includes('date') && data[key]) {
              form[key] = data[key].split('T')[0];
            } 
            // Traitement spécial pour le capital social (conversion en string pour l'input)
            else if (key === 'capital_social' && data[key] !== null) {
              form[key] = data[key].toString();
            } 
            // Cas général
            else {
              form[key] = data[key];
            }
          }
        });
    };

    /**
     * Charge les données du client
     */
    const loadClientData = async () => {
      isLoading.value = true;
      
      try {
        // 1. Déterminer quel ID utiliser
        // On regarde d'abord les props, sinon on regarde le store (cas navigation depuis la liste)
        let targetId = props.clientId;
        
        if (!targetId && clientStore.currentCustomer) {
            targetId = clientStore.currentCustomer.id;
        }

        // Si aucun ID trouvé (ex: refresh page sans ID dans l'URL), on redirige ou on reset
        if (!targetId) {
            console.warn("Aucun client sélectionné, retour à la liste ou mode création.");
            // Optionnel : router.push('/dashboard/customer-list');
            return; 
        }

        console.log(`Chargement du client ID: ${targetId} depuis l'API...`);
        
        // 2. Appel API pour avoir les infos fraîches
        const clientData = await clientStore.fetchCustomerById(targetId);
        
        // 3. Remplir le formulaire
        populateForm(clientData);
        
        console.log('Formulaire synchronisé avec succès');
        
      } catch (error) {
        console.error('Erreur lors du chargement du client:', error);
      } finally {
        isLoading.value = false;
      }
    };

    const loadChargeDeClienteleOptions = async () => {
      // Simulation ou appel API réel ici
      chargeDeClienteleOptions.value = [
          { id: 1, nom_complet: 'Jean Dupont' },
          { id: 2, nom_complet: 'Marie Curie' }
      ];
    };

    const handleClientTypeChange = () => {
      if (form.type_client === 'PERSONNE_PHYSIQUE') {
        form.raison_sociale = '';
        form.forme_juridique = '';
        form.numero_rccm = '';
        form.numero_cc = '';
        form.capital_social = '';
        form.representant_legal_nom = '';
        form.representant_legal_fonction = '';
      } else {
        form.nom = '';
        form.prenoms = '';
        form.date_naissance = '';
        form.lieu_naissance = '';
      }
    };

    const handleAvatarChange = () => {
      // TODO: Implémenter upload avatar
    };

    const validateForm = () => {
      const errors = [];
      if (!form.type_client) errors.push('Le type de client est requis');
      if (!form.statut) errors.push('Le statut est requis');
      
      if (form.type_client === 'PERSONNE_PHYSIQUE') {
        if (!form.nom.trim()) errors.push('Le nom est requis');
        if (!form.prenoms.trim()) errors.push('Les prénoms sont requis');
      } else {
        if (!form.raison_sociale.trim()) errors.push('La raison sociale est requise');
      }
      
      if (!form.telephone_1.trim()) errors.push('Le téléphone 1 est requis');
      
      return errors;
    };

    const handleSubmit = () => {
      const errors = validateForm();
      if (errors.length > 0) {
        alert('Erreurs :\n' + errors.join('\n'));
        return;
      }
      showConfirmModal.value = true;
    };

    const confirmSave = async () => {
      isSaving.value = true;
      showConfirmModal.value = false;
      
      try {
        const dataToSave = { ...form };
        
        // Nettoyage des données
        Object.keys(dataToSave).forEach(key => {
          if (dataToSave[key] === '' || dataToSave[key] === null) {
            dataToSave[key] = null;
          }
          if (key === 'capital_social' && dataToSave[key]) {
            dataToSave[key] = parseFloat(dataToSave[key]);
          }
        });
        
        // On utilise l'ID du formulaire (récupéré au chargement) ou l'ID des props
        const idToUpdate = form.id || props.clientId || (clientStore.currentCustomer ? clientStore.currentCustomer.id : null);

        if (idToUpdate) {
          // UPDATE
          await clientStore.updateCustomer(idToUpdate, dataToSave);
          alert('Client mis à jour avec succès!');
          await loadClientData(); // Recharger pour être sûr
        } else {
          // CREATE
          const newClient = await clientStore.createCustomer(dataToSave);
          alert('Client créé avec succès!');
          // Mise à jour de l'ID local pour passer en mode édition
          form.id = newClient.id;
          clientStore.attachCustomer(newClient);
        }
        
      } catch (error) {
        console.error('Erreur save:', error);
        alert('Erreur: ' + (clientStore.error || error.message));
      } finally {
        isSaving.value = false;
      }
    };

    const handleCancel = () => {
        // Si on a un ID, on recharge les données originales
        if (form.id || props.clientId || clientStore.currentCustomer) {
            loadClientData();
        } else {
            // Sinon on vide tout (mode création)
            Object.keys(form).forEach(key => {
                if (key !== 'type_client' && key !== 'statut') form[key] = '';
            });
            form.type_client = 'PERSONNE_PHYSIQUE';
            form.statut = 'ACTIF';
        }
    };

    const getStatusLabel = (status) => {
      const labels = { 'ACTIF': 'Actif', 'INACTIF': 'Inactif', 'PROSPECT': 'Prospect', 'ARCHIVE': 'Archivé' };
      return labels[status] || status;
    };

    const isEmailVerified = (email) => email && email.includes('@') && email.includes('.');
    const isPhoneVerified = (phone) => phone && phone.length >= 8;

    // Computed pour les initiales
    const clientInitials = computed(() => {
      if (form.type_client === 'PERSONNE_PHYSIQUE') {
        const nom = form.nom?.trim() || '';
        const prenoms = form.prenoms?.trim() || '';
        return (nom[0] || '') + (prenoms[0] || '');
      } else {
        const raison = form.raison_sociale?.trim() || '';
        const words = raison.split(' ');
        return words.slice(0, 2).map(w => w[0] || '').join('');
      }
    });

    // --- CYCLE DE VIE ---
    onMounted(async () => {
      await Promise.all([
          loadClientData(),
          loadChargeDeClienteleOptions()
      ]);
    });

    // Si l'ID change via les props (cas rare si pas dans l'URL, mais bonne pratique)
    watch(() => props.clientId, (newVal) => {
        if(newVal) loadClientData();
    });

    return {
      form,
      isSaving,
      isLoading,
      editNotes,
      showConfirmModal,
      chargeDeClienteleOptions,
      clientInitials,
      handleClientTypeChange,
      handleAvatarChange,
      handleSubmit,
      confirmSave,
      handleCancel,
      getStatusLabel,
      isEmailVerified,
      isPhoneVerified
    };
  }
};
</script>

<style scoped>
.account-section {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #F3F4F6;
  min-height: 100vh;
}

.section-header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 1.5rem;
}

.card {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Référence client */
.client-reference {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #E5E7EB;
}

.ref-badge {
  background: #F3F4F6;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #4B5563;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.actif { background: #D1FAE5; color: #065F46; }
.status-badge.inactif { background: #FEE2E2; color: #991B1B; }
.status-badge.prospect { background: #DBEAFE; color: #1E40AF; }
.status-badge.archive { background: #E5E7EB; color: #374151; }

/* Profile Avatar */
.profile-header {
  margin-bottom: 2.5rem;
  text-align: left;
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
  width: 100px;
  height: 100px;
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: 12px;
  border: 4px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
  color: white;
  text-transform: uppercase;
}

.camera-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background: #3B82F6;
  color: white;
  border: 3px solid white;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.camera-btn:hover {
  background: #2563EB;
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.full-width {
  grid-column: span 2;
}

/* Form Controls */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

label {
  color: #374151;
  font-size: 0.9rem;
  font-weight: 500;
}

label:has(+ .input-wrapper input[required]),
label:has(+ .input-wrapper select[required])::after {
  content: " *";
  color: #EF4444;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

input, select, textarea {
  width: 100%;
  padding: 0.85rem 1rem;
  padding-right: 2.5rem;
  border: 1px solid #D1D5DB;
  border-radius: 12px;
  font-size: 0.95rem;
  color: #1F2937;
  outline: none;
  background: white;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
}

textarea {
  resize: vertical;
  min-height: 60px;
  padding: 1rem;
}

input:focus, select:focus, textarea:focus {
  border-color: #3B82F6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

input[readonly], select:disabled {
  background-color: #F9FAFB;
  cursor: not-allowed;
}

/* Icon positioning */
.input-icon {
  position: absolute;
  right: 1rem;
  display: flex;
  align-items: center;
  pointer-events: none;
}

/* Custom styling for Select */
select {
  appearance: none;
  background-color: white;
  cursor: pointer;
}

select:disabled {
  cursor: not-allowed;
}

/* Notes Container */
.notes-container {
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 1rem;
  transition: border-color 0.2s;
}

.notes-container.active {
  border-color: #3B82F6;
  background-color: #F8FAFC;
}

.notes-container textarea {
  border: none;
  background: transparent;
  padding: 0;
}

/* Helper Texts & Status */
.action-link {
  font-size: 0.85rem;
  color: #6B7280;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: color 0.2s;
}

.action-link:hover {
  color: #374151;
}

.status-verified {
  font-size: 0.85rem;
  color: #059669;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #E5E7EB;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: #3B82F6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563EB;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #F3F4F6;
  color: #374151;
}

.btn-secondary:hover {
  background: #E5E7EB;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.modal h3 {
  margin: 0 0 1rem 0;
  color: #111827;
  font-size: 1.25rem;
}

.modal p {
  color: #6B7280;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

/* Spinner */
.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .account-section {
    padding: 1rem;
  }
  
  .card {
    padding: 1.5rem;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }
  
  .full-width {
    grid-column: span 1;
  }
  
  .client-reference {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .section-header h2 {
    font-size: 1.5rem;
  }
  
  .avatar-wrapper {
    width: 80px;
    height: 80px;
  }
}
</style>