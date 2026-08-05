<template>
  <section class="main-section w-full">
    
    <h3>Bienvenu Jean Yves, très ravi de vous revoir.</h3>

    <BaseInput placeholder="Trouver votre dossier/client">
      <template #prepend>
        <div class="search-icon-wrapper">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke-width="1.5" 
            stroke="currentColor"
          >
            <path 
              stroke-linecap="round" 
              stroke-linejoin="round" 
              d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" 
            />
          </svg>
        </div>
      </template>
    </BaseInput>

    <div class="actions">
      <features-card 
        title="Dossiers" 
        content="Gérer correctement tous vos dossiers et mettez de l'ordre dans votre espace de travail"
        @click="()=> {router.push('/dashboard/affairs')}"
      />
      <features-card 
        title="Clients" 
        content="Gérer correctement tous vos clients avec des outils puissants"
        @click="()=> {router.push('/dashboard/customer')}"
      />
      <features-card 
        title="Archives" 
        content="Accéder à tous vos documents archivés en quelques clics"
        @click="()=>{router.push('/dashboard/archives')}"
      />
    </div>

  </section>
</template>

<script lang="ts">
import BaseInput from '../../BaseInput/BaseInput.vue'
import folderCards from '../../cards/folderCards.vue'
import featuresCard from '../../cards/featuresCards.vue'

import { useRouter } from 'vue-router'
export default {

  components:{
    BaseInput,
    folderCards,
    featuresCard
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
  background: var(--primary-color );        /* fond gris clair */
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