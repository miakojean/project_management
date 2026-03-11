<template>
    <div class="logo" @click="goToDashboard">
        <img src="../../assets//juristrack.jpeg" class="log--pic" alt="logo de Adn consulting">
        <h4>Juristrack</h4>
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
}

img{
    width:50px;
    height:50px;
    background-size: cover;
    border-radius: 50%;
}

.logo h4{
    font-size: 1.2rem;
    font-weight: 400;
    color: #fff;
}

.logo h4 span{
    font-weight: 600;
    color: #7ac17a;
}
</style>