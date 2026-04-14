<template>
    
    <div class="main-container">

        <LoginForm/>


    </div>

</template>

<script lang="ts">
import LoginForm from '@/components/forms/loginForm.vue';


export default {
    name:'AuthLoginView',
    components:{
        LoginForm

    }
}

</script>

<style scoped></style>