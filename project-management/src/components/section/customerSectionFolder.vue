<template>
    <section class="flex flex-col min-h-screen gap-8">
        <div class="grid grid-cols-2 gap-6 flex-1">
            <div class="sticky top-4 self-start">
                <cardsaffairs
                    v-if="doc && doc.titre"
                    :title="doc.titre"
                    :description="doc.description || 'Aucune description'"
                    :status="getStatus(doc.statut)"
                    :date="formatDate(doc.date_creation || doc.created_at)"
                    :clientName="doc.client_details?.nom_complet || 'Client non spécifié'"
                    :progress="doc.taux_avancement"
                    @view="handleView"
                    @edit="handleEdit"
                    @action="handleAction"
                />
                <div v-else class="p-6 bg-gray-50 rounded-lg border border-dashed border-gray-300 text-center">
                    <p class="text-gray-500">Aucun dossier sélectionné</p>
                    <p class="text-sm text-gray-400 mt-2">Sélectionnez un dossier pour voir les détails</p>
                </div>
            </div>

            <div class="sticky top-4 self-start">
                <uploadFileButton />
            </div>
        </div>

        <div class=" grid grid-cols-3 w-full gap-2">
            <fileCards v-for="document in doc.documents"
                :key="document.id"
                :title="document.titre"
                :size="document.taille_lisible"
                :status="document.statut"
                :documentType="document.extension"
                :description="document.description"
                @download="handleDownload(document.id, document.titre)"
                @delete="showDeleteDocumentModal(document)" 
            />

            <emptyCards/>
        </div>

        <deleteModale 
            :is-open="isDeleteModaleOpen"
            :item-to-delete="documentToDelete"
            :message="deleteModalMessage"
            @close="() => isDeleteModaleOpen = false"
            @confirm="handleDelete"
        />

        <notificationPopup 
            :visible="notificationPopup.isVisible"
            :message="notificationPopup.message"
            :duration="notificationPopup.duration"
        />

    </section>
</template>

<script>
import cardsaffairs from '../cards/cardsaffairs.vue';
import documentList from '../items/documentList.vue';
import uploadFileButton from '../button/uploadFileButton.vue';
import emptyCards from '../cards/emptyCards.vue';
import { onMounted, watch, ref, computed } from 'vue';
import fileCards from '../cards/fileCards.vue';
import deleteModale from '../modales/deleteModale.vue';
import notificationPopup from '../tools/notificationPopup.vue';

// Store 
import { useDossierStore } from '@/stores/dossierStore';
import { useDocumentStore } from '@/stores/documentsStore';

export default {
    components: {
        cardsaffairs,
        documentList,
        uploadFileButton,
        fileCards,
        deleteModale,
        notificationPopup,
        emptyCards
    },
    setup(){
        const doc = ref({})
        const dossierStore = useDossierStore();
        const documentStore = useDocumentStore();
        const documents = ref({}); // Note: Ceci est redondant avec doc.value.documents, mais conservé.

        // =================================================================
        // ✅ CORRECTION 1 : GESTION DE LA SUPPRESSION (État dédié)
        // =================================================================
        const isDeleteModaleOpen = ref(false);
        const documentToDelete = ref(null); // Référence spécifique au document à supprimer

        const deleteModalMessage = computed(() => {
            if (documentToDelete.value) {
                return `Voulez-vous vraiment supprimer le document "${documentToDelete.value.titre}" ? Cette action est irréversible.`;
            }
            return "Voulez-vous supprimer ce document ?";
        });

        // =================================================================
        // ✅ CORRECTION 2 : GESTION DES NOTIFICATIONS (Initialisation)
        // =================================================================
        const notificationPopup = ref({
            isVisible: false,
            message: '',
            type: 'success', // 'success' ou 'error'
            duration:5000
        });


        // Méthodes utilitaires (Inchangées)
        const getStatus = (status) => {
             // ... (votre implémentation)
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
            // ... (votre implémentation)
            if (!dateString) return 'Date inconnue';
            const date = new Date(dateString);
            return date.toLocaleDateString('fr-FR', {
                day: 'numeric',
                month: 'short',
                year: 'numeric'
            });
        };

        const calculateProgress = (status) => {
            // ... (votre implémentation)
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

        // Ouverture de la modale de suppression
        const showDeleteDocumentModal = (document) => { // Renommé pour plus de clarté
            documentToDelete.value = document; // Stocke le document à supprimer
            isDeleteModaleOpen.value = true;
            console.log('Document à supprimer', documentToDelete.value);
            console.log('ID du document au clic:', documentToDelete.value?.id);
        }

        const handleView = () => {
            console.log('Voir le dossier:', doc.value);
        };

        const handleEdit = () => {
            console.log('Éditer le dossier:', doc.value);
        };

        const handleAction = (action) => {
            console.log('Action:', action, 'sur:', doc.value);
        };

        const handleDownload = async (docId, fileName) => {
            await documentStore.downloadDocuments(docId, fileName)
            console.log('Vous voulez télécharger', docId)
        };

        // =================================================================
        // ✅ CORRECTION 3 : LOGIQUE DE SUPPRESSION COMPLÈTE
        // =================================================================
        const handleDelete = async () => {
            const document = documentToDelete.value; 
            
            // VÉRIFICATION INITIALE
            if (!document || !document.id) {
                console.error("Document non valide pour la suppression");
                isDeleteModaleOpen.value = false;
                documentToDelete.value = null;
                return;
            }

            try {
                // 1. APPEL AU STORE
                await documentStore.deleteDocument(document); 

                // 2. MISE À JOUR LOCALE
                if (doc.value.documents) {
                    doc.value.documents = doc.value.documents.filter(d => d.id !== document.id);
                }

                // 3. NOTIFICATION DE SUCCÈS
                notificationPopup.value = {
                    isVisible: true,
                    message: `Le document "${document.titre}" a été supprimé avec succès.`,
                    type: "success"
                };

            } catch (error) {
                // 4. NOTIFICATION D'ERREUR
                console.error("Erreur lors de la suppression du document:", error);
                
                const errorMessage = error.response?.data?.error 
                    || error.message 
                    || "Une erreur est survenue lors de la suppression du document.";

                notificationPopup.value = {
                    isVisible: true,
                    message: errorMessage,
                    type: "error"
                };
                
            } finally {
                // 5. NETTOYAGE (sans afficher de notification)
                isDeleteModaleOpen.value = false;
                documentToDelete.value = null;
                
                // 6. FERMETURE AUTOMATIQUE DE LA NOTIFICATION APRÈS 5 SECONDES
                setTimeout(() => {
                    notificationPopup.value.isVisible = false;
                }, 5000);
            }
        }

        // Surveillance du currentDossier dans le store (Inchangée)
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
            { immediate: true }
        );

        onMounted(async() => {
            console.log('📁 Dossier store:', dossierStore.currentDossier);

            if(dossierStore.currentDossier && dossierStore.currentDossier.id){
                doc.value = dossierStore.currentDossier;
                try {
                    const dossierData = await dossierStore.fetchDossierById(doc.value.id);
                    documents.value = dossierData.documents || dossierData.files || [];
                    console.log('📁 Documents chargés au montage:', documents.value);
                } catch (error) {
                    console.error('Erreur lors du chargement des documents:', error);
                    documents.value = [];
                }
            }
        });

        return {
            doc,
            documents,
            documentStore,
            dossierStore,
            getStatus,
            formatDate,
            calculateProgress,
            handleView,
            handleEdit,
            handleAction,
            handleDownload,
            
            // Suppression
            isDeleteModaleOpen,
            documentToDelete, // Exporté pour la gestion des données de la modale (optionnel mais utile)
            deleteModalMessage, // Message calculé
            showDeleteDocumentModal, // Renommé
            handleDelete,
            
            // ✅ CORRECTION 4 : Notification exportée
            notificationPopup 
        };
    }
}
</script>