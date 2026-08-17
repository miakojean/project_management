<template>
  <form action="" @submit.prevent="handleSubmit">
    <input-family 
      label="Email/Username" 
      placeholder="Entrer nom utilisateur/email"
      v-model="loginForm.email"
    />
    <input-family 
      label="Mot de passe" 
      type="password" placeholder="Entrer votre mot de passe"
      v-model="loginForm.password"
    />
    <mainButton label="se connecter"/>
    <p v-if="!isValid">{{messageForm.message}}</p>
  </form>
</template>

<script lang="ts">
import { ref, computed } from 'vue'
import inputFamily from '../BaseInput/inputfamily.vue'
import mainButton from '../buttons/mainButton.vue'
import type { LoginForm } from "../../types/auth"
import { isValidLoginForm } from '../../utils/forms'

export default {
  components: { inputFamily, mainButton },
  setup() {
    const loginForm = ref<LoginForm>({ 
      email: '',
      password: ''
    })

    const messageForm = ref({ message: '' })

    // computed réactive : se recalcule à chaque modification de loginForm
    const isValid = computed(() => isValidLoginForm(loginForm.value))

    function handleSubmit() {
      messageForm.value.message = "";
      if (!isValid.value) {
        console.log("Formulaire invalide", loginForm.value); // log here
        messageForm.value.message = "Veuillez remplir tous les champs";
        return;
      }
      console.log("Formulaire valide, envoie des données au serveur");
    }

    return {
      messageForm,
      loginForm,
      isValid,   // dans le template, pas besoin de .value
      handleSubmit
    }
  }
}
</script>

<style scoped>
form{
  width: 100%;
  max-width: 500px;
}
</style>
