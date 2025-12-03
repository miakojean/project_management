<template>
    <form class="form-container" @submit.prevent="handleSubmit">
        <div v-if="errorMessage" class="error-banner">
            <div class="error-content">
                <span class="error-icon">⚠️</span>
                <span class="error-text">{{ errorMessage }}</span>
                <button class="error-close" @click="clearError">x</button>
            </div>
        </div>

        <!-- Afficher le client sélectionné -->
        <div v-if="currentClient" class="client-info-banner">
            <strong>Client sélectionné :</strong> {{ currentClient.nom_complet }} 
            ({{ currentClient.reference_client }})
        </div>
        <div v-else class="client-warning">
            ⚠️ Aucun client sélectionné
        </div>

        <div class="form-grid">
            
            <div class="form-row">
                <inputfamily 
                    identifiant="FolderName"
                    label="Nom de dossier *"
                    placeholder="Entrer le nom du dossier"
                    v-model="formData.titre"
                    :error="fieldErrors.titre"
                />
                <selectfamily 
                    label="Type de dossier *"
                    :options="dossierTypes"
                    v-model="formData.type_dossier"
                    :error="fieldErrors.type_dossier"
                />
                <selectfamily
                    label="Priorité *" 
                    :options="priority"
                    v-model="formData.priorite"
                    :error="fieldErrors.priorite"
                />
            </div>

            <div class="form-row">
                <inputfamily 
                    identifiant="OpenedDate"
                    label="Date d'échéance"
                    placeholder="Entrer la date d'échéance"
                    v-model="formData.date_echeance"
                    type="date"
                />
                <inputArea 
                    label="Observations"
                    placeholder="Entrer une observation sur le dossier"
                    v-model="formData.observations"
                />
                <inputArea 
                    label="Description *"
                    placeholder="Entrer une description relative au dossier"
                    v-model="formData.description"
                    :show-validation="showValidation"
                    :error-message="fieldErrors.description || 'La description est obligatoire'"
                />
            </div>

            <div class="form-actions">
                <prevButton @click="handlePrev"/>
                <mainButton
                    :isloading="isLoading"
                    label="Créer dossier"
                    type="submit"
                />
            </div>

        </div>
    </form>
</template>

<script>
import { reactive, ref, onMounted, watch, computed } from 'vue';
import { useRouter } from 'vue-router';
import inputfamily from '../input/inputfamily.vue';
import selectfamily from '../input/selectfamily.vue';
import inputArea from '../input/inputArea.vue';
import mainButton from '../button/mainButton.vue';
import prevButton from '../button/prevButton.vue';

import { useAuthStore } from '@/stores/auth';
import { useDossierStore } from '@/stores/dossierStore';
import { useCustomerStore } from '@/stores/custumerStore';

export default {
    name: 'CreateDossierForm',
    components: {
        inputfamily,
        selectfamily,
        inputArea,
        mainButton,
        prevButton
    },
    emits:['notification'],

    setup(props, {emit}) {
        const router = useRouter();
        const isLoading = ref(false);
        const errorMessage = ref('');
        const showValidation = ref(false);
        const fieldErrors = reactive({});

        // Stores
        const authStore = useAuthStore();
        const customerStore = useCustomerStore();
        const dossierStore = useDossierStore();

        // Computed pour le client actuel
        const currentClient = computed(() => {
            return customerStore.currentCustomer || customerStore.getCurrentCustomer;
        });

        // Options pour les selects - CORRECTION DU MAPPING
        const priority = ref([
            { value: 'HAUTE', label: 'Haute' },
            { value: 'NORMALE', label: 'Normale' },
            { value: 'BASSE', label: 'Basse' },
            { value: 'URGENTE', label: 'Urgente' }
        ]);

        const dossierTypes = ref([
            { value: 'CONSTITUTION', label: 'Constitution de société' },
            { value: 'MODIFICATION', label: 'Modification statutaire' },
            { value: 'DISSOLUTION', label: 'Dissolution/Liquidation' },
            { value: 'FUSION_ACQUISITION', label: 'Fusion/Acquisition' },
            { value: 'CONSEIL', label: 'Conseil juridique' },
            { value: 'CONTRAT', label: 'Rédaction de contrat' },
            { value: 'AUDIT', label: 'Audit juridique' },
            { value: 'PROPRIETE_INTELLECTUELLE', label: 'Propriété intellectuelle' },
            { value: 'RECOUVREMENT', label: 'Recouvrement de créances' },
            { value: 'CONTENTIEUX', label: 'Contentieux' },
            { value: 'AUTRE', label: 'Autre' }
        ]);

        // Données du formulaire
        const formData = reactive({
            titre: "",
            type_dossier: "",
            client: "", // Sera rempli automatiquement
            priorite: "NORMALE", // Valeur par défaut
            date_echeance: "",
            observations: "",
            description: "",
            date_ouverture: new Date().toISOString().split('T')[0],
        });

        // Watch pour mettre à jour automatiquement l'ID client
        watch(currentClient, (newClient) => {
            if (newClient && newClient.id) {
                formData.client = newClient.id;
                console.log("✅ Client ID assigné:", formData.client);
            }
        }, { immediate: true });

        // Fonctions
        const clearError = () => {
            errorMessage.value = '';
            Object.keys(fieldErrors).forEach(key => {
                fieldErrors[key] = '';
            });
        };

        const handlePrev = () => {
            router.back();
        };

        const isValid = () => {
            clearError();
            showValidation.value = true;
            let isValid = true;

            // Validation des champs obligatoires
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

            if (!formData.description.trim()) {
                fieldErrors.description = 'La description est obligatoire';
                isValid = false;
            }

            // Vérification du client
            if (!formData.client) {
                errorMessage.value = 'Aucun client sélectionné pour ce dossier';
                isValid = false;
            }

            // Affiche le rapport d'erreur
            if (!isValid) {
                console.log(errorMessage);
            }

            return isValid;
        };


        // Fonction pour créer un dossier
        const handleSubmit = async () => {
            console.log("🔄 Début de la création du dossier...");
            
            if (!isValid()) {
                console.log("soumission echouée!!!")
                return;
            }

            isLoading.value = true;

            try {
                console.log("📦 Données à envoyer:", JSON.stringify(formData, null, 2));

                // Utiliser le store pour créer le dossier
                const nouveauDossier = await dossierStore.createDossier(formData);
                
                console.log("✅ Dossier créé avec succès:", nouveauDossier);

                emit('notification', {
                    type: 'success',
                    message: 'Dossier ajouté avec succès',
                    duration: 4000
                });

                setTimeout(()=> {
                    router.push('/dashboard')
                }, 5000);

                return nouveauDossier;

            } catch (error) {
                console.error('❌ Erreur création dossier:', error);
                
                // Gestion des erreurs
                if (dossierStore.error) {
                    errorMessage.value = dossierStore.error;
                } else if (error.response?.data?.errors) {
                    // Traitement des erreurs de validation de l'API
                    Object.keys(error.response.data.errors).forEach(field => {
                        const fieldName = field.replace(/_/g, ' ');
                        fieldErrors[field] = Array.isArray(error.response.data.errors[field])
                            ? error.response.data.errors[field][0]
                            : error.response.data.errors[field];
                    });
                    errorMessage.value = 'Veuillez corriger les erreurs dans le formulaire';
                } else {
                    errorMessage.value = error.response?.data?.message || error.message || 'Erreur lors de la création du dossier';
                }
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

        onMounted(() => {
            console.log('🔍 Client sélectionné:', currentClient.value);
            console.log('🔍 Utilisateur connecté:', authStore.user);
            
            // S'assurer que l'initialisation est faite
            if (!authStore.user) {
                authStore.initializeAuth();
            }
        });

        return {
            // Stores
            authStore,
            dossierStore,
            customerStore,

            // State
            isLoading,
            errorMessage,
            showValidation,
            fieldErrors,
            currentClient,

            // Form
            priority,
            dossierTypes,
            formData,

            // Functions
            handleSubmit,
            handlePrev,
            clearError
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

.form-grid {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    width: 100%;
}

.form-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr); 
    gap: 1rem;
    align-items: start;
}

.form-actions {
    display: flex;
    justify-content:end;
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