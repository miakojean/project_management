<template>
    <section class=" flex items-center gap-4 flex-col">
        
        <h3 class="w-full align-text-left">Détail du dossier ABC</h3>

        <div class="grid grid-cols-2">
            
            <cardsaffairs
                title="Dossier Marketing Q4"
                description="Campagne publicitaire pour le lancement du nouveau produit"
                status="active"
                date="20 Jan 2024"
                clientName="Entreprise ABC"
                :progress="80"
                @view="handleView"
                @edit="handleEdit"
                @action="handleAction"
            />

            <documentList/>
        </div>
    </section>
</template>

<script>
import cardsaffairs from '../cards/cardsaffairs.vue';
import documentList from '../items/documentList.vue';
export default {

    components:{
        cardsaffairs,
        documentList
    }

}
</script>

<style scoped>

</style>