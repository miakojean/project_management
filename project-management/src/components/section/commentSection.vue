<template>
    <div class="comments__list w-full">
        <!-- En-tête -->
        <div class="mb-6">
            <h4 class="text-lg font-bold text-gray-800">
                Commentaires ({{ comments.length }})
            </h4>
        </div>

        <!-- État vide -->
        <div v-if="comments.length === 0" class="text-center py-8 text-gray-500">
            <p>Aucun commentaire pour le moment</p>
        </div>

        <!-- Liste des commentaires -->
        <div v-else class="space-y-4">
            <div 
                v-for="comment in comments" 
                :key="comment.id"
                class="bg-white p-4 rounded-lg border border-gray-200"
            >
                <!-- En-tête -->
                <div class="flex items-center gap-3 mb-3">
                    <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                        <span class="text-blue-600 text-xs font-semibold">
                            {{ getInitials(comment.author) }}
                        </span>
                    </div>
                    <div>
                        <p class="font-medium text-gray-800">{{ comment.author }}</p>
                        <p class="text-xs text-gray-500">{{ formatDate(comment.date) }}</p>
                    </div>
                </div>

                <!-- Contenu -->
                <p class="text-gray-700">{{ comment.content }}</p>

                <!-- Actions -->
                <div class="flex justify-end gap-3 mt-3 pt-3 border-t border-gray-100">
                    <button 
                        v-if="canReply"
                        @click="$emit('reply', comment)"
                        class="text-sm text-blue-600 hover:text-blue-800"
                    >
                        Répondre
                    </button>
                    <button 
                        v-if="canEdit(comment)"
                        @click="$emit('edit', comment)"
                        class="text-sm text-gray-600 hover:text-gray-800"
                    >
                        Modifier
                    </button>
                    <button 
                        v-if="canDelete(comment)"
                        @click="$emit('delete', comment)"
                        class="text-sm text-red-600 hover:text-red-800"
                    >
                        Supprimer
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    comments: {
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
    }
})

const emit = defineEmits(['edit', 'delete', 'reply'])

const getInitials = (name) => {
    if (!name) return '??'
    return name
        .split(' ')
        .map(word => word[0])
        .join('')
        .toUpperCase()
        .substring(0, 2)
}

const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

const canEdit = (comment) => {
    return props.currentUserId && comment.userId === props.currentUserId
}

const canDelete = (comment) => {
    return props.currentUserId && comment.userId === props.currentUserId
}
</script>