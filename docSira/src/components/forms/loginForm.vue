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

        <!-- Message d'erreur -->
        <div v-if="errorMessage" class="error__message center__flex">
            <p>{{ errorMessage }}</p>
        </div>

        <!-- Message de succès 
        <div v-if="successMessage" class="success__message center__flex">
            <p>{{ successMessage }}</p>
        </div> -->

        <divider />
        
        <div class="w-full flex justify-items-start gap-2 cursor-pointer" @click="goToPasswordReset">
            <p>Mot de passe oublié?</p>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
            </svg>
        </div>
        
    </form>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
//import { useAuthStore } from '@/stores/auth'; // ✅ IMPORT DU STORE
import inputfamily from '../input/inputfamily.vue';
import mainButton from '../button/mainButton.vue';
import divider from '../tools/divider.vue';

const router = useRouter();
// const authStore = useAuthStore();

// Refs
const isloading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const emailInput = ref(null);
const passwordInput = ref(null);

// Form data
const formData = reactive({
    email: "",
    password: ""
});

// Validation
const validateData = () => {
    const isEmailValid = emailInput.value?.validate();
    const isPasswordValid = passwordInput.value?.validate();

    if (isEmailValid && isPasswordValid) {
        console.log("✅ Données valides, soumission du formulaire...");
        return true;
    }
    
    errorMessage.value = "Veuillez remplir tous les champs correctement";
    return false;
};

// Redirection pour mot de passe oublié
const goToPasswordReset = () => {
    router.push('/reset-password');
};

// Soumission
const handleSubmit = async () => {
    // Réinitialiser les messages
    errorMessage.value = '';
    successMessage.value = '';
    isloading.value = true;

    try {
        // Validation
        if (!validateData()) {
            isloading.value = false;
            return;
        }

        //console.log("🔐 Tentative de connexion...");

        // ✅ UTILISER LE STORE POUR LE LOGIN
        // Le store gère automatiquement les cookies
        await authStore.login({
            email: formData.email,
            password: formData.password
        });

        //console.log("✅ Connexion réussie via le store");
        successMessage.value = "Connexion réussie ! Redirection en cours...";

        // ✅ La redirection est déjà gérée par le store dans `auth.js`
        // ou on peut rediriger manuellement après un délai
        setTimeout(() => {
            router.push('/dashboard');
        }, 1000);

    } catch (error) {
        //console.error("❌ Erreur de connexion:", error);
        
        // ✅ Gestion des erreurs simplifiée - le store a déjà formaté les erreurs
        if (authStore.error) {
            errorMessage.value = authStore.error;
        } else {
            // Fallback si le store n'a pas d'erreur
            const errorData = error.response?.data || {};
            
            if (error.response?.status === 401) {
                errorMessage.value = "Email ou mot de passe incorrect";
            } else if (error.response?.status === 400) {
                errorMessage.value = errorData.error || errorData.message || "Données de connexion invalides";
            } else if (error.response?.status === 403) {
                errorMessage.value = "Accès non autorisé";
            } else if (error.response?.status === 404) {
                errorMessage.value = "Service d'authentification non disponible";
            } else if (error.response?.status >= 500) {
                errorMessage.value = "Erreur serveur. Veuillez réessayer plus tard.";
            } else if (error.message) {
                errorMessage.value = error.message;
            } else {
                errorMessage.value = "Échec de la connexion. Veuillez réessayer.";
            }
        }
        
        // Log détaillé pour le débogage (développement seulement)
        if (process.env.NODE_ENV === 'development') {
            console.error("Détails de l'erreur:", {
                status: error.response?.status,
                data: error.response?.data,
                message: error.message
            });
        }
        
    } finally {
        isloading.value = false;
    }
};
</script>

<style scoped>
form {
    width: 100%;
    max-width: 500px;
    height: 100%;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
}

form h3 {
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
    animation: fadeIn 0.3s ease;
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
    animation: fadeIn 0.3s ease;
}

.success__message p {
    color: #155724;
    font-weight: 500;
    margin: 0;
    text-align: center;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>