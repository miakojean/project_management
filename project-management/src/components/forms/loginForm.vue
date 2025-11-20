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

export default {
    components: {
        inputfamily,
        mainButton,
        divider
    },
    setup() {

        const router = useRouter();

        const isloading = ref(false);

        const formData = reactive({
            email: "",
            password: ""
        })

        // Refs pour accéder aux méthodes de validation
        const emailInput = ref(null);
        const passwordInput = ref(null);

        const validateData = () => {
            const isEmailValid = emailInput.value?.validate();
            const isPasswordValid = passwordInput.value?.validate();

            if(isEmailValid && isPasswordValid){
                console.log("Données valides, soumission du formulaire...");
                console.log("Email:", formData.email);
                console.log("Password:", formData.password);
                return true;
            }
            return false;
        }

        const handleSubmit = () => {
            if (validateData()) {
                isloading.value = true
                setTimeout(()=>{
                    router.push('/dashboard')
                    console.log("Vous avez réussi ");
                    isloading.value = false
                }, 3000);
            } else {
                console.log("Veuillez corriger les erreurs du formulaire");
            }
        };
        
        return {
            router,
            isloading,
            formData,
            emailInput,
            passwordInput,
            validateData,
            handleSubmit
        }
    }
}
</script>

<style scoped>
form{
    width: 100%;
    max-width: 500px;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem; /* Pour l'espacement entre les éléments */
}

form h3{
    text-align: start;
    width: 100%;
    margin-bottom: 1rem;
}

form p, svg{
    color: #2f80ed;
    font-size: 1rem;
    cursor: pointer;
}


</style>