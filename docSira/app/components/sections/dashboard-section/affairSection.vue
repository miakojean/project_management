<template>
  <section class="main-section w-full h-full">


    <div class="actions">
      <folder v-for="folder in 22" 
        :key="folder"
      />
    </div>
    

  </section>
</template>

<script lang="ts">
import BaseInput from '../../BaseInput/BaseInput.vue'
import folderCards from '../../cards/folderCards.vue'
import featuresCard from '../../cards/featuresCards.vue'
import folder from '../../tools/folder.vue'

import { ref } from 'vue';
import { useRouter } from 'vue-router';
export default {

  components:{
    BaseInput,
    folderCards,
    featuresCard,
    folder
  },

  setup(){

    const router = useRouter();

    return{
      router,
    }

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

.actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 2 colonnes par défaut (mobile) */
  gap: 0.75rem;                        /* espacement entre les cartes */
  max-width: 900px;
  margin: 0 auto;                      /* centrage horizontal du bloc */
  justify-items: center;               /* centrage de chaque carte dans sa cellule */
  align-items: center;                 /* centrage vertical (optionnel) */
  height: 100vh;
}

/* Tablette : 3 colonnes */
@media (min-width: 768px) {
  .actions {
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }
}

/* Desktop : 4 colonnes */
@media (min-width: 1024px) {
  .actions {
    padding-top: 3rem;
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
    width:100%;
  }
}

</style>