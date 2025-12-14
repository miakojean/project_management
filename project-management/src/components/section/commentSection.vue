<template>
    <div class="comments__container w-full max-w-4xl mx-auto">
        <div class="flex items-center gap-3 mb-8 pb-4 border-b border-gray-100">
            <h4 class="text-xl font-bold text-gray-900">Commentaires</h4>
            <span class="px-2.5 py-0.5 bg-blue-50 text-blue-600 text-sm font-bold rounded-full border border-blue-100">
                {{ totalCommentaires }}
            </span>
        </div>

        <div v-if="commentaires.length === 0 && !loading" class="flex flex-col items-center justify-center py-16 px-4 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 text-center">
            <div class="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
            </div>
            <p class="text-gray-900 font-semibold">Aucun commentaire pour le moment</p>
            <p class="text-gray-500 text-sm mt-1">Soyez le premier à partager votre avis sur ce dossier.</p>
        </div>

        <div v-if="loading" class="flex justify-center py-12">
            <div class="relative w-10 h-10">
                <div class="absolute top-0 left-0 w-full h-full border-4 border-blue-100 rounded-full"></div>
                <div class="absolute top-0 left-0 w-full h-full border-4 border-blue-600 rounded-full border-t-transparent animate-spin"></div>
            </div>
        </div>

        <div v-else class="space-y-8">
            <div 
                v-for="commentaire in commentaires" 
                :key="commentaire.id"
                class="group relative"
            >
                <div v-if="commentaire.reponses && commentaire.reponses.length > 0" 
                     class="absolute left-5 top-12 bottom-0 w-0.5 bg-gray-100 group-last:bg-transparent"></div>

                <div class="flex gap-4">
                    <div class="flex-shrink-0 z-10">
                        <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-sm text-white font-bold text-sm">
                            {{ getInitials(getAuthorName(commentaire)) }}
                        </div>
                    </div>

                    <div class="flex-1 min-w-0">
                        <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow duration-300">
                            <div class="flex items-center justify-between mb-2">
                                <div class="flex items-center gap-2">
                                    <span class="font-bold text-gray-900">{{ getAuthorName(commentaire) }}</span>
                                    <span v-if="commentaire.auteur_id === currentUserId" class="px-2 py-0.5 bg-blue-600 text-white text-[10px] font-black uppercase tracking-wider rounded-md">
                                        Vous
                                    </span>
                                </div>
                                <span class="text-xs text-gray-400 font-medium">{{ formatDate(commentaire.date_creation) }}</span>
                            </div>
                            
                            <p class="text-gray-700 leading-relaxed text-sm whitespace-pre-wrap">{{ commentaire.message }}</p>

                            <div class="flex items-center gap-4 mt-4 pt-3 border-t border-gray-50">
                                <button v-if="canReply" @click="handleReply(commentaire)" class="flex items-center gap-1.5 text-xs font-bold text-blue-600 hover:text-blue-700 transition-colors">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                                        <path fill-rule="evenodd" d="M7.707 3.293a1 1 0 010 1.414L5.414 7H11a7 7 0 017 7v2a1 1 0 11-2 0v-2a5 5 0 00-5-5H5.414l2.293 2.293a1 1 0 11-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                                    </svg>
                                    Répondre
                                </button>
                                
                                <div v-if="canEdit(commentaire) || canDelete(commentaire)" class="flex items-center gap-3 ml-auto">
                                    <button v-if="canEdit(commentaire)" @click="handleEdit(commentaire)" class="text-xs font-semibold text-gray-500 hover:text-gray-800 transition-colors">Modifier</button>
                                    <button v-if="canDelete(commentaire)" @click="handleDelete(commentaire)" class="text-xs font-semibold text-red-500 hover:text-red-700 transition-colors">Supprimer</button>
                                </div>
                            </div>
                        </div>

                        <div v-if="commentaire.reponses && commentaire.reponses.length > 0" class="mt-4 space-y-4 ml-2">
                            <div 
                                v-for="reponse in commentaire.reponses" 
                                :key="reponse.id"
                                class="flex gap-3 relative before:absolute before:-left-5 before:top-5 before:w-5 before:h-0.5 before:bg-gray-100"
                            >
                                <div class="flex-shrink-0 z-10">
                                    <div class="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center text-gray-600 font-bold text-xs">
                                        {{ getInitials(getAuthorName(reponse)) }}
                                    </div>
                                </div>
                                
                                <div class="flex-1 bg-gray-50 p-4 rounded-xl border border-gray-100">
                                    <div class="flex items-center justify-between mb-1">
                                        <div class="flex items-center gap-2">
                                            <span class="text-sm font-bold text-gray-800">{{ getAuthorName(reponse) }}</span>
                                            <span v-if="reponse.auteur_id === currentUserId" class="text-[9px] bg-gray-200 text-gray-600 px-1.5 py-0.5 rounded font-bold uppercase">Moi</span>
                                        </div>
                                        <span class="text-[10px] text-gray-400">{{ formatDate(reponse.date_creation) }}</span>
                                    </div>
                                    <p class="text-gray-600 text-sm leading-snug">{{ reponse.message }}</p>
                                    
                                    <div v-if="canEditReponse(reponse) || canDeleteReponse(reponse)" class="flex justify-end gap-3 mt-2">
                                        <button @click="handleEditReponse(reponse)" class="text-[11px] font-bold text-gray-400 hover:text-gray-600">Modifier</button>
                                        <button @click="handleDeleteReponse(reponse)" class="text-[11px] font-bold text-red-400 hover:text-red-600">Supprimer</button>
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
import { computed } from 'vue'

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

const emit = defineEmits(['edit', 'delete', 'reply', 'editReponse', 'deleteReponse'])

const totalCommentaires = computed(() => {
    return props.commentaires.length + props.reponses.length;
})

const getAuthorName = (item) => {
    if (item.auteur_nom) return item.auteur_nom;
    if (item.auteur?.nom_complet) return item.auteur.nom_complet;
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

const handleReply = (commentaire) => {
    emit('reply', commentaire)
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
.comments__container {
    padding: 1rem;
}

/* Scrollbar personnalisée plus fine */
.comments__container::-webkit-scrollbar {
    width: 4px;
}

.comments__container::-webkit-scrollbar-track {
    background: transparent;
}

.comments__container::-webkit-scrollbar-thumb {
    background: #e2e8f0;
    border-radius: 10px;
}

.comments__container::-webkit-scrollbar-thumb:hover {
    background: #cbd5e1;
}
</style>