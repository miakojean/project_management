<template>
  <section class="main-section w-full">


      <div class="actions">
        <folderCards title="Dossiers"/>
        <folderCards title="Clients"/>
        <folderCards title="Archives"/>
      </div>
    

  </section>
</template>

<script>
import BaseInput from '../../BaseInput/BaseInput.vue'
import folderCards from '../../cards/folderCards.vue'
import featuresCard from '../../cards/featuresCards.vue'
export default {

    components:{
      BaseInput,
      folderCards,
      featuresCard
    }

}
</script>

<style scoped>

.search-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: #5452f4;        /* fond gris clair */
  border-radius: 50%;         /* cercle */
  margin-left: 2px;           /* ajustement si besoin */
  transition: background 0.2s;
}

.search-icon-wrapper svg {
  width: 20px;
  height: 20px;
  color: #ffffff;             /* couleur de l'icône */
}

.actions{
  width: 100%;
  max-width: 900px;
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

</style>