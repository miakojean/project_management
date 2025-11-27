<template>
    <section class="w-full flex flex-col gap-8">
        <h2>Dossier récents</h2>

        <!-- État de chargement -->
        <div v-if="dossierStore.loading" class="loading">
            Chargement des dossiers...
        </div>

        <!-- État d'erreur -->
        <div v-else-if="dossierStore.error" class="error">
            Erreur: {{ dossierStore.error }}
        </div>

        <!-- Données chargées -->
        <div v-else class="recents__affairs">
            <!-- Affichez chaque dossier -->
            <cardAffairsFolder 
                v-for="dossier in recentDossiers" 
                :key="dossier.id"
                :titre="dossier.titre" 
                :reference="dossier.reference_dossier"
                :clientNom="dossier.client_nom"
                :statut="dossier.statut"
                :dateOuverture="dossier.date_creation_formatee"
                :dossier="dossier"
                @click="goToFolderDetail(dossier.id)"
            />
            
            <!-- Message si aucun dossier -->
            <div v-if="recentDossiers.length === 0" class="no-data">
                Aucun dossier trouvé
            </div>
        </div>
    </section>
</template>

<script>
import cardAffairsFolder from '../cards/cardAffairsFolder.vue';
import { useDossierStore } from '@/stores/dossierStore';
import { onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

export default {
    components: {
        cardAffairsFolder,
    },

    setup() {
        const router = useRouter();
        const dossierStore = useDossierStore();

        // Computed pour les dossiers récents (par exemple les 6 premiers)
        const recentDossiers = computed(() => {
            return dossierStore.dossiers.slice(0, 6);
        });

        const goToFolderDetail = (dossierId) => {
            router.push(`/dashboard/customer/affairs/`);
        }

        onMounted(async () => {
            console.log('📂 Chargement des dossiers pour affairIndexSection...');
            
            // Si les dossiers ne sont pas déjà chargés par la sidebar, on les charge
            if (dossierStore.dossiers.length === 0) {
                await dossierStore.fetchDossiers();
            }
            
            console.log('✅ Dossiers disponibles:', dossierStore.dossiers.length);
            console.log('structure d\'un dossier', dossierStore.dossiers[0])
        });

        return {
            router,
            recentDossiers,
            goToFolderDetail,
            dossierStore
        }
    }
}
</script>

<style scoped>
.recents__affairs{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1rem;
}

section h2{
    font-size: 2rem;
    font-weight: 500;
}

.loading, .error, .no-data {
    padding: 2rem;
    text-align: center;
    background: #f5f5f5;
    border-radius: 8px;
}

.error {
    color: #e53e3e;
    background: #fed7d7;
}
</style>