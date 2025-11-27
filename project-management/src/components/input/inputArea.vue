<template>
<div class="input__family">
    <label :for="label">{{ label }}</label>
    <textarea :id="label" 
    :class="{
    'input-filled': fieldInfo !=='',
    'input-error': showError
    }"
    v-model="inputValue" 
    :placeholder="placeholder"
    rows="4"
    @change="updateValue"></textarea>
</div>
</template>

<script>
import { computed, ref, watch } from 'vue';

export default {
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
    type:{
    type:String,
    default: 'text'
    },
    modelValue:{
    type:String,
    default:""
    }
},

emits: ['update:modaleValue', 'blur'],

setup(props, { emit }){

    const fieldInfo = ref(props.modelValue);

    const showError = computed(() => {
    return props.showValidation && fieldInfo.value.trim() === '';
    })

    watch(() => props.modelValue, (newVal) => {
    fieldInfo.value = newVal;
    })

    watch(fieldInfo, (newVal) => {
    emit('update:modelValue', newVal);
    });

    return {
    fieldInfo,
    showError,
    }


}

}
</script>

<style scoped>

.toggle__btn:focus {
outline: 2px solid #55a7ff;
}

.error__message {
color: crimson;
font-size: 0.85rem;
width: 100%;
text-align: left;
margin: 0;
}

.input-error input {
border-color: crimson;
background-color: #ffe6e6;
}

</style>