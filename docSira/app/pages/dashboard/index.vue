<template>
  <div class="main-layout">
    <!-- Sidebar -->
    <sidebar />

    <!-- Contenu principal -->
    <main class="main-content">
      <navbar />
      <dashboarSection class="dashboard-section" />
    </main>
  </div>
</template>

<script>
import navbar from '../../components/navbar/navbar.vue'
import dashboarSection from '../../components/sections/dashboard-section/dashboardSection.vue'
import sidebar from '../../components/navbar/sidebar.vue'

export default {
  components: {
    dashboarSection,
    sidebar,
    navbar
  }
}
</script>

<style scoped>
/* === LAYOUT PRINCIPAL === */
.main-layout {
  display: flex;
  height: 100vh;                 /* Hauteur pleine de l'écran */
  overflow: hidden;              /* Empêche le débordement global */
  background: #f9fafb;           /* Couleur de fond (optionnelle) */
}

/* === SIDEBAR === */
/* La sidebar est supposée avoir une largeur fixe (ex: 250px) et une hauteur 100% */
/* Si elle est responsive, on gère avec des classes supplémentaires */

/* === CONTENU PRINCIPAL === */
.main-content {
  flex: 1;                       /* Prend tout l'espace restant */
  width: 100%;
  display: flex;
  flex-direction: column;        /* Navbar en haut, section en dessous */
  overflow-y: auto;              /* Scroll si le contenu dépasse */
  overflow-x: hidden;
  padding: 0 0 0.5rem 0;  /* Espace en bas pour la sidebar mobile */
  background: #e9ebee;
}

/* La section du dashboard prend tout l'espace vertical restant */
.dashboard-section {
  flex: 1;
}

/* Option : si tu veux un comportement différent sur grand écran */
@media (min-width: 1024px) {
  .main-layout {
    flex-direction: row;         /* Par défaut c'est déjà row, mais on le précise */
  }
  .main-content {
    padding-bottom: 1rem;        /* Pas d'espace supplémentaire sur desktop */
  }
}
</style>