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
                    :creatorName="doc.cree_par?.nom_complet || doc.cree_par?.username || 'Utilisateur'"
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
        
        <div v-if="hasDocuments" class="grid grid-cols-3 w-full gap-2">
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
        </div>
        
        <div v-else class="w-full">
            <emptyCards />
        </div>

        <div class="w-full">
            <h3 class="text-xl font-semibold text-gray-800 mb-4">Commentaires</h3>
            
            <commentInput
                v-if="doc.id"
                :placeholder="`Ajouter un commentaire sur le dossier`"
                buttonText="Commenter"
                :required="true"
                @submit="handleCreateComment"
                :disabled="isSubmittingComment"
            />
            
            <div v-if="commentairesLoading" class="flex justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
            
            <commentSection
                v-else
                :commentaires="commentaires"
                :currentUserId="currentUserId"
                :canReply="true"
                @edit="handleEditComment"
                @delete="handleDeleteComment"
                @reply="handleReplyToComment"
                @submitReply="handleCreateReponseFromChild"
            />
        </div>
        
        <deleteModale
            v-if="isDeleteModaleOpen"
            :isOpen="isDeleteModaleOpen"
            :message="deleteModalMessage"
            :itemToDelete="documentToDelete"  @confirm="handleDelete"
            @cancel="isDeleteModaleOpen = false"
            @close="isDeleteModaleOpen = false"
        />
        
        <deleteModale
            v-if="isDeleteCommentModalOpen"
            :isOpen="isDeleteCommentModalOpen"
            :message="deleteCommentModalMessage"
            @confirm="confirmDeleteComment"
            @cancel="isDeleteCommentModalOpen = false"
            @close="isDeleteCommentModalOpen=false"
        />
        
        <notificationPopup
            v-if="notificationPopupObject.isVisible"
            :isVisible="notificationPopupObject.isVisible"
            :message="notificationPopupObject.message"
            :type="notificationPopupObject.type"
            @close="notificationPopupObject.isVisible = false"
        />
    </section>
</template>

<script setup>
import cardsaffairs from '../cards/cardsaffairs.vue';
import uploadFileButton from '../button/uploadFileButton.vue';
import emptyCards from '../cards/emptyCards.vue';
import fileCards from '../cards/fileCards.vue';
import deleteModale from '../modales/deleteModale.vue';
import notificationPopup from '../tools/notificationPopup.vue';
import commentInput from '../input/commentInput.vue';
import commentSection from './commentSection.vue';

// Store 
import { useDossierStore } from '@/stores/dossierStore';
import { useDocumentStore } from '@/stores/documentsStore';
import { useAuthStore } from '@/stores/auth';
import { computed, ref, onMounted, nextTick, watch } from 'vue';

const dossierStore = useDossierStore();
const documentStore = useDocumentStore();
const authStore = useAuthStore();

// Utilisez directement le dossier du store (C'EST LA CLÉ !)
const doc = computed(() => dossierStore.currentDossier || {});

// État pour les commentaires
const commentaires = ref([]);
const commentairesLoading = ref(false);
const isSubmittingComment = ref(false);
const isSubmittingReponse = ref(false);

// Gestion de la réponse à un commentaire (désormais gérée inline dans le composant enfant)

// Gestion de la suppression de commentaire
const isDeleteCommentModalOpen = ref(false);
const commentToDelete = ref(null);

// États existants
const isDeleteModaleOpen = ref(false);
const documentToDelete = ref(null);

const notificationPopupObject = ref({
    isVisible: false,
    message: '',
    type: 'success',
    duration: 3000
});

// Computed
const currentUserId = computed(() => {
    return authStore.user?.id || null;
});

const hasDocuments = computed(() => {
    // Vérifie si doc.value est défini et si documents est un tableau non vide
    return doc.value?.documents?.length > 0;
});

const deleteModalMessage = computed(() => {
    if (documentToDelete.value) {
        return `Voulez-vous vraiment supprimer le document "${documentToDelete.value.titre}" ? Cette action est irréversible.`;
    }
    return "Voulez-vous supprimer ce document ?";
});

const deleteCommentModalMessage = computed(() => {
    if (commentToDelete.value) {
        return `Voulez-vous vraiment supprimer ce commentaire ? Cette action est irréversible.`;
    }
    return "Voulez-vous supprimer ce commentaire ?";
});

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
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('fr-FR', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });
    } catch (e) {
        console.error("Erreur de format de date:", e);
        return 'Date invalide';
    }
};

// Méthodes pour les commentaires
const loadCommentaires = async () => {
    console.log('loadCommentaires appelé, doc.value:', doc.value);
    if (!doc.value?.id) {
        console.log('Pas de dossier ID, vidage des commentaires');
        commentaires.value = []; // Vider si pas de dossier
        return;
    }
    
    console.log('Chargement des commentaires pour le dossier:', doc.value.id);
    commentairesLoading.value = true;
    try {
        // Utiliser la fonction utilitaire du store qui charge commentaires + réponses
        const result = await dossierStore.loadCommentairesForDossier(doc.value.id);
        // Résultat: { commentaires, reponses }
        console.log('loadCommentairesForDossier result:', result);

        // Associer les réponses à chaque commentaire pour l'affichage
        const commentairesAvecReponses = result.commentaires.map(c => ({
            ...c,
            reponses: result.reponses.filter(r => r.commentaire_id === c.id || r.commentaire === c.id)
        }));

        commentaires.value = commentairesAvecReponses;

        console.log("Commentaires chargés correctement", commentaires.value);
        
    } catch (error) {
        showNotification('Erreur lors du chargement des commentaires', 'error');
        console.error('Erreur loadCommentaires:', error);
    } finally {
        commentairesLoading.value = false;
    }
};

const handleCreateComment = async (message) => {
    if (!doc.value?.id || !message.trim()) return;
    
    isSubmittingComment.value = true;
    try {
        const newComment = await dossierStore.createCommentaire(doc.value.id, message);
        
        // Ajouter le nouveau commentaire à la liste (en haut)
        commentaires.value.unshift({
            ...newComment,
            reponses: [] // Assurez-vous qu'il y a une liste de réponses
        });
        
        showNotification('Commentaire ajouté avec succès', 'success');
        
    } catch (error) {
        showNotification('Erreur lors de l\'ajout du commentaire', 'error');
        console.error('Erreur handleCreateComment:', error);
    } finally {
        isSubmittingComment.value = false;
    }
};

const handleReplyToComment = (comment) => {
    // Backward-compatible handler called when user clicks 'Répondre' —
    // the child component now opens the inline reply input itself and focuses it.
    console.debug('handleReplyToComment called for comment', comment?.id);
};

// Handler for inline reply submission from the child component
const handleCreateReponseFromChild = async ({commentaireId, message}) => {
    if (!commentaireId || !message || !message.trim()) return;
    isSubmittingReponse.value = true;
    try {
        const newReponse = await dossierStore.createReponse(commentaireId, message);

        // Trouver le commentaire et ajouter la réponse localement
        const commentaireIndex = commentaires.value.findIndex(c => c.id === commentaireId);
        if (commentaireIndex !== -1) {
            if (!commentaires.value[commentaireIndex].reponses) {
                commentaires.value[commentaireIndex].reponses = [];
            }
            commentaires.value[commentaireIndex].reponses.push(newReponse);
        } else {
            console.warn(`Commentaire parent avec l'ID ${commentaireId} non trouvé pour ajouter la réponse.`);
        }

        showNotification('Réponse ajoutée avec succès', 'success');
    } catch (error) {
        const serverMsg = error?.response?.data?.error || error?.message || 'Erreur lors de l\'ajout de la réponse';
        showNotification(serverMsg, 'error');
        console.error('Erreur handleCreateReponseFromChild:', { error, serverMsg });
    } finally {
        isSubmittingReponse.value = false;
    }
};

// Old bottom reply handler removed; inline replies are handled by `handleCreateReponseFromChild` above.

const handleEditComment = async (comment) => {
    const newMessage = prompt('Modifier le commentaire:', comment.message);
    
    if (newMessage !== null && newMessage.trim() !== comment.message) {
        try {
            await dossierStore.updateCommentaire(comment.id, newMessage.trim());
            
            // Mettre à jour dans la liste
            // Trouver dans les commentaires de premier niveau
            let updated = false;
            const commentaireIndex = commentaires.value.findIndex(c => c.id === comment.id);
            if (commentaireIndex !== -1) {
                commentaires.value[commentaireIndex].message = newMessage.trim();
                commentaires.value[commentaireIndex].date_modification = new Date().toISOString();
                updated = true;
            }

            // Si ce n'est pas un commentaire de premier niveau, chercher dans les réponses
            if (!updated) {
                for (const c of commentaires.value) {
                    const reponseIndex = c.reponses?.findIndex(r => r.id === comment.id);
                    if (reponseIndex !== -1) {
                        c.reponses[reponseIndex].message = newMessage.trim();
                        c.reponses[reponseIndex].date_modification = new Date().toISOString();
                        updated = true;
                        break;
                    }
                }
            }

            if (updated) {
                showNotification('Commentaire modifié avec succès', 'success');
            }
            
        } catch (error) {
            showNotification('Erreur lors de la modification du commentaire', 'error');
            console.error('Erreur handleEditComment:', error);
        }
    }
};

const handleDeleteComment = (comment) => {
    commentToDelete.value = comment;
    isDeleteCommentModalOpen.value = true;
};

const confirmDeleteComment = async () => {
    if (!commentToDelete.value) return;
    
    try {
        await dossierStore.deleteCommentaire(commentToDelete.value.id);
        
        // Retirer de la liste
        let foundAndRemoved = false;
        // 1. Essayer de retirer des commentaires de premier niveau
        const initialLength = commentaires.value.length;
        commentaires.value = commentaires.value.filter(c => c.id !== commentToDelete.value.id);
        if (commentaires.value.length < initialLength) {
            foundAndRemoved = true;
        }

        // 2. Si non trouvé, essayer de retirer des réponses
        if (!foundAndRemoved) {
            for (const c of commentaires.value) {
                if (c.reponses) {
                    const initialReponseLength = c.reponses.length;
                    c.reponses = c.reponses.filter(r => r.id !== commentToDelete.value.id);
                    if (c.reponses.length < initialReponseLength) {
                        foundAndRemoved = true;
                        break;
                    }
                }
            }
        }
        
        showNotification('Commentaire supprimé avec succès', 'success');
        
    } catch (error) {
        showNotification('Erreur lors de la suppression du commentaire', 'error');
        console.error('Erreur confirmDeleteComment:', error);
    } finally {
        isDeleteCommentModalOpen.value = false;
        commentToDelete.value = null;
    }
};

// cancelReply removed — inline reply UI is handled by the child component

// Méthodes pour les documents
const showDeleteDocumentModal = (document) => {
    // Debug: Vérifiez la structure de l'objet document
    console.log('Document à supprimer - structure complète:', document);
    console.log('ID du document:', document.id);
    
    // Vérifiez que l'ID existe
    if (!document || !document.id) {
        console.error('Document invalide - pas d\'ID:', document);
        showNotification('Erreur: Document invalide', 'error');
        return;
    }
    
    documentToDelete.value = document;
    isDeleteModaleOpen.value = true;
};

const handleDelete = async () => {
    // 1. Utilisez .value pour vérifier l'ID
    if (!documentToDelete.value || !documentToDelete.value.id) {
        console.error('Aucun document sélectionné ou ID manquant');
        return;
    };
    
    try {
        // 2. ERREUR CORRIGÉE : On passe documentToDelete.value (le contenu)
        await documentStore.deleteDocument(documentToDelete.value);
        
        // 3. Mise à jour de l'interface
        if (doc.value.documents) {
            const updatedDocuments = doc.value.documents.filter(d => d.id !== documentToDelete.value.id);
            
            dossierStore.currentDossier = {
                ...dossierStore.currentDossier,
                documents: updatedDocuments
            };
        }
        
        showNotification('Document supprimé avec succès', 'success');
        
    } catch (error) {
        const errMsg = error?.message || 'Erreur lors de la suppression du document';
        showNotification(`Erreur : ${errMsg}`, 'error');
    } finally {
        isDeleteModaleOpen.value = false;
        documentToDelete.value = null;
    }
};

const showNotification = (message, type = 'success') => {
    notificationPopupObject.value = {
        isVisible: true,
        message,
        type
    };
    
    // Correction: utilise notificationPopupObject.value (max 3000ms)
    setTimeout(() => {
        notificationPopupObject.value.isVisible = false;
    }, 3000);
};

// Watcher pour recharger les commentaires quand le dossier change
watch(
    () => doc.value?.id,
    (newId) => {
        console.log('Watcher dossier ID déclenché, newId:', newId);
        if (newId) {
            console.log('Dossier changé, ID:', newId); // DEBUG
            loadCommentaires();
        } else {
            commentaires.value = [];
        }
    },
    { immediate: true }
);

// Initialisation
onMounted(() => {
    console.log('Composant customerSectionFolder monté, dossier actuel:', doc.value); // DEBUG
    console.log('currentDossier du store:', dossierStore.currentDossier); // DEBUG
});

// Méthodes pour le template
const handleView = () => {
    console.log('Voir le dossier:', doc.value);
    // Logique de navigation/affichage de vue détaillée
};

const handleEdit = () => {
    console.log('Éditer le dossier:', doc.value);
    // Logique d'ouverture de modale d'édition
};

const handleAction = (action) => {
    console.log('Action:', action);
    // Logique pour les actions spécifiques du dossier (e.g. "Clore", "Annuler")
};

const handleDownload = async (docId, fileName) => {
    try {
        // Passer le filename explicitement en troisième argument
        const result = await documentStore.downloadDocuments(docId, {}, fileName);
        showNotification(`Téléchargement lancé${result?.filename ? `: ${result.filename}` : ''}`, 'success');
    } catch (error) {
        showNotification('Erreur lors du téléchargement', 'error');
        console.error('Erreur handleDownload:', error);
    }
};
</script>