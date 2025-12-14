<template>
    <div class="comment__section w-full">
        <form class="w-full flex flex-col gap-4" @submit.prevent="handleSubmit">
            <label for="comment" class="w-full text-base font-semibold text-gray-800 text-left">
                Ajouter un commentaire
            </label>
            
            <textarea 
                id="comment" 
                v-model="commentText"
                :placeholder="props.placeholder"
                rows="4"
                :maxlength="props.maxLength"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-300 resize-none text-gray-800 placeholder-gray-500 shadow-sm"
                :class="{ 'border-red-500 focus:ring-red-100': error }"
                @input="clearError"
            ></textarea>
            
            <!-- Compteur de caractères et message d'erreur -->
            <div class="flex justify-between items-center">
                <div v-if="error" class="text-sm text-red-600 font-medium">
                    {{ error }}
                </div>
                <div v-else-if="showCounter" class="text-sm text-gray-500 ml-auto">
                    {{ commentText.length }} / {{ props.maxLength }}
                </div>
            </div>
            
            <!-- Bouton aligné à droite -->
            <div class="w-full flex justify-end gap-3">
                <mainButton 
                    max-width="200px"
                    :label="props.buttonText"
                    :disabled="isSubmitting || (props.required && !commentText.trim())"
                    :loading="isSubmitting"
                    @click="handleSubmit"
                />
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import mainButton from '../button/mainButton.vue'

const props = defineProps({
    placeholder: {
        type: String,
        default: 'Entrez votre commentaire ici...'
    },
    buttonText: {
        type: String,
        default: 'Commenter'
    },
    required: {
        type: Boolean,
        default: false
    },
    maxLength: {
        type: Number,
        default: 500
    },
    showCounter: {
        type: Boolean,
        default: true
    }
})

const emit = defineEmits(['submit', 'cancel'])

const commentText = ref('')
const isSubmitting = ref(false)
const error = ref('')

const clearError = () => {
    if (error.value) error.value = ''
}

const handleSubmit = async () => {
    // Validation du champ vide
    if (props.required && !commentText.value.trim()) {
        error.value = 'Le commentaire ne peut pas être vide'
        return
    }
    
    // Validation de la longueur
    if (commentText.value.length > props.maxLength) {
        error.value = `Le commentaire ne peut pas dépasser ${props.maxLength} caractères`
        return
    }
    
    isSubmitting.value = true
    error.value = ''
    
    try {
        // Envoi de l'événement submit avec le contenu
        await emit('submit', commentText.value.trim())
        commentText.value = '' // Réinitialiser après succès
    } catch (err) {
        // Gestion de l'erreur
        error.value = err.message || 'Une erreur est survenue lors de la publication.'
    } finally {
        isSubmitting.value = false
    }
}

const handleCancel = () => {
    emit('cancel')
    commentText.value = ''
    error.value = ''
}
</script>

<style scoped>
/* Assure une hauteur minimale pour la zone de texte */
textarea {
    min-height: 100px;
}
</style>