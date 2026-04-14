<template>
    <button 
        class="main-button"
    >   
        
        <span v-if="isloading === false">{{ label }}</span>
        <svg v-if="isloading === false" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25 21 12m0 0-3.75 3.75M21 12H3" />
        </svg>
        <span v-else class="loading loading-spinner loading-md"></span>

    </button>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
    name: 'MainButton',

    components:{
    },
    
    props: {
        label: {
            type: String,
            default: 'Suivant'
        },
        isloading:{
            type:Boolean,
            default: false
        }
    }
})
</script>

<style scoped>
.main-button {
    background: var(--primary-color);
    padding: 0.8rem;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: 500;
    width: 100%;
    max-width: 200px;
    transition: all 0.3s ease-in-out;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
}

.main-button span, svg{
    color: white;
}

.main-button:hover {
    border-radius: 0.2rem;
    background: var(--primary-color);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px #dfdfdf;
}

.main-button:active {
    transform: translateY(0);
    box-shadow: 0 2px 6px rgba(47, 128, 237, 0.2);
}

.main-button:disabled {
    background: #ccc;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}
</style>