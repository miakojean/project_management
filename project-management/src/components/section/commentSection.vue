<template>
    <div class="comments-container">
        <div class="comments-header">
            <h4 class="header-title">Commentaires</h4>
            <span class="comment-count-badge">
                {{ totalCommentaires }}
            </span>
        </div>

        <div v-if="commentaires.length === 0 && !loading" class="empty-state">
            <div class="empty-icon-wrapper">
                <svg xmlns="http://www.w3.org/2000/svg" class="empty-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
            </div>
            <p class="empty-title">Aucun commentaire pour le moment</p>
            <p class="empty-text">Soyez le premier à partager votre avis sur ce dossier.</p>
        </div>

        <div v-if="loading" class="loading-state">
            <div class="loader">
                <div class="loader-track"></div>
                <div class="loader-spinner"></div>
            </div>
        </div>

        <div v-else class="comments-list">
            <div 
                v-for="commentaire in commentaires" 
                :key="commentaire.id"
                class="comment-group"
                :data-comment-id="commentaire.id"
            >
                <div v-if="commentaire.reponses && commentaire.reponses.length > 0" 
                    class="reply-line"></div>

                <div class="comment-wrapper">
                    <div class="comment-avatar-container">
                        <div class="comment-avatar">
                            {{ getInitials(getAuthorName(commentaire)) }}
                        </div>
                    </div>

                    <div class="comment-content-area">
                        <div class="comment-card">
                            <div class="comment-meta">
                                <div class="meta-author-info">
                                    <span class="author-name">{{ getAuthorName(commentaire) }}</span>
                                    <span v-if="commentaire.auteur_id === currentUserId" class="author-tag">
                                        Vous
                                    </span>
                                </div>
                                <span class="meta-date">{{ formatDate(commentaire.date_creation) }}</span>
                            </div>
                            
                            <p class="comment-message">{{ commentaire.message }}</p>

                            <div class="comment-actions">
                                <button v-if="canReply" @click="handleReply(commentaire)" class="action-button reply-button">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="action-icon" viewBox="0 0 20 20" fill="currentColor">
                                        <path fill-rule="evenodd" d="M7.707 3.293a1 1 0 010 1.414L5.414 7H11a7 7 0 017 7v2a1 1 0 11-2 0v-2a5 5 0 00-5-5H5.414l2.293 2.293a1 1 0 11-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                                    </svg>
                                    Répondre
                                </button>
                                
                                <div v-if="canEdit(commentaire) || canDelete(commentaire)" class="action-controls">
                                    <button v-if="canEdit(commentaire)" @click="handleEdit(commentaire)" class="action-controls-button edit-button">Modifier</button>
                                    <button v-if="canDelete(commentaire)" @click="handleDelete(commentaire)" class="action-controls-button delete-button">Supprimer</button>
                                </div>
                            </div>
                        </div>

                        <!-- Inline reply input for this commentaire -->
                        <div v-if="replyingToId === commentaire.id" class="mt-3 ml-12 comment__section">
                            <comment-input
                                :placeholder="`Répondre à ${getAuthorName(commentaire)}...`"
                                buttonText="Répondre"
                                :required="true"
                                @submit="(msg) => submitInlineReply(commentaire.id, msg)"
                                @cancel="cancelInlineReply"
                                :disabled="isSubmittingReply"
                            />
                        </div>

                        <div v-if="commentaire.reponses && commentaire.reponses.length > 0" class="reply-list">
                            <div 
                                v-for="reponse in commentaire.reponses" 
                                :key="reponse.id"
                                class="reply-item"
                            >
                                <div class="reply-avatar-container">
                                    <div class="reply-avatar">
                                        {{ getInitials(getAuthorName(reponse)) }}
                                    </div>
                                </div>
                                
                                <div class="reply-content">
                                    <div class="reply-meta">
                                        <div class="reply-author-info">
                                            <span class="reply-author-name">{{ getAuthorName(reponse) }}</span>
                                            <span v-if="reponse.auteur_id === currentUserId" class="reply-author-tag">Moi</span>
                                        </div>
                                        <span class="reply-date">{{ formatDate(reponse.date_creation) }}</span>
                                    </div>
                                    <p class="reply-message">{{ reponse.message }}</p>
                                    
                                    <div v-if="canEditReponse(reponse) || canDeleteReponse(reponse)" class="reply-actions">
                                        <button @click="handleEditReponse(reponse)" class="reply-action-button edit-reply-button">Modifier</button>
                                        <button @click="handleDeleteReponse(reponse)" class="reply-action-button delete-reply-button">Supprimer</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, ref, watch, onMounted, nextTick } from 'vue'
import commentInput from '@/components/input/commentInput.vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
    commentaires: {
        type: Array,
        default: () => []
    },
    reponses: {
        type: Array,
        default: () => []
    },
    currentUserId: {
        type: [String, Number],
        default: null
    },
    canReply: {
        type: Boolean,
        default: true
    },
    loading: {
        type: Boolean,
        default: false
    },
    isReplying: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['edit', 'delete', 'reply', 'editReponse', 'deleteReponse', 'submitReply'])

// Store d'authentification
const authStore = useAuthStore()

// Informations de l'utilisateur connecté
const currentUser = computed(() => authStore.user)

// J'ai mis à jour ce computed pour prendre en compte les réponses imbriquées dans les commentaires.
const totalCommentaires = computed(() => {
    let total = props.commentaires.length;
    props.commentaires.forEach(c => {
        if (c.reponses) {
            total += c.reponses.length;
        }
    });
    return total;
})

const getAuthorName = (item) => {
    // Si c'est l'utilisateur connecté, utiliser ses informations du store
    if (item.auteur_id === props.currentUserId && currentUser.value) {
        return currentUser.value.nom_complet || `${currentUser.value.first_name || ''} ${currentUser.value.last_name || ''}`.trim() || 'Vous';
    }
    
    // Sinon, utiliser les informations du commentaire/réponse
    if (item.auteur?.username) return item.auteur.username;
    if (item.auteur?.first_name || item.auteur?.last_name) {
        return `${item.auteur.first_name || ''} ${item.auteur.last_name || ''}`.trim();
    }
    return 'Utilisateur';
}

const getInitials = (name) => {
    if (!name || name === 'Utilisateur') return '??'
    return name
        .split(' ')
        .map(word => word[0])
        .join('')
        .toUpperCase()
        .substring(0, 2)
}

const formatDate = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now - date
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)
    
    if (diffMins < 1) return 'À l\'instant'
    if (diffMins < 60) return `Il y a ${diffMins} min`
    if (diffHours < 24) return `Il y a ${diffHours} h`
    if (diffDays < 7) return `Il y a ${diffDays} j`
    
    return date.toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'short',
        year: diffDays > 365 ? 'numeric' : undefined
    })
}

const canEdit = (commentaire) => {
    return props.currentUserId && commentaire.auteur_id === props.currentUserId
}

const canDelete = (commentaire) => {
    return props.currentUserId && commentaire.auteur_id === props.currentUserId
}

const canEditReponse = (reponse) => {
    return props.currentUserId && reponse.auteur_id === props.currentUserId
}

const canDeleteReponse = (reponse) => {
    return props.currentUserId && reponse.auteur_id === props.currentUserId
}

// Inline reply state
const replyingToId = ref(null)
const isSubmittingReply = ref(false)
const prevReplyCounts = ref({})

onMounted(() => {
    // Initial snapshot of reply counts
    prevReplyCounts.value = {};
    props.commentaires.forEach(c => {
        prevReplyCounts.value[c.id] = (c.reponses || []).length
    })
})

// Watch for changes in commentaires: if a new reply was added to the currently replying comment, close the inline input
watch(() => props.commentaires, (newComments) => {
    if (!replyingToId.value) return;
    const target = newComments.find(c => c.id === replyingToId.value);
    const prev = prevReplyCounts.value[replyingToId.value] || 0;
    const now = target ? (target.reponses || []).length : 0;
    if (now > prev) {
        // A reply was added — clear inline reply
        replyingToId.value = null;
    }
    // Update snapshot
    prevReplyCounts.value = {};
    newComments.forEach(c => {
        prevReplyCounts.value[c.id] = (c.reponses || []).length
    })
}, { deep: true })

const handleReply = (commentaire) => {
    // Open inline reply input for this commentaire and notify parent (backward compatibility)
    replyingToId.value = commentaire.id
    emit('reply', commentaire)

    // Focus the inline textarea once it is rendered
    nextTick(() => {
        const selector = `.comment-group[data-comment-id="${commentaire.id}"] .comment__section textarea`;
        const el = document.querySelector(selector);
        if (el) el.focus();
    })
}

const submitInlineReply = async (commentaireId, message) => {
    if (!message || !message.trim()) return;
    isSubmittingReply.value = true;
    try {
        // Emit to parent to perform the creation
        emit('submitReply', { commentaireId, message: message.trim() })
    } catch (err) {
        //console.error('Erreur submitInlineReply emit:', err)
    } finally {
        isSubmittingReply.value = false;
    }
}

const cancelInlineReply = () => {
    replyingToId.value = null
}

const handleEdit = (commentaire) => {
    emit('edit', commentaire)
}

const handleDelete = (commentaire) => {
    emit('delete', commentaire)
}

const handleEditReponse = (reponse) => {
    emit('editReponse', reponse)
}

const handleDeleteReponse = (reponse) => {
    emit('deleteReponse', reponse)
}
</script>

<style scoped>
/* Conteneur principal */
.comments-container {
    width: 100%;
    max-width: 64rem; /* max-w-4xl */
    margin-left: auto; /* mx-auto */
    margin-right: auto; /* mx-auto */
    padding: 1rem; /* Du style original */
}

/* 1. Entête */
.comments-header {
    display: flex;
    align-items: center;
    gap: 0.75rem; /* gap-3 */
    margin-bottom: 2rem; /* mb-8 */
    padding-bottom: 1rem; /* pb-4 */
    border-bottom: 1px solid #f3f4f6; /* border-b border-gray-100 */
}

.header-title {
    font-size: 1.25rem; /* text-xl */
    font-weight: 700; /* font-bold */
    color: #111827; /* text-gray-900 */
}

.comment-count-badge {
    padding: 0.25rem 0.625rem; /* px-2.5 py-0.5 */
    background-color: #eff6ff; /* bg-blue-50 */
    color: #2563eb; /* text-blue-600 */
    font-size: 0.875rem; /* text-sm */
    font-weight: 700; /* font-bold */
    border-radius: 9999px; /* rounded-full */
    border: 1px solid #dbeafe; /* border border-blue-100 */
}

/* 2. État : Aucun commentaire */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    background-color: #f9fafb; /* bg-gray-50 */
    border-radius: 1rem; /* rounded-2xl */
    border: 2px dashed #e5e7eb; /* border-2 border-dashed border-gray-200 */
    text-align: center;
}

.empty-icon-wrapper {
    width: 4rem; /* w-16 */
    height: 4rem; /* h-16 */
    background-color: white;
    border-radius: 1rem; /* rounded-2xl */
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); /* shadow-sm */
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem; /* mb-4 */
}

.empty-icon {
    height: 2rem; /* h-8 */
    width: 2rem; /* w-8 */
    color: #9ca3af; /* text-gray-400 */
}

.empty-title {
    color: #111827; /* text-gray-900 */
    font-weight: 600; /* font-semibold */
}

.empty-text {
    color: #6b7280; /* text-gray-500 */
    font-size: 0.875rem; /* text-sm */
    margin-top: 0.25rem; /* mt-1 */
}

/* 3. État : Chargement */
.loading-state {
    display: flex;
    justify-content: center;
    padding-top: 3rem; /* py-12 / 2 */
    padding-bottom: 3rem; /* py-12 / 2 */
}

.loader {
    position: relative;
    width: 2.5rem; /* w-10 */
    height: 2.5rem; /* h-10 */
}

.loader-track {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: 4px solid #dbeafe; /* border-4 border-blue-100 */
    border-radius: 9999px; /* rounded-full */
}

.loader-spinner {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: 4px solid #2563eb; /* border-4 border-blue-600 */
    border-radius: 9999px; /* rounded-full */
    border-top-color: transparent; /* border-t-transparent */
    animation: spin 1s linear infinite; /* animate-spin */
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

/* 4. Liste des commentaires */
.comments-list {
    display: flex;
    flex-direction: column;
    gap: 2rem; /* space-y-8 */
}

.comment-group {
    position: relative;
}

.reply-line {
    position: absolute;
    left: 1.25rem; /* left-5 */
    top: 3rem; /* top-12 (approximatif) */
    bottom: 0;
    width: 2px; /* w-0.5 */
    background-color: #f3f4f6; /* bg-gray-100 */
}
/* La gestion de 'group-last:bg-transparent' est complexe en CSS pur sans sélecteurs avancés ou JS, on garde la ligne pour tous */

.comment-wrapper {
    display: flex;
    gap: 1rem; /* gap-4 */
}

.comment-avatar-container {
    flex-shrink: 0; /* flex-shrink-0 */
    z-index: 10;
}

.comment-avatar {
    width: 2.5rem; /* w-10 */
    height: 2.5rem; /* h-10 */
    /* Conversion du gradient to-br from-blue-500 to-indigo-600 */
    background-image: linear-gradient(to bottom right, #3b82f6, #4f46e5); 
    border-radius: 0.5rem; /* rounded-xl */
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); /* shadow-sm */
    color: white;
    font-weight: 700; /* font-bold */
    font-size: 0.875rem; /* text-sm */
}

.comment-content-area {
    flex: 1; /* flex-1 */
    min-width: 0; /* min-w-0 */
}

/* Carte du Commentaire Principal */
.comment-card {
    background-color: white;
    padding: 1.25rem; /* p-5 */
    border-radius: 1rem; /* rounded-2xl */
    border: 1px solid #f3f4f6; /* border border-gray-100 */
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06); /* shadow-sm */
    transition: box-shadow 300ms; /* transition-shadow duration-300 */
}

.comment-card:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); /* hover:shadow-md */
}

.comment-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem; /* mb-2 */
    /* Le padding original p-8 sur le meta semble trop grand, je le réduis pour une meilleure mise en page */
    padding: 0; 
}

.meta-author-info {
    display: flex;
    align-items: center;
    gap: 0.5rem; /* gap-2 */
}

.author-name {
    font-weight: 700; /* font-bold */
    color: #111827; /* text-gray-900 */
}

.author-tag {
    padding: 0.125rem 0.5rem; /* px-2 py-0.5 */
    background-color: #2563eb; /* bg-blue-600 */
    color: white;
    font-size: 0.625rem; /* text-[10px] */
    font-weight: 900; /* font-black */
    text-transform: uppercase; /* uppercase */
    letter-spacing: 0.05em; /* tracking-wider */
    border-radius: 0.375rem; /* rounded-md */
}

.meta-date {
    font-size: 0.75rem; /* text-xs */
    color: #9ca3af; /* text-gray-400 */
    font-weight: 500; /* font-medium */
}

.comment-message {
    color: #374151; /* text-gray-700 */
    line-height: 1.625; /* leading-relaxed */
    font-size: 0.875rem; /* text-sm */
    white-space: pre-wrap; /* Maintient les sauts de ligne */
}

/* Actions du commentaire principal */
.comment-actions {
    display: flex;
    align-items: center;
    gap: 1rem; /* gap-4 */
    margin-top: 1rem; /* mt-4 */
    padding-top: 0.75rem; /* pt-3 */
    border-top: 1px solid #f9fafb; /* border-t border-gray-50 */
}

.action-button {
    display: flex;
    align-items: center;
    gap: 0.375rem; /* gap-1.5 */
    font-size: 0.75rem; /* text-xs */
    font-weight: 700; /* font-bold */
    transition: color 150ms; /* transition-colors */
    background: none;
    border: none;
    cursor: pointer;
}

.reply-button {
    color: #2563eb; /* text-blue-600 */
}

.reply-button:hover {
    color: #1d4ed8; /* hover:text-blue-700 */
}

.action-icon {
    height: 0.875rem; /* h-3.5 */
    width: 0.875rem; /* w-3.5 */
}

.action-controls {
    display: flex;
    align-items: center;
    gap: 0.75rem; /* gap-3 */
    margin-left: auto; /* ml-auto */
}

.action-controls-button {
    font-size: 0.75rem; /* text-xs */
    font-weight: 600; /* font-semibold */
    transition: color 150ms; /* transition-colors */
    background: none;
    border: none;
    cursor: pointer;
}

.edit-button {
    color: #6b7280; /* text-gray-500 */
}
.edit-button:hover {
    color: #1f2937; /* hover:text-gray-800 */
}

.delete-button {
    color: #ef4444; /* text-red-500 */
}
.delete-button:hover {
    color: #b91c1c; /* hover:text-red-700 */
}

/* 5. Liste des Réponses */
.reply-list {
    margin-top: 1rem; /* mt-4 */
    display: flex;
    flex-direction: column;
    gap: 1rem; /* space-y-4 */
    margin-left: 0.5rem; /* ml-2 */
}

.reply-item {
    display: flex;
    gap: 0.75rem; /* gap-3 */
    position: relative;
}

/* Ligne de connexion des réponses */
.reply-item::before {
    content: '';
    position: absolute;
    left: -1.25rem; /* before:-left-5 */
    top: 1.25rem; /* before:top-5 */
    width: 1.25rem; /* before:w-5 */
    height: 2px; /* before:h-0.5 */
    background-color: #f3f4f6; /* before:bg-gray-100 */
}

.reply-avatar-container {
    flex-shrink: 0; /* flex-shrink-0 */
    z-index: 10;
}

.reply-avatar {
    width: 2rem; /* w-8 */
    height: 2rem; /* h-8 */
    background-color: #f3f4f6; /* bg-gray-100 */
    border-radius: 0.5rem; /* rounded-lg */
    display: flex;
    align-items: center;
    justify-content: center;
    color: #4b5563; /* text-gray-600 */
    font-weight: 700; /* font-bold */
    font-size: 0.75rem; /* text-xs */
}

.reply-content {
    flex: 1; /* flex-1 */
    background-color: #f9fafb; /* bg-gray-50 */
    padding: 1rem; /* p-4 */
    border-radius: 0.75rem; /* rounded-xl */
    border: 1px solid #f3f4f6; /* border border-gray-100 */
}

.reply-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.25rem; /* mb-1 */
}

.reply-author-info {
    display: flex;
    align-items: center;
    gap: 0.5rem; /* gap-2 */
}

.reply-author-name {
    font-size: 0.875rem; /* text-sm */
    font-weight: 700; /* font-bold */
    color: #1f2937; /* text-gray-800 */
}

.reply-author-tag {
    font-size: 0.5625rem; /* text-[9px] */
    background-color: #e5e7eb; /* bg-gray-200 */
    color: #4b5563; /* text-gray-600 */
    padding: 0.125rem 0.375rem; /* px-1.5 py-0.5 */
    border-radius: 0.25rem; /* rounded */
    font-weight: 700; /* font-bold */
    text-transform: uppercase;
}

.reply-date {
    font-size: 0.625rem; /* text-[10px] */
    color: #9ca3af; /* text-gray-400 */
}

.reply-message {
    color: #4b5563; /* text-gray-600 */
    font-size: 0.875rem; /* text-sm */
    line-height: 1.375; /* leading-snug */
}

.reply-actions {
    display: flex;
    justify-content: flex-end; /* justify-end */
    gap: 0.75rem; /* gap-3 */
    margin-top: 0.5rem; /* mt-2 */
}

.reply-action-button {
    font-size: 0.6875rem; /* text-[11px] */
    font-weight: 700; /* font-bold */
    transition: color 150ms;
    background: none;
    border: none;
    cursor: pointer;
}

.edit-reply-button {
    color: #9ca3af; /* text-gray-400 */
}
.edit-reply-button:hover {
    color: #4b5563; /* hover:text-gray-600 */
}

.delete-reply-button {
    color: #f87171; /* text-red-400 */
}
.delete-reply-button:hover {
    color: #dc2626; /* hover:text-red-600 */
}

/* La section pour la barre de défilement (déjà en CSS classique) */
.comments-container::-webkit-scrollbar {
    width: 4px;
}

.comments-container::-webkit-scrollbar-track {
    background: transparent;
}

.comments-container::-webkit-scrollbar-thumb {
    background: #e2e8f0;
    border-radius: 10px;
}

.comments-container::-webkit-scrollbar-thumb:hover {
    background: #cbd5e1;
}
</style>