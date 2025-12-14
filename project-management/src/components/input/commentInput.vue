<template>
    <div class="comment__section w-full">
        <form class="w-full flex flex-col gap-4" @submit.prevent="handleSubmit">
            <label for="comment" class="w-full text-base font-semibold text-gray-800 text-left">
                {{ props.label }}
            </label>
            
            <textarea 
                id="comment" 
                v-model="commentText"
                :placeholder="props.placeholder"
                rows="4"
                :maxlength="props.maxLength"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-300 resize-none text-gray-800 placeholder-gray-500 shadow-sm"
                :class="{ 
                    'border-red-500 focus:ring-red-100': error,
                    'border-yellow-500 focus:ring-yellow-100': props.isEditing
                }"
                @input="clearError"
                ref="textareaRef"
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
            
            <!-- Boutons -->
            <div class="w-full flex justify-end gap-3">
                <button 
                    v-if="props.isEditing || props.showCancel"
                    type="button"
                    @click="handleCancel"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors duration-200"
                    :disabled="isSubmitting"
                >
                    Annuler
                </button>
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
import { ref, onMounted, watch } from 'vue'
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
    label: {
        type: String,
        default: 'Ajouter un commentaire'
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
    },
    showCancel: {
        type: Boolean,
        default: false
    },
    isEditing: {
        type: Boolean,
        default: false
    },
    initialValue: {
        type: String,
        default: ''
    }
})

const emit = defineEmits(['submit', 'cancel'])

const commentText = ref('')
const isSubmitting = ref(false)
const error = ref('')
const textareaRef = ref(null)

const clearError = () => {
    if (error.value) error.value = ''
}

const handleSubmit = async () => {
    if (props.required && !commentText.value.trim()) {
        error.value = 'Le commentaire ne peut pas être vide'
        textareaRef.value?.focus()
        return
    }
    
    if (commentText.value.length > props.maxLength) {
        error.value = `Le commentaire ne peut pas dépasser ${props.maxLength} caractères`
        return
    }
    
    isSubmitting.value = true
    error.value = ''
    
    try {
        await emit('submit', commentText.value.trim())
        if (!props.isEditing) {
            commentText.value = ''
        }
    } catch (err) {
        error.value = err.message || 'Une erreur est survenue lors de la publication.'
    } finally {
        isSubmitting.value = false
    }
}

const handleCancel = () => {
    emit('cancel')
    commentText.value = props.isEditing ? props.initialValue : ''
    error.value = ''
}

// Focus sur le textarea au montage
onMounted(() => {
    commentText.value = props.initialValue
    if (props.isEditing && textareaRef.value) {
        textareaRef.value.focus()
        textareaRef.value.select()
    }
})

// Mettre à jour la valeur initiale quand elle change
watch(() => props.initialValue, (newValue) => {
    commentText.value = newValue
})
</script>