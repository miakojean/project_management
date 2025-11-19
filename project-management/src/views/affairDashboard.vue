<template>
  <div class="dashboard-container">
    
    <sidebar />

    <header class="header-area">
      <navbar />
    </header>

    <main class="main-area">
      <customerSectionFolder/>
    </main>

    <footer class="footer-area">
      <p>&copy; 2024 Mon Entreprise</p>
    </footer>

  </div>
</template>

<script>
import navbar from '@/components/navigation/navbar.vue';
import sidebar from '@/components/navigation/sidebar.vue';
import customerSectionFolder from '@/components/section/customerSectionFolder.vue';

export default {
    name: 'DashboardLayout',
    components: {
      navbar,
      sidebar,
      customerSectionFolder
        
    }
}
</script>

<style scoped>
/* --- Configuration de la Grille --- */
.dashboard-container {
  display: grid;
  height: 100vh;
  grid-template-columns: 250px 1fr; 
  grid-template-rows: 60px 1fr auto;
  grid-template-areas: 
    "sidebar header"
    "sidebar main"
    "sidebar footer";
}

/* --- Styles des Zones --- */

/* NOTE: Vue applique automatiquement le style scoped du parent 
   à la racine du composant enfant. Donc ce style s'appliquera 
   bien à la balise <aside> qui est dans sidebar.vue 
*/
.sidebar-area {
  grid-area: sidebar;
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  overflow-y: auto;
}

.header-area {
  grid-area: header;
  background-color: #ffffff;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
}

.main-area {
  grid-area: main;
  background-color: #ffffff;
  overflow-y: auto;
  padding: 2rem;
}

.footer-area {
  grid-area: footer;
  background-color: #ffffff;
  border-top: 1px solid #e0e0e0;
  padding: 1rem;
  text-align: center;
  font-size: 0.9rem;
  color: #666;
}
</style>