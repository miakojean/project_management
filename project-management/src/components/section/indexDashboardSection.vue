<template>
    <section class="w-full flex flex-col gap-2">
        <div class="layout__header flex flex-col items-center justify-center gap-4 rounded-2xl">
            <div class="cta-content flex flex-col gap-4">
                <div class="cta-text">
                    <h2>Bienvenu(e) sur ADN JurisTrack</h2>
                    <p>
                        Une solution pour la gestion et le suivi de vos dossiers juridiques mise en place par ADN Consulting SAS.
                    </p>
                </div>
                <div class="cards grid-rows-3 grid-cols-2 gap-4 mb-4 flex">
                    <FeaturesCards 
                        title="Gérer vos dossiers"
                        description="Créez, suivez et organisez tous vos dossiers juridiques en un seul endroit."
                    />
                    <FeaturesCards 
                        title="Clients" 
                        description="Sachez d'où viennent vos clients et gérez leurs informations efficacement.">
                        <template #icon>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z" />
                            </svg>
                        </template>
                    </FeaturesCards>
                    <FeaturesCards 
                        title="Base de données" 
                        description="Conservez toutes les informations juridiques importantes dans une base de données sécurisée.">
                        <template #icon>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125" />
                            </svg>
                        </template>
                    </FeaturesCards>
                </div>
                <div class="cta-actions w-1/2 flex gap-4">
                    <secondButton @click="goToClients" label="voir les dossiers"></secondButton>
                    <mainButton @click="goToNewCustomer" label="Ajouter un client"></mainButton>
                </div>
            </div>
        </div>
        <div class="section-cards">
            <h3>
                Vos statistiques pour ce mois
            </h3>
            <chartSection/>
        </div>
    </section>
</template>

<script>   
import chartSection from './chartSection.vue';
import mainButton from '../button/mainButton.vue';
import secondButton from '../button/secondButton.vue';
import FeaturesCards from '../cards/featuresCards.vue';
import { useCustomerStore } from '@/stores/custumerStore';
import { useDossierStore } from '@/stores/dossierStore';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
    name: 'IndexDashboardSection',

    components:{
        FeaturesCards,
        chartSection,
        mainButton,
        secondButton
    },

    setup(){

        const customerStore = useCustomerStore();
        const dossierStore = useDossierStore();
        const router = useRouter();

        const goToNewCustomer = () => {
            router.push('/customer');
        };

        const goToClients = () => {
            router.push('/dashboard/customer');
        };

        onMounted(() => {
            // Pré-charger éventuellement des stats / clients
            if (!customerStore.customers.length) customerStore.fetchCustomers?.();
            if (!dossierStore.dossiers?.length) dossierStore.fetchDossiers?.();
        });

        return{
            customerStore,
            dossierStore,
            goToNewCustomer,
            goToClients
        }
        
    }
}
</script>
<style scoped>
.layout__header {
    padding: 20px;
    border-bottom: 1px solid #e0e0e0;
    background-color: #ffffff;
    padding: 1rem;
    min-height: 450px;
}

.layout__header h2 {
    margin: 0;
    font-size: 32px;
    font-weight: 700;
    color: #333333;
    line-height: 1.5;
}

.layout__header p {
    margin: 0;
    font-size: 22px;
    font-weight: 400;
    color: #8a8a8a;
    line-height: 1.5
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

svg {
  width: 32px;
  height: 32px;
  stroke: white;
  stroke-width: 1.5;
}
</style>