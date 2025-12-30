<template>
    <button 
        class="main-button"
    >   
        <span v-if="isloading === false">{{ label }}</span>

        <span v-else class="loading loading-spinner loading-md"></span>

    </button>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
    name: 'prevButton',

    components:{
    },
    
    props: {
        label: {
            type: String,
            default: 'Retour'
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
    background: var(--adn-gray-color);
    padding: 0.8rem;
    border: none;
    border-radius: 1rem;
    font-size: 1rem;
    font-weight: 500;
    width: 100%;
    max-width: 400px;
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
    background: var(--adn-gray-color);
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