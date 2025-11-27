<template>
    <form class="form-container" @submit.prevent="handleSubmit">
        
        <!-- Notification d'erreur -->
        <div v-if="errorMessage" class="error-banner">
            <div class="error-content">
                <span class="error-icon">⚠️</span>
                <span class="error-text">{{ errorMessage }}</span>
            </div>
        </div>

        <h4>Constitution du dossier</h4>
        
        <div class="form-grid">
            
            <div class="form-row">
                <inputfamily 
                    identifiant="titre" 
                    label="Nom du dossier" 
                    placeholder="Entrer le nom du dossier"
                    v-model="formData.titre"
                    :required="true"
                    :error="fieldErrors.titre"
                />
                <selectfamily 
                    identifiant="type_dossier"
                    label="Type de dossier"
                    :options="dossierTypes"
                    v-model="formData.type_dossier"
                    :required="true"
                    :error="fieldErrors.type_dossier"
                />
                <selectfamily 
                    identifiant="priorite"
                    label="Priorité"
                    :options="priorities"
                    v-model="formData.priorite"
                    :required="true"
                    :error="fieldErrors.priorite"
                />
            </div>

            <div class="form-row">
                <inputArea
                    identifiant="observation" 
                    label="Observation" 
                    placeholder="Faire une observation"
                    v-model="formData.observation"
                    :error="fieldErrors.observation"
                />
                <inputArea  
                    identifiant="description" 
                    label="Description" 
                    placeholder="Faire une description"
                    type="text"
                    v-model="formData.description"
                    :error="fieldErrors.description"
                />
                <inputfamily
                    identifiant="date_echeance"
                    label="Date d'échéance"
                    placeholder="JJ/MM/AAAA"
                    type="date"
                    v-model="formData.date_echeance"
                    :error="fieldErrors.date_echeance"
                />
            </div>
        </div>

        <div class="form-actions">
            <prevButton @click="handlePrevStep"/>
            <mainButton 
                :isloading="isLoading"
                label="Créer le dossier"
                type="submit"
            />
        </div>
    </form>
</template>

<script>
import { ref, reactive, watch, onMounted } from 'vue';
import inputfamily from '../input/inputfamily.vue';
import selectfamily from '../input/selectfamily.vue';
import mainButton from '../button/mainButton.vue';
import prevButton from '../button/prevButton.vue';
import inputArea from '../input/inputArea.vue';
import { useAuthStore } from '@/stores/auth';
import { useCustomerStore } from '@/stores/custumerStore';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import api from '@/_services/api';

export default {
    name: 'DossierCreationForm',
    components: {
        inputfamily,
        selectfamily,
        inputArea,
        mainButton,
        prevButton,
    },
    props: {
        selectedClient: {
            type: Object,
            default: null
        }
    },
    emits: ['submit', 'prevstep', 'notification'],
    setup(props, { emit }) {
        const isLoading = ref(false);
        const errorMessage = ref('');
        const fieldErrors = reactive({});
        const router = useRouter();

        // Stores
        const authStore = useAuthStore();
        const customerStore = useCustomerStore();

        // Options pour les selects - CORRECTION DU MAPPING
        const priorities = ref([
            { value: 'Basse', label: 'Basse' },
            { value: 'Normale', label: 'Normale' },
            { value: 'Haute', label: 'Haute' },
            { value: 'Urgente', label: 'Urgente' }
        ]);

        const dossierTypes = ref([
            { value: 'JUDICIAIRE', label: 'Judiciaire' },
            { value: 'ADMINISTRATIF', label: 'Administratif' },
            { value: 'CONSEIL', label: 'Conseil' },
            { value: 'AUTRE', label: 'Autre' }
        ]);

        // Structure des données CORRIGÉE
        const formData = reactive({
            titre: "",
            type_dossier: "",
            client: "", // Sera rempli via props.selectedClient
            description: "",
            priorite: "Normale", // Valeur par défaut
            date_echeance: "",
            observation: "",
            collaborateurs: [],
            charge_de_clientele: "" // Sera rempli via user.id
        });

        const clearError = () => {
            errorMessage.value = '';
            Object.keys(fieldErrors).forEach(key => {
                fieldErrors[key] = '';
            });
        };

        // VALIDATION CORRECTE POUR UN DOSSIER
        const validateForm = () => {
            clearError();
            let isValid = true;

            // Validation des champs obligatoires pour un dossier
            if (!formData.titre.trim()) {
                fieldErrors.titre = 'Le nom du dossier est obligatoire';
                isValid = false;
            }

            if (!formData.type_dossier) {
                fieldErrors.type_dossier = 'Le type de dossier est obligatoire';
                isValid = false;
            }

            if (!formData.priorite) {
                fieldErrors.priorite = 'La priorité est obligatoire';
                isValid = false;
            }

            // Vérifier qu'un client est sélectionné
            if (!formData.client) {
                errorMessage.value = 'Aucun client sélectionné pour ce dossier';
                isValid = false;
            }

            // Validation de la date d'échéance si fournie
            if (formData.date_echeance) {
                const selectedDate = new Date(formData.date_echeance);
                const today = new Date();
                today.setHours(0, 0, 0, 0);

                if (selectedDate < today) {
                    fieldErrors.date_echeance = 'La date d\'échéance ne peut pas être dans le passé';
                    isValid = false;
                }
            }

            return isValid;
        };

        // WATCHERS POUR REMPLIR AUTOMATIQUEMENT LES IDs
        watch(() => props.selectedClient, (newClient) => {
            if (newClient && newClient.id) {
                formData.client = newClient.id;
                console.log("✅ Client ID assigné:", formData.client);
            }
        }, { immediate: true });

        watch(user, (newUser) => {
            console.log("👀 Watch user déclenché:", newUser);
            if (newUser && newUser.id) {
                formData.charge_de_clientele = newUser.id;
                console.log("✅ Agent ID assigné:", formData.charge_de_clientele);
            }
        }, { immediate: true });

        const handlePrevStep = () => {
            emit('prevstep');
        };

        onMounted(async () => {
            if (!user.value && !isInitialized.value) {
                console.log("🔄 User vide, tentative d'initialisation...");
                await authStore.initializeAuth();
            }
            else{
                console.log("Utilisateur selectionné", authStore.userProfile)
            }
        });

        const handleSubmit = async () => {
            if (!validateForm()) {
                return;
            }

            isLoading.value = true;

            // S'assurer que les IDs sont bien définis
            if (!formData.charge_de_clientele && user.value) {
                formData.charge_de_clientele = user.value.id;
            }

            try {
                console.log("📦 Données du dossier à envoyer:", JSON.stringify(formData, null, 2));

                // UTILISER LE BON ENDPOINT POUR LES DOSSIERS
                const response = await api.post('dossiers/creer/', formData);

                emit('notification', {
                    type: 'success',
                    message: 'Dossier créé avec succès',
                    duration: 5000
                });

                emit('submit', formData);

                // Redirection après succès
                setTimeout(() => {
                    router.push('/dashboard');
                }, 3000);

                return response;

            } catch (error) {
                console.error('❌ Erreur lors de la création du dossier:', error);

                let errorMsg = 'Une erreur est survenue lors de la création du dossier';

                if (error.response) {
                    if (error.response.status === 400) {
                        errorMsg = 'Données invalides. Vérifiez les informations saisies.';
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
                    } else if (error.response.status === 403) {
                        errorMsg = 'Vous n\'avez pas les permissions pour créer un dossier.';
                    }
                } else if (error.request) {
                    errorMsg = 'Impossible de contacter le serveur. Vérifiez votre connexion.';
                }

                errorMessage.value = errorMsg;

                emit('notification', {
                    type: 'error',
                    message: errorMsg,
                    duration: 8000
                });

            } finally {
                isLoading.value = false;
            }
        };

        return {
            isLoading,
            priorities,
            dossierTypes,
            formData,
            errorMessage,
            fieldErrors,
            clearError,
            handleSubmit,
            handlePrevStep,
            authStore,
            customerStore
        };
    }
};
</script>

<style scoped>
.form-container {
    width: 100%;
    max-width: 1000px; /* Augmenté un peu pour accommoder 3 colonnes */
    margin: 0 auto;
    padding-top: 4rem;
}

.form-grid {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    width: 100%;
}

.form-row {
    display: grid;
    /* C'est ici que se joue le 3 par 3 */
    grid-template-columns: repeat(3, 1fr); 
    gap: 1rem;
    align-items: start;
}

.form-actions {
    display: flex;
    justify-content: center;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e5e7eb;
    width: 100%;
    gap: 1rem;
}

/* Responsive */
@media (max-width: 992px) {
    /* Sur tablette moyenne, on passe à 2 colonnes */
    .form-row {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 600px) {
    /* Sur mobile, on passe à 1 colonne */
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
}

/* Animation */
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