<template>
  <main>
    <section class="left__side center__flex__column">
      <img src="../assets/undraw_working_n9u0.svg" alt="">
    </section>
    <section class="right__side center__flex">
      <registration-form/>
    </section>
  </main>
</template>

<script>
import registrationForm from '@/components/forms/registrationForm.vue';
export default {

  components:{
    registrationForm,
  }

}
</script>

<style scoped>
main{
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.right__side{
  height: 100vh;
  padding: 1rem;
  width: 50%;
}

.left__side{
  height: 100vh;
  background: #f3f3f3;
  width: 50%;
}

img{
  width: 100%;
  height: 100%;
  max-width: 500px;
  max-height: 500px;
  background-size: cover;

}
</style>