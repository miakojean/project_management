<template>
    <form action="" class="center__flex_start">
        <h3>Enregistrement</h3>
        
        <!-- Step 1 -->
        <template v-if="currentStep === 1">
            <inputfamily identifiant="Nom" label="Nom" placeholder="Entrer votre nom"/>
            <inputfamily identifiant="Prenoms" label="Prenoms" placeholder="Entrer prenom(s)"/>
            <inputfamily identifiant="Email_professionnel" label="Email professionnel" placeholder="Votre email professionnel"/>
            
            <mainButton type="button" @click="currentStep = 2" label="Suivant"></mainButton>
        </template>
        
        <!-- Step 2 -->
        <template v-if="currentStep === 2">
            <inputfamily identifiant="Telephone" label="Téléphone" placeholder="Votre numéro"/>
            <inputfamily identifiant="Poste" label="Poste" placeholder="Votre poste"/>
            <inputfamily identifiant="Departement" label="Département" placeholder="Votre département"/>
            
            <mainButton type="submit">Précédent</mainButton>
        </template>
    </form>
</template>

<script>
import inputfamily from '../input/inputfamily.vue';
import mainButton from '../button/mainButton.vue';
import { ref } from 'vue';

export default {
    components: {
        inputfamily,
        mainButton
    },
    setup() {
        const currentStep = ref(1);
        
        return {
            currentStep
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
</style>