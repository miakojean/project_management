<template>
    <form @submit.prevent="handleSubmit" class="center__flex_start">
        <h3>Se connecter</h3>
        
        <inputfamily 
            v-model="formData.email"
            identifiant="Email_professionnel" 
            label="Email professionnel" 
            placeholder="Entrer votre email professionnel"
            :required="true"
            ref="emailInput"
        />
        <inputfamily 
            v-model="formData.password"
            identifiant="Mot_de_passe" 
            label="Mot de passe" 
            placeholder="Entrer votre mot de passe"
            :required="true"
            ref="passwordInput"
            type="password"
        />
        
        <mainButton type="submit" label="Se connecter" :isloading="isloading"></mainButton>

        <div v-if="message.errorMessage" class="error__message center__flex">
            <p>{{ message.errorMessage }}</p>
        </div>

        <divider />
        
        <div class="w-full flex justify-items-start gap-2">
            <p>Signaler l'oubli du mot de passe</p>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
            </svg>
        </div>
    
    </form>
</template>

<script>
import inputfamily from '../input/inputfamily.vue';
import mainButton from '../button/mainButton.vue';
import divider from '../tools/divider.vue';
import { useRouter } from 'vue-router';
import { reactive, ref } from 'vue';
import api from '@/_services/api';

export default {
    components: {
        inputfamily,
        mainButton,
        divider
    },
    setup() {
        const router = useRouter();
        const isloading = ref(false);

        const message = ref({
            errorMessage: "",
            succesMessage: "",
        });

        const formData = reactive({
            email: "",
            password: ""
        });

        // Refs pour accéder aux méthodes de validation
        const emailInput = ref(null);
        const passwordInput = ref(null);

        const validateData = () => {
            const isEmailValid = emailInput.value?.validate();
            const isPasswordValid = passwordInput.value?.validate();

            if (isEmailValid && isPasswordValid) {
                console.log("Données valides, soumission du formulaire...");
                console.log("Email:", formData.email);
                console.log("Password:", formData.password);
                return true;
            }
            return false;
        };

        const handleSubmit = async () => {
            isloading.value = true;
            // Réinitialiser les messages
            message.value = {
                errorMessage: "",
                succesMessage: ""
            };

            try {
                if (!validateData()) {
                    console.log("Les champs ne sont pas correctement remplis");
                    message.value.errorMessage = "Veuillez remplir tous les champs correctement";
                    return;
                }

                const response = await api.post('/account/login', {
                    email: formData.email,
                    password: formData.password // CORRECTION: "password" au lieu de "passwor"
                });

                console.log("Réponse complète:", response);

                // Gestion flexible des tokens selon la structure de réponse
                let token = null;
                let refreshToken = null;

                // Différentes possibilités de structure de réponse
                if (response.data.access_token) {
                    token = response.data.access_token;
                    refreshToken = response.data.refresh_token;
                } else if (response.data.access) {
                    token = response.data.access;
                    refreshToken = response.data.refresh;
                } else if (response.data.token) {
                    token = response.data.token;
                } else if (response.data.data?.access_token) {
                    token = response.data.data.access_token;
                    refreshToken = response.data.data.refresh_token;
                }

                if (token) {
                    // Stockage des tokens
                    sessionStorage.setItem('authToken', token);
                    if (refreshToken) {
                        sessionStorage.setItem('refresh', refreshToken);
                    }

                    // Réinitialiser le formulaire
                    formData.email = "";
                    formData.password = "";
                    
                    // Redirection
                    router.push('/dashboard');
                } else {
                    throw new Error("Token d'authentification non reçu dans la réponse");
                }

            } catch (error) {
                console.log("Erreur de connexion:", error);
                
                // Gestion des erreurs améliorée
                if (error.response?.status === 401) {
                    message.value.errorMessage = "Email ou mot de passe incorrect";
                } else if (error.response?.status === 400) {
                    message.value.errorMessage = "Données de connexion invalides";
                } else if (error.response?.status === 403) {
                    message.value.errorMessage = "Accès non autorisé";
                } else if (error.response?.status === 404) {
                    message.value.errorMessage = "Service d'authentification non disponible";
                } else if (error.response?.status >= 500) {
                    message.value.errorMessage = "Erreur serveur. Veuillez réessayer plus tard.";
                } else if (error.response?.data?.message) {
                    message.value.errorMessage = error.response.data.message;
                } else if (error.message) {
                    message.value.errorMessage = error.message;
                } else {
                    message.value.errorMessage = "Échec de la connexion. Veuillez réessayer."; // CORRECTION: utilisation de message.value
                }
                
                // Log détaillé pour le débogage
                console.error("Détails de l'erreur:", {
                    status: error.response?.status,
                    data: error.response?.data,
                    message: error.message
                });
            } finally {
                isloading.value = false;
            }
        };
        
        return {
            router,
            isloading,
            message,
            formData,
            emailInput,
            passwordInput,
            validateData,
            handleSubmit
        };
    }
};
</script>

<style scoped>
form {
    width: 100%;
    max-width: 500px;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
}

form h3 {
    text-align: start;
    width: 100%;
    margin-bottom: 1rem;
}

form p, svg {
    color: #2f80ed;
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
</style>