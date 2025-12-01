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
            <div class="upload__container">
                <fileInput 
                    ref="fileInputRef"
                    :show-categories="false"
                    @upload-complete="onFilesUploaded"
                />

                <h3> Documents de </h3>
            </div>

                
            <div class="form-row">
                <inputfamily 
                    identifiant="Title" 
                    label="Titre du document" 
                    placeholder="Entrer le titre du document"
                    v-model="formData.titre"
                    :required="true"
                    :error="fieldErrors.titre"
                />
                <inputArea
                    identifiant="Description" 
                    label="Description" 
                    placeholder="Entrer une description"
                    v-model="formData.description"
                    :required="true"
                    :error="fieldErrors.description"
                />
                <selectfamily 
                    identifiant="TypeDoc" 
                    label="Type de documents" 
                    v-model="formData.type_document"
                    :error="fieldErrors.date_naissance"
                    :options="docTypes"
                />
                <div class="form-actions">
                    <prevButton @click="handlePrevStep"/>
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

<script>
import { ref, reactive, watch, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { storeToRefs } from 'pinia';
import inputfamily from '../input/inputfamily.vue';
import inputArea from '../input/inputArea.vue';
import selectfamily from '../input/selectfamily.vue';
import mainButton from '../button/mainButton.vue';
import prevButton from '../button/prevButton.vue';
import fileInput from '../input/fileInput.vue';
import api from '@/_services/api';
import { useRouter } from 'vue-router';
import { useDossierStore } from '@/stores/dossierStore';
import { useDocumentStore} from '@/stores/documentsStore';
import { useCustomerStore } from '@/stores/custumerStore';

export default {
    name: 'FileForm',
    components: {
        inputfamily,
        inputArea,
        selectfamily,
        mainButton,
        prevButton,
        fileInput
    },
    emits: ['prevstep', 'submit', 'notification'],
    setup(props, { emit }) {
        const isLoading = ref(false);
        const errorMessage = ref('');
        const fieldErrors = reactive({});
        const authStore = useAuthStore();
        const router = useRouter();

        // Stores organisation
        const customer = useCustomerStore();
        const dossierStore = useDossierStore();
        const documentStore = useDocumentStore();

        const { user, isInitialized } = storeToRefs(authStore);

        // About form
        const fileInputRef = ref(null);
        const uploadedFiles = ref([]);  // ← on stocke les fichiers ici

        const onFilesUploaded = (payload) => {
            uploadedFiles.value = payload.files;   // on récupère tous les fichiers uploadés
            console.log('Fichiers prêts :', uploadedFiles.value);
        };

        const docTypes = ref([
            {value:'PIECE_IDENTITE', label:'Pièce d\'identité'},
            {value:'STATUT', label:'Statut'},
            {value:'PROCES_VERBAL', label:'Procès verbal'},
            {value:'CONTRAT', label:'Contrat'},
            {value:'COURRIER', label:'Courrier'},
            {value:'ATTESTATION', label:'Attestation'},
            {value:'CERTIFICAT', label:'Certificat'},
            {value:'FACTURE', label:'Facture'},
            {value:'RECU', label:'Reçu'},
            {value:'ACTE', label:'Acte juridique'},
            {value:'JUGEMENT', label:'Jugement'},
            {value:'ORDONNANCE', label:'Ordonnance'},
            {value:'ASSIGNATION', label:'Assignation'},
            {value:'CONCLUSIONS', label:'Conclusions'},
            {value:'MEMOIRE', label:'Mémoire'},
            {value:'RAPPORT', label:'Rapport'},
            {value:'NOTE', label:'Note juridique'},
            {value:'CORRESPONDANCE', label:'Correspondance'},
            {value:'FORMULAIRE', label:'Formulaire administratif'},
            {value:'JUSTIFICATIF', label:'Justificatif'},
            {value:'AUTRE', label:'Autre'}
        ])

        const formData = reactive({
            titre:'',
            description: '',
            type_document: '',
            dossier:'',
            client:'',
        });

        const clearError = () => {
            errorMessage.value = '';
            Object.keys(fieldErrors).forEach(key => {
                fieldErrors[key] = '';
            });
        };

        const validateForm = () => {
            clearError();
            let isValid = true;

            // Validation des champs requis
            if (!formData.titre.trim()) {
                fieldErrors.titre = 'Le nom est obligatoire';
                isValid = false;
            }

            if (!formData.description.trim()) {
                fieldErrors.description = 'Le prénom est obligatoire';
                isValid = false;
            }

            if (!isValid) {
                errorMessage.value = 'Veuillez corriger les erreurs dans le formulaire';
            }

            return isValid;
        };

        const handlePrevStep = () => {
            emit('prevstep');
        };

        const handleSubmit = async () => {
            if (!validateForm()) {
                return;
            }

            isLoading.value = true;
            
            if (!formData.charge_de_clientele && user.value) {
                formData.charge_de_clientele = user.value.id;
            }

            try {
                console.log("📤 Envoi du formulaire avec ID Agent:", formData.charge_de_clientele);

                const formDataToSend = new FormData();
                formDataToSend.append('titre', formData.titre);
                formDataToSend.append('description', formData.description);
                formDataToSend.append('type_document', formData.type_document || 'other');
                
                // CORRECTION ICI : Utilisez .value pour les refs/computed
                if (dossierStore.currentDossier) {
                    formDataToSend.append('dossier', dossierStore.currentDossier.id || dossierStore.currentDossier);
                } else {
                    console.warn('⚠️ Aucun dossier sélectionné');
                    // Gérer l'erreur ou laisser vide selon votre logique métier
                }
                
                if (customer.currentCustomer) {
                    formDataToSend.append('client', customer.currentCustomer.id || customer.currentCustomer);
                } else {
                    console.warn('⚠️ Aucun client sélectionné');
                    // Gérer l'erreur ou laisser vide selon votre logique métier
                }

                // Ajoute chaque fichier
                uploadedFiles.value.forEach((fileObj, index) => {
                    formDataToSend.append(`files`, fileObj.file);
                });

                // Debug: Afficher le contenu de FormData
                for (let [key, value] of formDataToSend.entries()) {
                    console.log(`${key}:`, value);
                }

                const response = await api.post('manager/documents/', formDataToSend, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });

                console.log('✅ Réponse du serveur:', response.data);

                // Émettre une notification de succès
                emit('notification', {
                    type: 'success',
                    message: 'Document ajouté avec succès',
                    duration: 5000
                });

                return response;

            } catch (error) {
                console.error('Erreur lors de la soumission:', error);
                
                let errorMsg = 'Une erreur est survenue lors de l\'ajout du client';
                
                if (error.response) {
                    // Gestion des erreurs de l'API
                    if (error.response.status === 400) {
                        errorMsg = 'Données invalides. Vérifiez les informations saisies.';
                        // Traitement des erreurs de champ spécifiques
                        if (error.response.data) {
                            Object.keys(error.response.data).forEach(field => {
                                const fieldName = field.replace(/_/g, ' ');
                                fieldErrors[field] = Array.isArray(error.response.data[field]) 
                                    ? error.response.data[field][0]
                                    : error.response.data[field];
                            });
                        }
                    } else if (error.response.status === 500) {
                        errorMsg = 'Erreur serveur. Veuillez réessayer plus tard.';
                    }
                }

                errorMessage.value = errorMsg;
                
                // Émettre une notification d'erreur
                emit('notification', {
                    type: 'error',
                    message: errorMsg,
                    duration: 8000
                });

            } finally {
                isLoading.value = false;
            }
        };

        watch(user, (newUser) => {
            console.log("👀 Watch user déclenché:", newUser);
            if (newUser && newUser.id) {
                formData.charge_de_clientele = newUser.id;
                console.log("✅ ID assigné:", formData.charge_de_clientele);
            }
        }, { immediate: true });

        onMounted(async () => {
            if (!user.value && !isInitialized.value) {
                console.log("🔄 User vide, tentative d'initialisation...");
                await authStore.initializeAuth();
            }
            
            // CORRECTION ICI : Vérifiez et récupérez les données séparément
            if (!customer.currentCustomer) {
                console.log('🔍 Tentative de récupération du client courant...');
                // Si vous avez besoin d'appeler une méthode pour récupérer le client courant
                // customer.attachCustomer(customerId) ou autre selon votre logique
            }
            
            if (!dossierStore.currentDossier) {
                console.log('🔍 Tentative de récupération du dossier courant...');
                // Si vous avez besoin d'appeler une méthode pour récupérer le dossier courant
                // dossierStore.attachAffair(dossierId) ou autre selon votre logique
            }
            
            // Debug: Afficher les valeurs actuelles
            console.log('👤 Client courant:', customer.currentCustomer);
            console.log('📁 Dossier courant:', dossierStore.currentDossier);
        });

        return {
            isLoading,
            errorMessage,
            docTypes,
            fieldErrors,
            fileInputRef,
            uploadedFiles,
            onFilesUploaded,
            formData,
            authStore,
            router,
            handlePrevStep,
            handleSubmit,
            clearError,

            // Store
            customer,
            dossierStore,
            documentStore
        };
    }
};
</script>

<style scoped>
.form-container {
    width: 100%;
    max-width: 1000px;
    margin: 0 auto;
    padding-top: 2rem;
}

.form-row {
    display: flex;
    flex-direction: column;
    justify-content: start;
    gap: 1rem;
    width: 50%;
}

.form-actions {
    display: flex;
    gap: 2rem;
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

/* Responsive */
@media (max-width: 992px) {
    .form-row {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 600px) {
    .form-row {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .form-actions {
        justify-content: center;
    }
    
    .form-container {
        padding: 0 1rem;
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

.form-row {
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

/* Stagger animation pour les lignes */
.form-row:nth-child(1) { animation-delay: 0.1s; }
.form-row:nth-child(2) { animation-delay: 0.2s; }
.form-row:nth-child(3) { animation-delay: 0.3s; }
.form-row:nth-child(4) { animation-delay: 0.4s; }
</style>