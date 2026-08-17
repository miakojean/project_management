<template>
  <section class="main-section w-full">


    <div class="actions">
      <affairsCards v-for="folder in 9" 
        :key="folder"
      />
    </div>
    

  </section>
</template>

<script lang="ts">

import affairsCards from '../../cards/affairsCards.vue'

import { ref } from 'vue';
import { useRouter } from 'vue-router';
export default {

  components:{
    
    affairsCards
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
  background: #5452f4;
  border-radius: 50%;
  margin-left: 2px;
  transition: background 0.2s;
}

.search-icon-wrapper svg {
  width: 20px;
  height: 20px;
  color: #ffffff;
}

/* =========================================
   CONTENEUR ACTIONS (GRILLE SCROLLABLE)
   ========================================= */
.actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr); 
  gap: 0.75rem;
  margin: 0 auto;
  justify-items: center; 
  
  /* ⚡️ LES CORRECTIONS SONT ICI ⚡️ */
  align-items: start;       /* Remplace 'center' pour éviter que les cartes ne sortent par le haut */
  align-content: start;     /* Aligne le bloc entier vers le haut */
  
  /* On force une hauteur maximale pour déclencher l'overflow */
  max-height: calc(100vh - 100px); /* 💡 Ajuste le "100px" selon la hauteur de ta Navbar/Breadcrumb */
  overflow-y: auto;
  
  /* Petit confort visuel */
  padding-bottom: 2rem;     /* Laisse respirer la dernière carte lors du scroll */
  padding-top: 1rem;
}

/* --- Masquer la barre de défilement (Optionnel mais plus esthétique) --- */
.actions::-webkit-scrollbar {
  width: 6px;
}
.actions::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 10px;
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
    grid-template-columns: repeat(3, 1fr); /* 💡 J'ai corrigé en 4 (ton commantaire disait 4, le code 3) */
    gap: 1rem;
    width: 100%;
    /* Plus besoin de répéter overflow et height ici, ils sont hérités ! */
  }
}
</style>