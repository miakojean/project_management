<template>
    <section class="flex flex-col min-h-screen gap-8">
        <div class="grid grid-cols-2 gap-6 flex-1">
            <!-- Colonne gauche fixe -->
            <div class="sticky top-4 self-start">
                <cardsaffairs
                    v-if="doc && doc.titre"
                    :title="doc.titre"
                    :description="doc.description || 'Aucune description'"
                    :status="getStatus(doc.statut)"
                    :date="formatDate(doc.date_creation || doc.created_at)"
                    :clientName="doc.client_nom || 'Client non spécifié'"
                    :progress="calculateProgress(doc.statut)"
                    @view="handleView"
                    @edit="handleEdit"
                    @action="handleAction"
                />
                <div v-else class="p-6 bg-gray-50 rounded-lg border border-dashed border-gray-300 text-center">
                    <p class="text-gray-500">Aucun dossier sélectionné</p>
                    <p class="text-sm text-gray-400 mt-2">Sélectionnez un dossier pour voir les détails</p>
                </div>
            </div>

            <!-- Colonne droite défilante -->
            <div class="sticky top-4 self-start">
                <uploadFileButton />
            </div>
        </div>

        <div class="">
            <documentList/>
        </div>
    </section>
</template>

<script>
import cardsaffairs from '../cards/cardsaffairs.vue';
import documentList from '../items/documentList.vue';
import uploadFileButton from '../button/uploadFileButton.vue';
import { useDossierStore } from '@/stores/dossierStore';
import { onMounted, watch, ref, computed } from 'vue';

export default {
    components: {
        cardsaffairs,
        documentList,
        uploadFileButton
    },
    setup(){
        const doc = ref({})
        const dossierStore = useDossierStore();

        // Méthodes utilitaires
        const getStatus = (status) => {
            const statusMap = {
                'NOUVEAU': 'active',
                'EN_COURS': 'active',
                'EN_ATTENTE': 'pending',
                'TERMINE': 'completed',
                'CLOS': 'archived',
                'ANNULE': 'cancelled'
            };
            return statusMap[status] || 'pending';
        };

        const formatDate = (dateString) => {
            if (!dateString) return 'Date inconnue';
            const date = new Date(dateString);
            return date.toLocaleDateString('fr-FR', {
                day: 'numeric',
                month: 'short',
                year: 'numeric'
            });
        };

        const calculateProgress = (status) => {
            const progressMap = {
                'NOUVEAU': 10,
                'EN_COURS': 50,
                'EN_ATTENTE': 30,
                'TERMINE': 100,
                'CLOS': 100,
                'ANNULE': 0
            };
            return progressMap[status] || 25;
        };

        // Surveillance du currentDossier dans le store
        watch(
            () => dossierStore.currentDossier,
            (newDossier) => {
                console.log('🔄 Dossier mis à jour:', newDossier);
                if (newDossier) {
                    doc.value = newDossier;
                    console.log('📄 Document mis à jour:', doc.value);
                } else {
                    doc.value = {};
                }
            },
            { immediate: true } // Exécute immédiatement au montage
        );

        onMounted(() => {
            // Cette partie peut être optionnelle si watch s'exécute immédiatement
            console.log('🏁 Composant monté');
            console.log('📁 Dossier store:', dossierStore.currentDossier);
        });

        const handleView = () => {
            console.log('Voir le dossier:', doc.value);
        };

        const handleEdit = () => {
            console.log('Éditer le dossier:', doc.value);
        };

        const handleAction = (action) => {
            console.log('Action:', action, 'sur:', doc.value);
        };

        return {
            doc,
            dossierStore,
            getStatus,
            formatDate,
            calculateProgress,
            handleView,
            handleEdit,
            handleAction
        };
    }
}
</script>