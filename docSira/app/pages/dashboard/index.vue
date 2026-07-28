<template>
    <div class="main-layout">
        <navbar/>
        <sidebar/>
        <dashboarSection/>
    </div>
</template>

<script langs="ts">
import navbar from '../../components/navbar/navbar.vue'
import dashboarSection from '../../components/sections/dashboard-section/dashboardSection.vue'
import sidebar from '../../components/navbar/sidebar.vue'
export default {

    components:{
        dashboarSection,
        sidebar,
        navbar
    }

}
</script>

<style scoped>

</style>