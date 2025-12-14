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
        
        <!-- SECTION DES DOCUMENTS -->
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
        
        <!-- ÉTAT VIDE - PREND TOUTE LA LARGEUR -->
        <div v-else class="w-full">
            <emptyCards />
        </div>

        <!-- SECTION DES COMMENTAIRES -->
        <div class="w-full">
            <h3 class="text-xl font-semibold text-gray-800 mb-4">Commentaires</h3>
            
            <!-- Zone de création de commentaire -->
            <commentInput
                v-if="doc.id"
                :placeholder="`Ajouter un commentaire sur le dossier`"
                buttonText="Commenter"
                :required="true"
                @submit="handleCreateComment"
                :disabled="isSubmittingComment"
            />
            
            <!-- Liste des commentaires -->
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
            />
            
            <!-- Modale de réponse -->
            <div v-if="isReplyingTo" class="mt-4 ml-12">
                <commentInput
                    :placeholder="`Répondre à ${replyingToAuthor}...`"
                    buttonText="Répondre"
                    @submit="handleCreateReponse"
                    @cancel="cancelReply"
                    :disabled="isSubmittingReponse"
                />
            </div>
        </div>
        
        <!-- MODALE DE SUPPRESSION DOCUMENT -->
        <deleteModale
            v-if="isDeleteModaleOpen"
            :isVisible="isDeleteModaleOpen"
            :message="deleteModalMessage"
            @confirm="handleDelete"
            @cancel="isDeleteModaleOpen = false"
        />
        
        <!-- MODALE DE SUPPRESSION COMMENTAIRE -->
        <deleteModale
            v-if="isDeleteCommentModalOpen"
            :isVisible="isDeleteCommentModalOpen"
            :message="deleteCommentModalMessage"
            @confirm="confirmDeleteComment"
            @cancel="isDeleteCommentModalOpen = false"
        />
        
        <!-- NOTIFICATION POPUP -->
        <notificationPopup
            v-if="notificationPopup.isVisible"
            :isVisible="notificationPopup.isVisible"
            :message="notificationPopup.message"
            :type="notificationPopup.type"
            @close="notificationPopup.isVisible = false"
        />
    </section>
</template>

<script>
import cardsaffairs from '../cards/cardsaffairs.vue';
import uploadFileButton from '../button/uploadFileButton.vue';
import emptyCards from '../cards/emptyCards.vue';
import { onMounted, watch, ref, computed, nextTick } from 'vue';
import fileCards from '../cards/fileCards.vue';
import deleteModale from '../modales/deleteModale.vue';
import notificationPopup from '../tools/notificationPopup.vue';
import commentInput from '../input/commentInput.vue';
import commentSection from './commentSection.vue';

// Store 
import { useDossierStore } from '@/stores/dossierStore';
import { useDocumentStore } from '@/stores/documentsStore';
import { useAuthStore } from '@/stores/auth';

export default {
    components: {
        cardsaffairs,
        uploadFileButton,
        fileCards,
        deleteModale,
        notificationPopup,
        emptyCards,
        commentInput,
        commentSection
    },
    setup(){
        const doc = ref({})
        const dossierStore = useDossierStore();
        const documentStore = useDocumentStore();
        const authStore = useAuthStore(); // Store d'authentification
        
        // État pour les commentaires
        const commentaires = ref([]);
        const commentairesLoading = ref(false);
        const isSubmittingComment = ref(false);
        const isSubmittingReponse = ref(false);
        
        // Gestion de la réponse à un commentaire
        const isReplyingTo = ref(false);
        const replyingToCommentId = ref(null);
        const replyingToAuthor = ref('');
        
        // Gestion de la suppression de commentaire
        const isDeleteCommentModalOpen = ref(false);
        const commentToDelete = ref(null);
        
        // États existants
        const isDeleteModaleOpen = ref(false);
        const documentToDelete = ref(null);
        
        const notificationPopup = ref({
            isVisible: false,
            message: '',
            type: 'success',
            duration: 5000
        });

        // Computed
        const currentUserId = computed(() => {
            return authStore.user?.id || null;
        });
        
        const hasDocuments = computed(() => {
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
            const date = new Date(dateString);
            return date.toLocaleDateString('fr-FR', {
                day: 'numeric',
                month: 'short',
                year: 'numeric'
            });
        };

        // Méthodes pour les commentaires
        const loadCommentaires = async () => {
            if (!doc.value.id) return;
            
            commentairesLoading.value = true;
            try {
                // Charger les commentaires du dossier
                await dossierStore.fetchCommentairesByDossier(doc.value.id);
                
                // Mettre à jour la liste locale
                commentaires.value = dossierStore.getCommentairesByDossier(doc.value.id);
                
                // Pour chaque commentaire, charger ses réponses
                for (const commentaire of commentaires.value) {
                    await dossierStore.fetchReponsesByCommentaire(commentaire.id);
                    // Mettre à jour le commentaire avec ses réponses
                    commentaire.reponses = dossierStore.getReponsesByCommentaire(commentaire.id);
                }

                console.log("Commentaires chargés correctement", commentaires.value)
                
            } catch (error) {
                showNotification('Erreur lors du chargement des commentaires', 'error');
                console.error('Erreur loadCommentaires:', error);
            } finally {
                commentairesLoading.value = false;
            }
        };

        const handleCreateComment = async (message) => {
            if (!doc.value.id || !message.trim()) return;
            
            isSubmittingComment.value = true;
            try {
                const newComment = await dossierStore.createCommentaire(doc.value.id, message);
                
                // Ajouter le nouveau commentaire à la liste
                commentaires.value.unshift({
                    ...newComment,
                    reponses: []
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
            isReplyingTo.value = true;
            replyingToCommentId.value = comment.id;
            replyingToAuthor.value = comment.auteur_nom || comment.auteur?.nom_complet || 'l\'utilisateur';
            
            // Scroller vers la zone de réponse
            nextTick(() => {
                document.querySelector('.comment__section textarea')?.focus();
            });
        };

        const handleCreateReponse = async (message) => {
            if (!replyingToCommentId.value || !message.trim()) return;
            
            isSubmittingReponse.value = true;
            try {
                const newReponse = await dossierStore.createReponse(replyingToCommentId.value, message);
                
                // Trouver le commentaire et ajouter la réponse
                const commentaireIndex = commentaires.value.findIndex(c => c.id === replyingToCommentId.value);
                if (commentaireIndex !== -1) {
                    if (!commentaires.value[commentaireIndex].reponses) {
                        commentaires.value[commentaireIndex].reponses = [];
                    }
                    commentaires.value[commentaireIndex].reponses.push(newReponse);
                }
                
                showNotification('Réponse ajoutée avec succès', 'success');
                cancelReply();
                
            } catch (error) {
                showNotification('Erreur lors de l\'ajout de la réponse', 'error');
                console.error('Erreur handleCreateReponse:', error);
            } finally {
                isSubmittingReponse.value = false;
            }
        };

        const handleEditComment = async (comment) => {
            const newMessage = prompt('Modifier le commentaire:', comment.message);
            
            if (newMessage !== null && newMessage.trim() !== comment.message) {
                try {
                    await dossierStore.updateCommentaire(comment.id, newMessage.trim());
                    
                    // Mettre à jour dans la liste
                    const commentaireIndex = commentaires.value.findIndex(c => c.id === comment.id);
                    if (commentaireIndex !== -1) {
                        commentaires.value[commentaireIndex].message = newMessage.trim();
                        commentaires.value[commentaireIndex].date_modification = new Date().toISOString();
                    }
                    
                    showNotification('Commentaire modifié avec succès', 'success');
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
                commentaires.value = commentaires.value.filter(c => c.id !== commentToDelete.value.id);
                
                showNotification('Commentaire supprimé avec succès', 'success');
                
            } catch (error) {
                showNotification('Erreur lors de la suppression du commentaire', 'error');
                console.error('Erreur confirmDeleteComment:', error);
            } finally {
                isDeleteCommentModalOpen.value = false;
                commentToDelete.value = null;
            }
        };

        const cancelReply = () => {
            isReplyingTo.value = false;
            replyingToCommentId.value = null;
            replyingToAuthor.value = '';
        };

        // Méthodes pour les documents (inchangées)
        const showDeleteDocumentModal = (document) => {
            documentToDelete.value = document;
            isDeleteModaleOpen.value = true;
        };

        const handleDelete = async () => {
            // ... code existant pour la suppression de documents ...
        };

        const showNotification = (message, type = 'success') => {
            notificationPopup.value = {
                isVisible: true,
                message,
                type
            };
            
            setTimeout(() => {
                notificationPopup.value.isVisible = false;
            }, 5000);
        };

        // Watchers
        watch(
            () => dossierStore.currentDossier,
            (newDossier) => {
                if (newDossier) {
                    doc.value = newDossier;
                    loadCommentaires(); // Charger les commentaires quand le dossier change
                } else {
                    doc.value = {};
                    commentaires.value = [];
                }
            },
            { immediate: true }
        );

        watch(
            () => doc.value.id,
            (newId) => {
                if (newId) {
                    loadCommentaires();
                }
            }
        );

        onMounted(async () => {
            if (dossierStore.currentDossier?.id) {
                doc.value = dossierStore.currentDossier;
                await loadCommentaires();
            }
        });

        return {
            doc,
            commentaires,
            commentairesLoading,
            currentUserId,
            isSubmittingComment,
            isSubmittingReponse,
            isReplyingTo,
            replyingToAuthor,
            isDeleteCommentModalOpen,
            hasDocuments,
            isDeleteModaleOpen,
            documentToDelete,
            deleteModalMessage,
            deleteCommentModalMessage,
            notificationPopup,
            
            // Méthodes
            getStatus,
            formatDate,
            handleCreateComment,
            handleReplyToComment,
            handleCreateReponse,
            handleEditComment,
            handleDeleteComment,
            confirmDeleteComment,
            cancelReply,
            showDeleteDocumentModal,
            handleDelete,
            handleView: () => console.log('Voir le dossier:', doc.value),
            handleEdit: () => console.log('Éditer le dossier:', doc.value),
            handleAction: (action) => console.log('Action:', action),
            handleDownload: async (docId, fileName) => {
                await documentStore.downloadDocuments(docId, fileName);
            }
        };
    }
}
</script>