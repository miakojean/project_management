<template>
    <section class="w-full flex flex-col gap-2">
        <div class="layout__header">
            <h2>Bienvenu(e)</h2>
        </div>
        <div class="section-cards">
            <h3>
                La statistique des clients ce mois-ci
            </h3>
            <chartSection/>
        </div>
        <div class="section-cards">
            <h3>
                Les derniers dossiers ajoutés
            </h3>
            
        </div>
    </section>
</template>

<script>   
import chartSection from './chartSection.vue';
import { useCustomerStore } from '@/stores/custumerStore';
import { useDossierStore } from '@/stores/dossierStore';
export default {
    name: 'IndexDashboardSection',

    components:{
        chartSection,
    },

    setup(){

        const customerStore = useCustomerStore();
        const dossierStore = useDossierStore();

        return{
            customerStore,
            dossierStore
        }
        
    }
}
</script>
<style scoped>
.layout__header {
    padding: 20px;
    border-bottom: 1px solid #e0e0e0;
    background-color: #f9f9f9;
}

.layout__header h2 {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    color: #333333;
}

.section-cards {
    padding: 20px;
}

.section-cards h3 {
    margin: 0 0 10px 0;
    font-size: 20px;
    font-weight: 500;
    color: #555555;
}
</style>