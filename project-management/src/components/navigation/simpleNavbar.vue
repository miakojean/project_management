<template>
    <nav>
        <brand/>
    </nav>
</template>

<script>
import brand from './brand.vue';
export default {
    components:{
        brand
    }
}
</script>

<style scoped>
nav{
    background: var(--primary-color);
    width: 100%;
    padding: 1rem;
}

img{
    width:50px;
    height:50px;
    background-size: cover;
}

.logo{
    display: flex;
    align-items: center;
    gap: 1rem;
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