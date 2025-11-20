<template>
    <section class="w-full flex flex-col gap-8">
        <h2>Dossier récents</h2>

        <div class="recents__affairs">
            <cardAffairsFolder :avancement="50"/>
            <cardAffairsFolder/>
            <cardAffairsFolder/>
            <cardAffairsFolder/>
            <cardAffairsFolder/>
        </div>
    </section>
</template>

<script>
import cardAffairsFolder from '../cards/cardAffairsFolder.vue';
export default {

    components:{
        cardAffairsFolder,
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