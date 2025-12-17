<template>
    <div class="logo" @click="goToDashboard">
        <img src="../../../public/LOGO.png" alt="logo de Adn consulting">
        <h4><span>adn</span> consulting</h4>
    </div>
</template>

<script>
import { useRouter } from 'vue-router';
export default {
    setup(){
        const router = useRouter()
        const goToDashboard = () =>{
            router.push('/dashboard')
        }
        return{
            router,
            goToDashboard
        }
    }
}
</script>

<style scoped>
.logo{
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: start;
    gap: 1rem;
    cursor: pointer;
    border-bottom: 1px solid #e5e7eb;
}

img{
    width:50px;
    height:50px;
    background-size: cover;
}

.logo h4{
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--secondary-color);
}

.logo h4 span{
    color: var(--primary-color);
}
</style>