<template>
    <button 
        class="main-button"
        :style="{ maxWidth: maxWidth }"
    >   
        
        <span v-if="isloading === false">{{ label }}</span>
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
            default: 'inscription'
        },
        maxWidth: {
            type: String,
            default: '500px'
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
    color: white;
    font-size: 1rem;
    font-weight: 500;
    width: 100%;
    transition: all 0.3s ease-in-out;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
}

.main-button span{
    color: white;
}

.main-button:hover {
    border-radius: 0.2rem;
    background: #2f80ed;
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