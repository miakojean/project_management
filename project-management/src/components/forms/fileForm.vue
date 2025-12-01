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
                    v-model="formData.date_naissance"
                    :error="fieldErrors.date_naissance"
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
                    formDataToSend.append('dossier', ()=> dossierStore.currentDossier)
                    formDataToSend.append('client', ()=> customer.currentCustomer)

                    // Ajoute chaque fichier
                    uploadedFiles.value.forEach((fileObj, index) => {
                    formDataToSend.append(`files`, fileObj.file);  // ou `fileObj.file` si tu veux le File brut
                });

                const response = await api.post('manager/documents/', formDataToSend, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });

                // Émettre une notification de succès
                emit('notification', {
                    type: 'success',
                    message: 'Document ajouté avec succès',
                    duration: 5000
                });

                // Reset intelligent
                const currentAgent = formData.charge_de_clientele;
                formData.charge_de_clientele = currentAgent;
                formData.type_client = 'PERSONNE_PHYSIQUE';

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
        });

        return {
            isLoading,
            errorMessage,
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