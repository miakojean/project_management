<template>
    <div class="logo">
        <img src="../../../public/LOGO.png" alt="logo de Adn consulting">
        <h4> <span>ADN</span> CONSULTING</h4>
    </div>
</template>

<script>
export default {

}
</script>

<style scoped>
.logo{
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: start;
    gap: 1rem;
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