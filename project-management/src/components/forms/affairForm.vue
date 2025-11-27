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

        <h4>Constitution du dossier de </h4>
        
        <div class="form-grid">
            
            <div class="form-row">
                <inputfamily 
                    identifiant="titre" 
                    label="Nom du dossier" 
                    placeholder="Entrer le nom du dossier"
                    v-model="formData.titre"
                    :required="true"
                />
                <selectfamily/>
                <selectfamily 
                    label="Priorité"
                    :options="priorities"
                />
            </div>
            
            <div class="form-row">
                <inputfamily 
                    identifiant="CompteContribuable" 
                    label="Numéro Compte Contribuable" 
                    placeholder="Numéro Compte Contribuable"
                    v-model="formData.numero_cc"
                />
                <inputfamily 
                    identifiant="Capitalsocial" 
                    label="Capital social" 
                    placeholder="Votre Capital social"
                    v-model="formData.capital_social"
                />
                <inputfamily 
                    identifiant="adresse" 
                    label="Adresse" 
                    placeholder="Entrer l'adresse"
                    type="text"
                    v-model="formData.adresse"
                    :required="true"
                />
            </div>

            <div class="form-row">
                <inputfamily 
                    identifiant="ville" 
                    label="Ville" 
                    placeholder="Entrer la ville"
                    v-model="formData.ville"
                />
                <inputfamily 
                    identifiant="telephone" 
                    label="Téléphone" 
                    placeholder="Entrer le téléphone"
                    type="tel"
                    v-model="formData.telephone_1"
                />

                <inputfamily 
                    identifiant="telephone 2" 
                    label="Téléphone 2" 
                    placeholder="Entrer le deuxième numéro"
                    v-model="formData.telephone_2"
                />
                
            </div>

            <div class="form-row">
                <inputfamily 
                    identifiant="email" 
                    label="Email" 
                    placeholder="Entrer votre email"
                    v-model="formData.email"
                />
                <inputfamily 
                    identifiant="representantLegal" 
                    label="Nom du representant legal" 
                    placeholder="Entrer le pays"
                    v-model="formData.representant_legal_nom"
                />
                <inputfamily 
                    identifiant="profession" 
                    label="Profession du représentant légal" 
                    placeholder="Entrer la profession"
                    v-model="formData.representant_legal_fonction"
                />
            </div>
        </div>

        <div class="form-actions">
            <prevButton @click="handlePrevStep"/>
            <mainButton 
                :isloading="isLoading"
                label="Ajouter client"
                type="submit"
            >
                
            </mainButton>
        </div>
    </form>
</template>

<script>
import { ref, reactive, watch, onMounted } from 'vue';
import inputfamily from '../input/inputfamily.vue';
import selectfamily from '../input/selectfamily.vue';
import mainButton from '../button/mainButton.vue';
import prevButton from '../button/prevButton.vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import api from '@/_services/api';

export default {
    name: 'ClientMoralForm',
    components: {
        inputfamily,
        selectfamily,
        mainButton,
        prevButton,
    },
    emits: ['submit', 'prevstep', 'notification'],
    setup(props, { emit }) {
        const isLoading = ref(false);
        const errorMessage = ref('');
        const fieldErrors = reactive({});
        const authStore = useAuthStore();
        const router = useRouter();

        const { user, isInitialized } = storeToRefs(authStore);

        // About the payload

        const priorities = ref([
            {value:'Basse', matching:'Basse'},
            {value: 'Normale', matching:'Normale'},
            {value:'Haute', matching:'Haute'},
            {value:'Urgente', name:'urgente'}
        ])

        const formData = reactive({
            titre:"",
            type_dossier:"",
            client:"",
            description:"",
            priorite:"",
            date_echeance:"",
            honoraires_prevues:"",
            numero_tribunal:"",
            juridiction:"",
            observation:"",
            collaborateurs:""
        });

        const clearError = () => {
            errorMessage.value = '';
            Object.keys(fieldErrors).forEach(key => {
                fieldErrors[key] = '';
            });
        };

        const isValidEmail = (email) => {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        };

        const isValidPhone = (phone) => {
            const phoneRegex = /^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,4}[-\s.]?[0-9]{1,9}$/;
            return phoneRegex.test(phone.replace(/\s/g, ''));
        };

        const validateForm = () => {
            clearError();
            let isValid = true;

            if (!formData.raison_sociale.trim()) {
                fieldErrors.raison_sociale = 'La raison sociale est obligatoire';
                isValid = false;
            }

            if (!formData.adresse.trim()) {
                fieldErrors.adresse = 'L\'adresse est obligatoire';
                isValid = false;
            }

            if (!formData.representant_legal_fonction.trim()) {
                fieldErrors.representant_legal_fonction = 'La fonction du représentant légal ne peut être vide';
                isValid = false;
            }

            if (!formData.representant_legal_nom.trim()) {
                fieldErrors.representant_legal_nom = 'Le nom du représentant légal ne peut être vide';
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

            return isValid;
        };

        watch(user, (newUser) => {
            console.log("👀 Watch user déclenché:", newUser);
            if (newUser && newUser.id) {
                formData.charge_de_clientele = newUser.id;
                console.log("✅ ID assigné:", formData.charge_de_clientele);
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
        });

        const handleSubmit = async () => {
            if (!validateForm()) {
                return;
            }

            isLoading.value = true;

            if (!formData.charge_de_clientele && user.value) {
                formData.charge_de_clientele = user.value.id;
            }

            try {
                console.log("Envoi du formulaire avec ID Agent:", formData.charge_de_clientele);

                const response = await api.post('manager/clients/ajouter/', formData);

                emit('notification', {
                    type: 'success',
                    message: 'Client de type firme ajouté avec succès',
                    duration: 5000
                });

                emit('submit', {
                    ...formData,
                    type_client: 'PERSONNE_MORALE'
                });

                setTimeout(()=> {
                    router.push('/dashboard')
                }, 6000)

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
            priorities,
            formData,
            errorMessage,
            fieldErrors,
            clearError,
            handleSubmit,
            handlePrevStep
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
    gap: 2rem;
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