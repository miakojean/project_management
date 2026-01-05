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
        <selectfamily label="Type de client *" identifiant="type_client" v-model="form.type_client" :options="typeClientOptions" option-label="label" option-value="value" />
        <selectfamily label="Statut du client *" identifiant="statut" v-model="form.statut" :options="statutOptions" option-label="label" option-value="value" />
        
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
          <inputfamily label="Capital social" identifiant="capital_social" v-model="form.capital_social" />
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
        <inputfamily label="Téléphone" identifiant="telephone" type="tel" v-model="form.telephone_1" />
        <inputfamily label="Téléphone 2" identifiant="telephone2" type="tel" v-model="form.telephone_2" />
        <inputfamily label="Email" identifiant="email" type="email" v-model="form.email" />
        <!--
          <inputfamily label="Chargé de clientèle" identifiant="charge_de_clientele" v-model="form.charge_de_clientele" />
        -->
        <!-- Date premier contact -->
        <inputfamily label="Date de premier contact" identifiant="date_premier_contact" type="date" v-model="form.date_premier_contact" />

        <!-- Boutons d'action -->
        <div class="form-actions full-width">
          <mainButton @click="showConfirmModal = true" :disabled="isSaving" :isLoading="isSaving" label="Enregistrer">
          </mainButton>
        </div>
      </form>
    </div>

    <confirm-modale
      :isOpen="showConfirmModal"
      title="Confirmer l'enregistrement"
      message="Êtes-vous sûr de vouloir enregistrer les modifications ?"
      confirmText="Confirmer"
      cancelText="Annuler"
      @confirm="confirmSave"
      @close="showConfirmModal = false"
    ></confirm-modale>

    <notification-popup
      :message="notificationSettings.message"
      :type="notificationSettings.type"
      :duration="notificationSettings.duration"
      :visible="notificationSettings.visible"
      @close="notificationSettings.visible = false"
    />

  </div>
</template>

<script>
import { ref, reactive, onMounted, watch, computed } from 'vue';
import { useRouter } from 'vue-router'; // Import du router pour la redirection si nécessaire
import inputfamily from '../input/inputfamily.vue';
import inputArea from '../input/inputArea.vue';
import selectfamily from '../input/selectfamily.vue';
import confirmModale from '../modales/confirmModale.vue';
import { useCustomerStore } from '@/stores/custumerStore';
import mainButton from '../button/mainButton.vue';
import prevButton from '../button/prevButton.vue';
import notificationPopup from '../tools/notificationPopup.vue';

export default {
  name: 'CustomerSectionInfo',
  components: {
    confirmModale,
    inputfamily,
    mainButton,
    prevButton,
    selectfamily,
    inputArea,
    notificationPopup
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

    // Dans setup(), avant le return, ajoutez :
    const typeClientOptions = ref([
      { label: 'Personne Physique', value: 'PERSONNE_PHYSIQUE' },
      { label: 'Personne Morale', value: 'PERSONNE_MORALE' }
    ]);

    const statutOptions = ref([
      { label: 'Actif', value: 'ACTIF' },
      { label: 'Inactif', value: 'INACTIF' },
      { label: 'Prospect', value: 'PROSPECT' },
      { label: 'Archivé', value: 'ARCHIVE' }
    ]);

    // Modèle de données
    const form = reactive({
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

    const notificationSettings = ref({
      message: '',
      type: 'success',
      duration: 3000,
      visible: false
    });

    const confirmSave = async () => {
      isSaving.value = true;
      showConfirmModal.value = false;
      
      try {
        // 1. On copie TOUT le formulaire (votre logique est respectée)
        const dataToSave = { ...form };
        
        // 2. IDENTIFICATION DU CLIENT
        // On s'assure d'avoir un ID. Priorité : Formulaire > Props > Store
        const idToUpdate = form.id || props.clientId || clientStore.currentCustomer?.id;

        if (!idToUpdate) {
            throw new Error("Impossible de trouver l'ID du client à mettre à jour.");
        }

        // 3. NETTOYAGE TECHNIQUE (Indispensable pour Django)
        
        // -> Gestion des DATES : Convertir "" en null
        // Sinon Django renvoie : "Date has wrong format"
        ['date_naissance', 'date_premier_contact'].forEach(field => {
            if (dataToSave[field] === '') {
                dataToSave[field] = null; 
            }
        });

        // -> Gestion des NOMBRES : Convertir "" en null et string en float
        // Sinon Django renvoie : "A valid number is required"
        if (dataToSave.capital_social === '' || dataToSave.capital_social === null) {
            dataToSave.capital_social = null;
        } else {
            // S'assurer que c'est bien un nombre pour l'API
            dataToSave.capital_social = parseFloat(dataToSave.capital_social);
        }

        // -> RETRAIT DES CHAMPS LECTURE SEULE
        // On évite d'envoyer ces champs pour ne pas polluer la requête ou trigger des erreurs
        delete dataToSave.reference_client; // Souvent généré auto
        delete dataToSave.date_creation;

        // 4. ENVOI
        console.log("Envoi des données pour mise à jour :", dataToSave);
        await clientStore.updateCustomer(idToUpdate, dataToSave);
        
        // 5. SUCCÈS
        notificationSettings.value = {
          message: 'Client mis à jour avec succès !',
          type: 'success',
          duration: 3000,
          visible: true
        };        
        // On recharge pour être sûr d'avoir les données confirmées par le serveur
        await loadClientData(); 
        
      } catch (error) {
        console.error('Erreur save:', error);
        
        // Affichage intelligent de l'erreur pour comprendre ce qui bloque
        let errorMsg = error.message || 'Erreur inconnue';
        
        if (error.response && error.response.data) {
            // Si le backend renvoie des détails (ex: "Ce champ est obligatoire")
            if (error.response.data.errors) {
                errorMsg = "Erreur de validation :\n" + JSON.stringify(error.response.data.errors, null, 2);
            } else if (error.response.data.message) {
                errorMsg = error.response.data.message;
            }
        }
        
        alert(errorMsg);
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

    watch(() => form.type_client, (newVal, oldVal) => {
      if (newVal !== oldVal) {
        handleClientTypeChange();
      }
    });

    return {
      form,
      isSaving,
      isLoading,
      editNotes,
      showConfirmModal,
      chargeDeClienteleOptions,
      typeClientOptions,
      statutOptions,
      notificationSettings,
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
  background: var(--primary-color);
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