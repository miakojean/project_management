<template>
    <div class="customer__cards__container">
        <customerCards v-for="(card, index) in 6" :key="index"/>
    </div>
</template>

<script>
import customerCards from '../cards/customerCards.vue';
export default {
    components:{
        customerCards
    }
}
</script>

<style scoped>
.customer__cards__container{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1rem;
}
</style>