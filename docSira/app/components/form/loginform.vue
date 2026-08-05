<template>
    <form action="">
        <input-family label="Email/Username" placeholder="Entrer nom utilisateur/email"/>
        <input-family label="Mot de passe" type="password" placeholder="Entrer votre mot de passe"/>
        <mainButton label="se connecter"/>
    </form>
</template>

<script lang=ts>
import {ref} from 'vue'
import inputFamily from '../BaseInput/inputfamily.vue';
import mainButton from '../buttons/mainButton.vue';

import type { LoginForm } from "../../types/auth"

export default {
  components: {
    inputFamily,
    mainButton
  },
  setup(){
    const loginForm = ref<LoginForm>({
      email: '',
      password: ''
    })

    return{
      loginForm
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
