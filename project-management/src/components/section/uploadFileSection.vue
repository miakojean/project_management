<template>
    <section>
        <simpleNavbar></simpleNavbar>
        <fileForm/>
    </section>
</template>

<script>
import fileForm from '../forms/fileForm.vue';
import simpleNavbar from '../navigation/simpleNavbar.vue';
export default {
    components:{
        fileForm,
        simpleNavbar
    }
}
</script>

<style>

</style>