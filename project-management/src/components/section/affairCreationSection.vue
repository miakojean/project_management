<template>
    <main class="center__flex__column">
        <affairForm/>
    </main>
</template>

<script>
import affairForm from '../forms/affairForm.vue';
export default {
    components:{
        affairForm
    }
}
</script>

<style scoped>

main{
    min-height: 100vh;
}

</style>