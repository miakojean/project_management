<template>
    <form class="form-container" @submit.prevent="handleSubmit">
        <!-- Notification d'erreur -->
        <div v-if="errorMessage" class="error-banner">
            <div class="error-content">
                <span class="error-icon">⚠️</span>
                <span class="error-text">{{ errorMessage }}</span>
                <button class="error-close" @click="clearError">×</button>
            </div>
        </div>

        <div class="form-grid">
            
            <div class="form-row">
                <inputfamily 
                    identifiant="nom" 
                    label="Nom" 
                    placeholder="Entrer le nom du client"
                    v-model="formData.nom"
                    :required="true"
                    :error="fieldErrors.nom"
                />
                <inputfamily 
                    identifiant="prenoms" 
                    label="Prénom(s)" 
                    placeholder="Entrer prénom(s)"
                    v-model="formData.prenoms"
                    :required="true"
                    :error="fieldErrors.prenoms"
                />
                 <inputfamily 
                    identifiant="date-naissance" 
                    label="Date de naissance" 
                    placeholder="JJ/MM/AAAA"
                    type="date"
                    v-model="formData.date_naissance"
                    :error="fieldErrors.date_naissance"
                />
            </div>
            
            <div class="form-row">
                <inputfamily 
                    identifiant="lieu-naissance" 
                    label="Lieu de naissance" 
                    placeholder="Entrer le lieu de naissance"
                    v-model="formData.lieu_naissance"
                    :error="fieldErrors.lieu_naissance"
                />
                <inputfamily 
                    identifiant="adresse" 
                    label="Adresse" 
                    placeholder="Entrer l'adresse"
                    type="text"
                    v-model="formData.adresse"
                    :required="true"
                    :error="fieldErrors.adresse"
                />
                <inputfamily 
                    identifiant="ville" 
                    label="Ville" 
                    placeholder="Entrer la ville"
                    v-model="formData.ville"
                    :error="fieldErrors.ville"
                />
            </div>

            <div class="form-row">
                <inputfamily 
                    identifiant="telephone" 
                    label="Téléphone" 
                    placeholder="Entrer le téléphone"
                    type="tel"
                    v-model="formData.telephone_1"
                    :error="fieldErrors.telephone_1"
                />

                <inputfamily 
                    identifiant="telephone 2" 
                    label="Téléphone 2 *(optionnel)" 
                    placeholder="Entrer le deuxième numéro"
                    v-model="formData.telephone_2"
                    :error="fieldErrors.telephone_2"
                />
                
                <inputfamily 
                    identifiant="email" 
                    label="Email" 
                    placeholder="Entrer votre email"
                    v-model="formData.email"
                    :error="fieldErrors.email"
                />
            </div>

            <div class="form-row">
                <inputfamily 
                    identifiant="representantLegal" 
                    label="Nom du representant legal" 
                    placeholder="Entrer le nom du representant legal"
                    v-model="formData.representant_legal_nom"
                    :error="fieldErrors.representant_legal_nom"
                />
                <inputfamily 
                    identifiant="representantLegalRole" 
                    label="Représentant légal fonction" 
                    placeholder="Entrer la fonction"
                    v-model="formData.representant_legal_fonction"
                    :error="fieldErrors.representant_legal_fonction"
                />
            </div>
        </div>

        <div class="form-actions">
            <prevButton @click="handlePrevStep"/>
            <mainButton 
                :isloading="isLoading"
                label="Ajouter client"
                type="submit"
            />
        </div>
    </form>
</template>

<script>
import { ref, reactive, watch, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { storeToRefs } from 'pinia';
import inputfamily from '../input/inputfamily.vue';
import mainButton from '../button/mainButton.vue';
import prevButton from '../button/prevButton.vue';
import api from '@/_services/api';
import { useRouter } from 'vue-router';

export default {
    name: 'ClientPhysiqueForm',
    components: {
        inputfamily,
        mainButton,
        prevButton
    },
    emits: ['prevstep', 'submit', 'notification'],
    setup(props, { emit }) {
        const isLoading = ref(false);
        const errorMessage = ref('');
        const fieldErrors = reactive({});
        const authStore = useAuthStore();
        const router = useRouter();

        const { user, isInitialized } = storeToRefs(authStore);

        const formData = reactive({
            type_client: 'PERSONNE_PHYSIQUE',
            nom: '',
            prenoms: '',
            date_naissance: '',
            lieu_naissance: '',
            adresse: '',
            ville: '',
            commune: '',
            telephone_1: '',
            telephone_2: '',
            email: '',
            representant_legal_nom: '',
            representant_legal_fonction: '',
            charge_de_clientele: '',
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
            if (!formData.nom.trim()) {
                fieldErrors.nom = 'Le nom est obligatoire';
                isValid = false;
            }

            if (!formData.prenoms.trim()) {
                fieldErrors.prenoms = 'Le prénom est obligatoire';
                isValid = false;
            }

            if (!formData.adresse.trim()) {
                fieldErrors.adresse = 'L\'adresse est obligatoire';
                isValid = false;
            }

            // Validation email si fourni
            if (formData.email && !isValidEmail(formData.email)) {
                fieldErrors.email = 'Format d\'email invalide';
                isValid = false;
            }

            // Validation téléphone si fourni
            if (formData.telephone_1 && !isValidPhone(formData.telephone_1)) {
                fieldErrors.telephone_1 = 'Format de téléphone invalide';
                isValid = false;
            }

            if (!isValid) {
                errorMessage.value = 'Veuillez corriger les erreurs dans le formulaire';
            }

            return isValid;
        };

        const isValidEmail = (email) => {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        };

        const isValidPhone = (phone) => {
            const phoneRegex = /^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,4}[-\s.]?[0-9]{1,9}$/;
            return phoneRegex.test(phone.replace(/\s/g, ''));
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

                const response = await api.post('manager/clients/ajouter/', formData);

                // Émettre une notification de succès
                emit('notification', {
                    type: 'success',
                    message: 'Client ajouté avec succès',
                    duration: 5000
                });

                emit('submit', {
                    ...formData,
                    type_client: 'PERSONNE_PHYSIQUE'
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

        return {
            isLoading,
            errorMessage,
            fieldErrors,
            formData,
            authStore,
            router,
            handlePrevStep,
            handleSubmit,
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