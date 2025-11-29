<template>
<div class="input__family">
    <label :for="label">{{ label }}</label>
    <textarea 
        :id="label" 
        :class="{
            'input-filled': modelValue !== '',
            'input-error': showError
        }"
        :value="modelValue"
        @input="updateValue"
        @blur="handleBlur"
        :placeholder="placeholder"
        rows="4"
    ></textarea>
    <span v-if="showError" class="error__message">{{ error || errorMessage }}</span>
</div>
</template>

<script>
import { computed, ref } from 'vue';

export default {
    name: 'InputArea',
    props: {
        label: {
            type: String,
            default: "Je suis"
        },
        placeholder: {
            type: String,
            default: "Entrer la description"
        },
        inputId: {
            type: String,
            default: 'username'
        },
        errorMessage: {
            type: String,
            default: 'Champs réquis*'
        },
        showValidation: {
            type: Boolean,
            default: false
        },
        type: {
            type: String,
            default: 'text'
        },
        modelValue: {
            type: String,
            default: ""
        },
        error: {
            type: String,
            default: ''
        }
    },

    emits: ['update:modelValue', 'blur'],

    setup(props, { emit }) {
        const isTouched = ref(false);
        
        const showError = computed(() => {
            return (props.showValidation || isTouched.value) && props.modelValue.trim() === '';
        });

        const updateValue = (event) => {
            emit('update:modelValue', event.target.value);
        };

        const handleBlur = () => {
            isTouched.value = true;
            emit('blur');
        };

        return {
            showError,
            updateValue,
            handleBlur,
            isTouched
        };
    }
};
</script>

<style scoped>
.input__family {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
}

label {
    font-weight: 500;
    color: #374151;
    font-size: 0.9rem;
}

textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 0.9rem;
    resize: vertical;
    min-height: 80px;
    transition: all 0.2s ease;
}

textarea:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input-filled {
    border-color: #10b981;
}

.input-error {
    border-color: #ef4444 !important;
    background-color: #fef2f2;
}

.error__message {
    color: #ef4444;
    font-size: 0.75rem;
    margin-top: 0.25rem;
}

.toggle__btn:focus {
    outline: 2px solid #55a7ff;
}
</style>