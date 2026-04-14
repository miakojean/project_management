<template>
    <div class="w-full flex flex-col justify-center items-center gap-4">
        <!-- Étape 1: Demande d'email -->
        <form 
            @submit.prevent="handleEmailSubmit" 
            class="center__flex_start"
            v-if="currentStep === 1"
        >
            <h3>Réinitialiser le mot de passe</h3>
            
            <inputfamily 
                v-model="formData.email"
                identifiant="Email_professionnel" 
                label="Email professionnel" 
                placeholder="Entrer votre email professionnel"
                :required="true"
                ref="emailInput"
                type="email"
            />
            
            <mainButton type="submit" label="Réinitialiser" :isloading="isLoading"></mainButton>

            <div v-if="message.errorMessage" class="error__message center__flex">
                <p>{{ message.errorMessage }}</p>
            </div>

            <div v-if="message.successMessage" class="success__message center__flex">
                <p>{{ message.successMessage }}</p>
            </div>

            <divider />
        </form>

        <!-- Étape 2: Vérification du token -->
        <form 
            @submit.prevent="handleTokenSubmit" 
            class="center__flex_start"
            v-if="currentStep === 2"
        >
            <h3>Copier le token reçu dans votre email</h3>
            
            <inputfamily 
                v-model="formData.token"
                identifiant="Token_réinitialisation" 
                label="Mon token de réinitialisation" 
                placeholder="Entrer votre token de réinitialisation"
                :required="true"
                ref="tokenInput"
            />
            
            <mainButton type="submit" label="Vérifier le token" :isloading="isLoading"></mainButton>

            <div v-if="message.errorMessage" class="error__message center__flex">
                <p>{{ message.errorMessage }}</p>
            </div>

            <div v-if="message.successMessage" class="success__message center__flex">
                <p>{{ message.successMessage }}</p>
            </div>

            <divider />
        </form>

        <!-- Étape 3: Nouveau mot de passe -->
        <form 
            @submit.prevent="handlePasswordSubmit" 
            class="center__flex_start"
            v-if="currentStep === 3"
        >
            <h3>Réinitialiser le mot de passe</h3>
            
            <inputfamily 
                v-model="formData.newPassword"
                identifiant="Nouveau_mot_de_passe" 
                label="Nouveau mot de passe" 
                placeholder="Entrer votre nouveau mot de passe"
                :required="true"
                ref="newPasswordInput"
                type="password"
            />

            <inputfamily 
                v-model="formData.confirmPassword"
                identifiant="Confirmer_mot_de_passe" 
                label="Confirmer le mot de passe" 
                placeholder="Confirmer votre nouveau mot de passe"
                :required="true"
                ref="confirmPasswordInput"
                type="password"
            />
            
            <mainButton type="submit" label="Changer le mot de passe" :isloading="isLoading"></mainButton>

            <div v-if="message.errorMessage" class="error__message center__flex">
                <p>{{ message.errorMessage }}</p>
            </div>

            <div v-if="message.successMessage" class="success__message center__flex">
                <p>{{ message.successMessage }}</p>
            </div>

            <divider />
        </form>

        <!-- Étape 4: Confirmation -->
        <div v-if="currentStep === 4" class="center__flex_start confirmation-step">
            <h3>Réinitialisation réussie !</h3>
            <div class="success__message center__flex">
                <p>Votre mot de passe a été réinitialisé avec succès.</p>
            </div>
            <p class="redirect-text">Vous allez être redirigé vers la page de connexion dans {{ countdown }} secondes...</p>
            <mainButton @click="goToLogin" label="Se connecter maintenant"></mainButton>
        </div>
    </div>
</template>

<script>
import inputfamily from '../input/inputfamily.vue';
import mainButton from '../button/mainButton.vue';
import divider from '../tools/divider.vue';
import { useRouter } from 'vue-router';
import { reactive, ref, computed } from 'vue';
import api from '@/_services/api';

export default {
    components: {
        inputfamily,
        mainButton,
        divider
    },
    setup() {
        const router = useRouter();
        const isLoading = ref(false);
        const currentStep = ref(1);
        const countdown = ref(5);
        let countdownInterval = null;

        const message = ref({
            errorMessage: "",
            successMessage: "",
        });

        const formData = reactive({
            email: "",
            token: "",
            newPassword: "",
            confirmPassword: ""
        });

        // Références aux inputs
        const emailInput = ref(null);
        const tokenInput = ref(null);
        const newPasswordInput = ref(null);
        const confirmPasswordInput = ref(null);

        // Validation des données
        const validateEmailStep = () => {
            if (!emailInput.value?.validate) {
                message.value.errorMessage = "Veuillez saisir un email valide";
                return false;
            }
            return true;
        };

        const validateTokenStep = () => {
            if (!formData.token || formData.token.trim() === '') {
                message.value.errorMessage = "Veuillez saisir le token reçu par email";
                return false;
            }
            return true;
        };

        const validatePasswordStep = () => {
            // Validation du mot de passe
            if (!formData.newPassword || formData.newPassword.length < 8) {
                message.value.errorMessage = "Le mot de passe doit contenir au moins 8 caractères";
                return false;
            }

            if (formData.newPassword !== formData.confirmPassword) {
                message.value.errorMessage = "Les mots de passe ne correspondent pas";
                return false;
            }

            // Validation de la force du mot de passe (optionnel)
            const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
            if (!passwordRegex.test(formData.newPassword)) {
                message.value.errorMessage = "Le mot de passe doit contenir au moins une majuscule, une minuscule, un chiffre et un caractère spécial";
                return false;
            }

            return true;
        };

        // Gestionnaires pour chaque étape
        const handleEmailSubmit = async () => {
            isLoading.value = true;
            resetMessages();

            if (!validateEmailStep()) {
                isLoading.value = false;
                return;
            }

            try {
                const response = await api.post('/account/password-reset', {
                    email: formData.email,
                });

                if (response.status === 200) {
                    message.value.successMessage = response.data.message || "Si un compte existe avec cet email, un lien de réinitialisation a été envoyé.";
                    currentStep.value = 2; // Passer à l'étape du token
                }
            } catch (error) {
                //console.error("Erreur lors de la demande de réinitialisation :", error);
                // Toujours afficher le même message pour des raisons de sécurité
                message.value.successMessage = "Si un compte existe avec cet email, un lien de réinitialisation a été envoyé.";
                currentStep.value = 2; // Passer quand même à l'étape suivante pour la sécurité
            } finally {
                isLoading.value = false;
            }
        };

        const handleTokenSubmit = async () => {
            isLoading.value = true;
            resetMessages();

            if (!validateTokenStep()) {
                isLoading.value = false;
                return;
            }

            try {
                const response = await api.post('/account/password-reset/verify', {
                    token: formData.token.trim(),
                });

                if (response.status === 200 && response.data.valid) {
                    message.value.successMessage = "Token vérifié avec succès. Vous pouvez maintenant définir votre nouveau mot de passe.";
                    currentStep.value = 3; // Passer à l'étape du nouveau mot de passe
                } else {
                    message.value.errorMessage = response.data.message || "Token invalide ou expiré";
                }
            } catch (error) {
                // console.error("Erreur lors de la vérification du token :", error);
                if (error.response && error.response.data) {
                    message.value.errorMessage = error.response.data.message || "Token invalide ou expiré";
                } else {
                    message.value.errorMessage = "Une erreur est survenue lors de la vérification du token";
                }
            } finally {
                isLoading.value = false;
            }
        };

        const handlePasswordSubmit = async () => {
            isLoading.value = true;
            resetMessages();

            if (!validatePasswordStep()) {
                isLoading.value = false;
                return;
            }

            try {
                const response = await api.post('/account/password-reset/confirm', {
                    token: formData.token,
                    new_password: formData.newPassword,
                    new_password2: formData.confirmPassword
                });

                if (response.status === 200) {
                    message.value.successMessage = "Mot de passe réinitialisé avec succès !";
                    currentStep.value = 4; // Étape de confirmation
                    startCountdown();
                }
            } catch (error) {
                // console.error("Erreur lors de la réinitialisation du mot de passe :", error);
                if (error.response && error.response.data) {
                    message.value.errorMessage = error.response.data.error || error.response.data.message || "Une erreur est survenue lors de la réinitialisation";
                } else {
                    message.value.errorMessage = "Une erreur est survenue lors de la réinitialisation du mot de passe";
                }
            } finally {
                isLoading.value = false;
            }
        };

        // Fonctions utilitaires
        const resetMessages = () => {
            message.value = {
                errorMessage: "",
                successMessage: ""
            };
        };

        const startCountdown = () => {
            countdownInterval = setInterval(() => {
                countdown.value--;
                if (countdown.value <= 0) {
                    clearInterval(countdownInterval);
                    goToLogin();
                }
            }, 1000);
        };

        const goToLogin = () => {
            if (countdownInterval) {
                clearInterval(countdownInterval);
            }
            router.push('/login');
        };

        // Nettoyage
        const cleanup = () => {
            if (countdownInterval) {
                clearInterval(countdownInterval);
            }
        };

        return {
            router,
            isLoading,
            currentStep,
            countdown,
            message,
            formData,
            emailInput,
            tokenInput,
            newPasswordInput,
            confirmPasswordInput,
            handleEmailSubmit,
            handleTokenSubmit,
            handlePasswordSubmit,
            goToLogin,
            cleanup
        };
    }
};
</script>

<style scoped>
form, .confirmation-step {
    width: 100%;
    max-width: 500px;
    height: 100%;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
}

form h3, .confirmation-step h3 {
    font-size: 1.5rem;
    text-align: start;
    width: 100%;
    margin-bottom: 1rem;
}

form p, svg {
    color: var(--primary-color);
    font-size: 1rem;
    cursor: pointer;
}

.error__message {
    padding: 0.5rem;
    background: #ffb7b7;
    width: 100%;
    border-radius: 4px;
}

.error__message p {
    color: #bd0000;
    font-weight: 500;
    margin: 0;
    text-align: center;
}

.success__message {
    padding: 0.5rem;
    background: #d4edda;
    width: 100%;
    border-radius: 4px;
}

.success__message p {
    color: #155724;
    font-weight: 500;
    margin: 0;
    text-align: center;
}

.redirect-text {
    color: #666;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

.confirmation-step {
    text-align: center;
}
</style>