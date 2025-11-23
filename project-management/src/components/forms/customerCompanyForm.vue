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
            
            <!-- Informations de l'entreprise -->
            <div class="form-row">
                <inputfamily 
                    identifiant="raison-sociale" 
                    label="Raison sociale *" 
                    placeholder="Entrer la raison sociale"
                    v-model="formData.raison_sociale"
                    :required="true"
                    :error="fieldErrors.raison_sociale"
                />
                <inputfamily 
                    identifiant="forme-juridique" 
                    label="Forme juridique *" 
                    placeholder="Ex: SARL, SA, SAS, etc."
                    v-model="formData.forme_juridique"
                    :required="true"
                    :error="fieldErrors.forme_juridique"
                />
                 <inputfamily 
                    identifiant="capital-social" 
                    label="Capital social (FCFA)" 
                    placeholder="0.00"
                    type="number"
                    v-model="formData.capital_social"
                    :error="fieldErrors.capital_social"
                />
            </div>
            
            <!-- Numéros d'immatriculation -->
            <div class="form-row">
                <inputfamily 
                    identifiant="numero-rccm" 
                    label="Numéro RCCM *" 
                    placeholder="Entrer le numéro RCCM"
                    v-model="formData.numero_rccm"
                    :required="true"
                    :error="fieldErrors.numero_rccm"
                />
                <inputfamily 
                    identifiant="numero-cc" 
                    label="Numéro Compte Contribuable" 
                    placeholder="Entrer le numéro de compte contribuable"
                    v-model="formData.numero_cc"
                    :error="fieldErrors.numero_cc"
                />
            </div>

            <!-- Coordonnées -->
            <div class="form-row">
                <inputfamily 
                    identifiant="adresse" 
                    label="Adresse siège *" 
                    placeholder="Entrer l'adresse du siège"
                    type="text"
                    v-model="formData.adresse"
                    :required="true"
                    :error="fieldErrors.adresse"
                />
                <inputfamily 
                    identifiant="ville" 
                    label="Ville *" 
                    placeholder="Entrer la ville"
                    v-model="formData.ville"
                    :required="true"
                    :error="fieldErrors.ville"
                />
                <inputfamily 
                    identifiant="commune" 
                    label="Commune" 
                    placeholder="Entrer la commune"
                    v-model="formData.commune"
                    :error="fieldErrors.commune"
                />
            </div>

            <!-- Contacts -->
            <div class="form-row">
                <inputfamily 
                    identifiant="telephone" 
                    label="Téléphone *" 
                    placeholder="Entrer le téléphone"
                    type="tel"
                    v-model="formData.telephone_1"
                    :required="true"
                    :error="fieldErrors.telephone_1"
                />

                <inputfamily 
                    identifiant="telephone-2" 
                    label="Téléphone 2 (optionnel)" 
                    placeholder="Entrer le deuxième numéro"
                    v-model="formData.telephone_2"
                    :error="fieldErrors.telephone_2"
                />
                
                <inputfamily 
                    identifiant="email" 
                    label="Email *" 
                    placeholder="Entrer l'email de l'entreprise"
                    v-model="formData.email"
                    :required="true"
                    :error="fieldErrors.email"
                />
            </div>

            <!-- Représentant légal -->
            <div class="form-section">
                <h4 class="section-title">Représentant Légal</h4>
                <div class="form-row">
                    <inputfamily 
                        identifiant="representant-legal-nom" 
                        label="Nom complet *" 
                        placeholder="Entrer le nom du représentant légal"
                        v-model="formData.representant_legal_nom"
                        :required="true"
                        :error="fieldErrors.representant_legal_nom"
                    />
                    <inputfamily 
                        identifiant="representant-legal-fonction" 
                        label="Fonction *" 
                        placeholder="Ex: PDG, Directeur Général, Gérant"
                        v-model="formData.representant_legal_fonction"
                        :required="true"
                        :error="fieldErrors.representant_legal_fonction"
                    />
                </div>
            </div>

            <!-- Informations complémentaires -->
            <div class="form-section">
                <h4 class="section-title">Informations Complémentaires</h4>
                <div class="form-row">
                    <inputfamily 
                        identifiant="date-premier-contact" 
                        label="Date premier contact" 
                        type="date"
                        v-model="formData.date_premier_contact"
                        :error="fieldErrors.date_premier_contact"
                    />
                    <inputfamily 
                        identifiant="notes" 
                        label="Notes internes" 
                        placeholder="Notes sur le client"
                        type="textarea"
                        v-model="formData.notes"
                        :error="fieldErrors.notes"
                    />
                </div>
            </div>
        </div>

        <div class="form-actions">
            <prevButton @click="handlePrevStep"/>
            <mainButton 
                :isloading="isLoading"
                label="Ajouter l'entreprise"
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
    name: 'ClientCompanyForm',
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
            type_client: 'PERSONNE_MORALE',
            raison_sociale: '',
            forme_juridique: '',
            numero_rccm: '',
            numero_cc: '',
            capital_social: '',
            adresse: '',
            ville: '',
            commune: '',
            telephone_1: '',
            telephone_2: '',
            email: '',
            representant_legal_nom: '',
            representant_legal_fonction: '',
            date_premier_contact: new Date().toISOString().split('T')[0], // Date du jour par défaut
            notes: '',
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

            // Validation des champs requis pour personne morale
            if (!formData.raison_sociale.trim()) {
                fieldErrors.raison_sociale = 'La raison sociale est obligatoire';
                isValid = false;
            }

            if (!formData.forme_juridique.trim()) {
                fieldErrors.forme_juridique = 'La forme juridique est obligatoire';
                isValid = false;
            }

            if (!formData.numero_rccm.trim()) {
                fieldErrors.numero_rccm = 'Le numéro RCCM est obligatoire';
                isValid = false;
            }

            if (!formData.adresse.trim()) {
                fieldErrors.adresse = 'L\'adresse du siège est obligatoire';
                isValid = false;
            }

            if (!formData.ville.trim()) {
                fieldErrors.ville = 'La ville est obligatoire';
                isValid = false;
            }

            if (!formData.telephone_1.trim()) {
                fieldErrors.telephone_1 = 'Le téléphone est obligatoire';
                isValid = false;
            }

            if (!formData.email.trim()) {
                fieldErrors.email = 'L\'email est obligatoire';
                isValid = false;
            }

            if (!formData.representant_legal_nom.trim()) {
                fieldErrors.representant_legal_nom = 'Le nom du représentant légal est obligatoire';
                isValid = false;
            }

            if (!formData.representant_legal_fonction.trim()) {
                fieldErrors.representant_legal_fonction = 'La fonction du représentant légal est obligatoire';
                isValid = false;
            }

            // Validation email
            if (formData.email && !isValidEmail(formData.email)) {
                fieldErrors.email = 'Format d\'email invalide';
                isValid = false;
            }

            // Validation téléphone
            if (formData.telephone_1 && !isValidPhone(formData.telephone_1)) {
                fieldErrors.telephone_1 = 'Format de téléphone invalide';
                isValid = false;
            }

            if (formData.telephone_2 && !isValidPhone(formData.telephone_2)) {
                fieldErrors.telephone_2 = 'Format de téléphone invalide';
                isValid = false;
            }

            // Validation capital social
            if (formData.capital_social && parseFloat(formData.capital_social) < 0) {
                fieldErrors.capital_social = 'Le capital social ne peut pas être négatif';
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
                console.log("📤 Envoi du formulaire entreprise avec ID Agent:", formData.charge_de_clientele);

                // Préparer les données pour l'API
                const submitData = {
                    ...formData,
                    capital_social: formData.capital_social ? parseFloat(formData.capital_social) : null,
                    type_client: 'PERSONNE_MORALE'
                };

                const response = await api.post('manager/clients/ajouter/', submitData);

                // Émettre une notification de succès
                emit('notification', {
                    type: 'success',
                    message: 'Entreprise ajoutée avec succès',
                    duration: 5000
                });

                emit('submit', submitData);

                // Reset intelligent
                const currentAgent = formData.charge_de_clientele;
                Object.keys(formData).forEach(key => {
                    if (key !== 'type_client') {
                        formData[key] = '';
                    }
                });
                formData.charge_de_clientele = currentAgent;
                formData.type_client = 'PERSONNE_MORALE';
                formData.date_premier_contact = new Date().toISOString().split('T')[0]; // Reset à la date du jour

                return response;

            } catch (error) {
                console.error('Erreur lors de la soumission:', error);
                
                let errorMsg = 'Une erreur est survenue lors de l\'ajout de l\'entreprise';
                
                if (error.response) {
                    // Gestion des erreurs de l'API
                    if (error.response.status === 400) {
                        errorMsg = 'Données invalides. Vérifiez les informations saisies.';
                        // Traitement des erreurs de champ spécifiques
                        if (error.response.data && error.response.data.errors) {
                            Object.keys(error.response.data.errors).forEach(field => {
                                const fieldName = field.replace(/_/g, ' ');
                                fieldErrors[field] = Array.isArray(error.response.data.errors[field]) 
                                    ? error.response.data.errors[field][0]
                                    : error.response.data.errors[field];
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
    grid-template-columns: repeat(3, 1fr); 
    gap: 1rem;
    align-items: start;
}

.form-section {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1.5rem;
    background: #fafafa;
}

.section-title {
    margin: 0 0 1rem 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: #374151;
    border-bottom: 2px solid #3b82f6;
    padding-bottom: 0.5rem;
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
    
    .form-section {
        padding: 1rem;
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
    
    .form-section {
        padding: 0.75rem;
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
.form-row:nth-child(5) { animation-delay: 0.5s; }
</style>