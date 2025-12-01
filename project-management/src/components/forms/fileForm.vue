<template>
  <form class="form-container" @submit.prevent="handleSubmit">
    <!-- Notification d'erreur -->
    <div v-if="errorMessage" class="error-banner">
      <div class="error-content">
        <span class="error-icon">⚠️</span>
        <span class="error-text">{{ errorMessage }}</span>
        <button class="error-close" @click="clearError">x</button>
      </div>
    </div>

    <div class="form__body flex w-full gap-8">
      <!-- === ZONE D'UPLOAD === -->
      <div class="upload__container">
        <fileInput 
          ref="fileInputRef"
          v-model="selectedFiles"
          :show-categories="false"
          @error="handleFileError"
        />

        <!-- Message de confirmation -->
        <p v-if="selectedFiles.length > 0" class="files-ready-message">
          ✓ {{ selectedFiles.length }} fichier{{ selectedFiles.length > 1 ? 's' : '' }} sélectionné{{ selectedFiles.length > 1 ? 's' : '' }}
        </p>

        <h3 class="mt-6 text-lg font-semibold">
          Documents de {{ dossierStore.currentDossier?.client?.nom_complet || '...' }}
        </h3>
      </div>

      <!-- === FORMULAIRE === -->
      <div class="form-row flex-1">
        <inputfamily 
          identifiant="Title" 
          label="Titre du document *" 
          placeholder="Entrer le titre du document"
          v-model="formData.titre"
          :required="true"
          :error="fieldErrors.titre"
        />
        <inputArea
          identifiant="Description" 
          label="Description *" 
          placeholder="Entrer une description"
          v-model="formData.description"
          :required="true"
          :error="fieldErrors.description"
        />
        <selectfamily 
          identifiant="TypeDoc" 
          label="Type de document" 
          v-model="formData.type_document"
          :options="docTypes"
          :error="fieldErrors.type_document"
        />

        <div class="form-actions">
          <prevButton @click="handlePrevStep" />
          <mainButton 
            :isloading="isLoading"
            label="Ajouter document"
            type="submit"
          />
        </div>
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import inputfamily from '../input/inputfamily.vue'
import inputArea from '../input/inputArea.vue'
import selectfamily from '../input/selectfamily.vue'
import mainButton from '../button/mainButton.vue'
import prevButton from '../button/prevButton.vue'
import fileInput from '../input/fileInput.vue'
import api from '@/_services/api'
import { useRouter } from 'vue-router'
import { useDossierStore } from '@/stores/dossierStore'
import { useDocumentStore } from '@/stores/documentsStore'
import { useCustomerStore } from '@/stores/custumerStore'

const emit = defineEmits(['prevstep', 'notification'])

const isLoading = ref(false)
const errorMessage = ref('')
const fieldErrors = reactive({})
const authStore = useAuthStore()
const router = useRouter()

// Stores
const customer = useCustomerStore()
const dossierStore = useDossierStore()
const documentStore = useDocumentStore()
const { user, isInitialized } = storeToRefs(authStore)

// Références
const fileInputRef = ref(null)
const selectedFiles = ref([])  // ✅ Lié au v-model de fileInput

// Types de documents
const docTypes = ref([
  { value: 'PIECE_IDENTITE', label: "Pièce d'identité" },
  { value: 'STATUT', label: 'Statut' },
  { value: 'PROCES_VERBAL', label: 'Procès verbal' },
  { value: 'CONTRAT', label: 'Contrat' },
  { value: 'COURRIER', label: 'Courrier' },
  { value: 'ATTESTATION', label: 'Attestation' },
  { value: 'CERTIFICAT', label: 'Certificat' },
  { value: 'FACTURE', label: 'Facture' },
  { value: 'RECU', label: 'Reçu' },
  { value: 'ACTE', label: 'Acte juridique' },
  { value: 'JUGEMENT', label: 'Jugement' },
  { value: 'ORDONNANCE', label: 'Ordonnance' },
  { value: 'ASSIGNATION', label: 'Assignation' },
  { value: 'CONCLUSIONS', label: 'Conclusions' },
  { value: 'MEMOIRE', label: 'Mémoire' },
  { value: 'RAPPORT', label: 'Rapport' },
  { value: 'NOTE', label: 'Note juridique' },
  { value: 'CORRESPONDANCE', label: 'Correspondance' },
  { value: 'FORMULAIRE', label: 'Formulaire administratif' },
  { value: 'JUSTIFICATIF', label: 'Justificatif' },
  { value: 'AUTRE', label: 'Autre' }
])

const formData = reactive({
  titre: '',
  description: '',
  type_document: 'AUTRE',
  charge_de_clientele: '',
  files:''
})

const clearError = () => {
  errorMessage.value = ''
  Object.keys(fieldErrors).forEach(k => delete fieldErrors[k])
}

const validateForm = () => {
  clearError()
  let valid = true

  if (!formData.titre.trim()) {
    fieldErrors.titre = 'Le titre est obligatoire'
    valid = false
  }
  if (!formData.description.trim()) {
    fieldErrors.description = 'La description est obligatoire'
    valid = false
  }
  if (!formData.type_document) {
    fieldErrors.type_document = 'Le type de document est obligatoire'
    valid = false
  }

  // Vérification des fichiers
  if (selectedFiles.value.length === 0) {
    errorMessage.value = 'Veuillez sélectionner au moins un fichier'
    valid = false
  }

  if (!valid) {
    errorMessage.value = 'Veuillez corriger les erreurs dans le formulaire'
  }

  return valid
}

const handleFileError = (error) => {
  errorMessage.value = error
}

const handlePrevStep = () => {
  emit('prevstep')
}

const handleSubmit = async () => {
  if (!validateForm()) return

  isLoading.value = true
  const formDataToSend = new FormData()

  // 1. Ajout de TOUS les fichiers avec la même clé → Django les reçoit en liste
  selectedFiles.value.forEach(file => {
    formDataToSend.append('files', file)
  })

  // 2. Métadonnées (une seule fois pour tous les documents)
  formDataToSend.append('titre', formData.titre)
  formDataToSend.append('description', formData.description)
  formDataToSend.append('type_document', formData.type_document || 'AUTRE')

  if (dossierStore.currentDossier?.id) {
    formDataToSend.append('dossier', dossierStore.currentDossier.id)
  }
  if (dossierStore.currentDossier?.client?.id) {
    formDataToSend.append('client', dossierStore.currentDossier.client.id)
  }

  try {
    const response = await api.post('manager/documents/', formDataToSend)
    
    // Réponse : { message: "X document(s) créé(s)...", documents: [...] }
    const count = response.data.documents?.length || selectedFiles.value.length

    emit('notification', {
      type: 'success',
      message: `${count} document(s) ajouté(s) avec succès`,
      duration: 5000
    })

    // Reset complet
    formData.titre = ''
    formData.description = ''
    formData.type_document = 'AUTRE'
    selectedFiles.value = []
    fileInputRef.value?.reset()

  } catch (error) {
    console.error('Erreur upload:', error)
    const msg = error.response?.data?.detail 
      || error.response?.data?.files?.[0] 
      || 'Erreur lors de l\'envoi des documents'

    errorMessage.value = msg
    emit('notification', { type: 'error', message: msg, duration: 8000 })
  } finally {
    isLoading.value = false
  }
}

// Assignation automatique du chargé de clientèle
watch(user, (u) => {
  if (u?.id) formData.charge_de_clientele = u.id
}, { immediate: true })

onMounted(async () => {
  console.log('📋 Composant fileForm monté')
  console.log('👤 Utilisateur:', user.value)
  console.log('📁 Dossier actuel:', dossierStore.currentDossier)

  if (!user.value && !isInitialized.value) {
    await authStore.initializeAuth()
  }
})
</script>

<style scoped>
.form-container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.form__body {
  display: flex;
  gap: 2rem;
}

.upload__container {
    flex: 1;
    min-width: 0;
}

.files-ready-message {
    margin-top: 1rem;
    padding: 0.75rem;
    background: #f0fdf4;
    border: 1px solid #86efac;
    border-radius: 8px;
    color: #16a34a;
    font-weight: 500;
    text-align: center;
}

.form-row {
    display: flex;
    flex-direction: column;
    justify-content: start;
    gap: 1rem;
    flex: 1;
    min-width: 0;
}

.form-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e5e7eb;
    width: 100%;
}

/* Bannière d'erreur */
.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  animation: slideDown 0.3s ease;
}

.error-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.error-icon {
    font-size: 1.25rem;
    flex-shrink: 0;
}

.error-text {
    color: #dc2626;
    font-weight: 500;
    flex: 1;
}

.error-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    color: #dc2626;
    cursor: pointer;
    padding: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background-color 0.2s;
}

.error-close:hover {
    background-color: #fecaca;
}

h3 {
    color: #374151;
    font-weight: 600;
    margin: 0;
}

/* Responsive */
@media (max-width: 992px) {
    .form__body {
      flex-direction: column;
    }
    
    .form-row {
        width: 100%;
    }
}

@media (max-width: 600px) {
    .form-container {
      padding: 1rem;
    }

    .form-actions {
      flex-direction: column;
    }
    
    .form-actions button {
      width: 100%;
    }

    .error-content {
      align-items: flex-start;
    }
}

/* Animations */
@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.form__body {
    animation: fadeInUp 0.5s ease;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>