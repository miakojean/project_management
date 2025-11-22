<template>
    <section class="w-full flex flex-col gap-8">
        <h2>Dossier récents</h2>

        <div class="recents__affairs">
            <cardAffairsFolder :avancement="50" @click="goToFolderDetail"/>
            <cardAffairsFolder @click="goToFolderDetail"/>
            <cardAffairsFolder @click="goToFolderDetail"/>
            <cardAffairsFolder @click="goToFolderDetail"/>
            <cardAffairsFolder @click="goToFolderDetail"/>
        </div>
    </section>
</template>

<script>
import cardAffairsFolder from '../cards/cardAffairsFolder.vue';
import { useRouter } from 'vue-router';
export default {

    components:{
        cardAffairsFolder,
    },

    setup(){
        const router = useRouter();

        const goToFolderDetail = () => {
            router.push('/dashboard/customer/affairs')
        }

        return{
            router,
            goToFolderDetail
        }
    }
}
</script>

<style scoped>
.recents__affairs{
    display:grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1rem;
}

section h2{
    font-size: 2rem;
    font-weight:500;
}
</style>