<!-- affairDashboard.vue -->
<template>
  <div class="dashboard-container">
    
    <sidebar />

    <header class="header-area">
      <navbar />
    </header>

    <main class="main-area">
      <affairIndexSection/>
    </main>

    <footer class="footer-area">
      <p>&copy; 2025 Adn consulting</p>
    </footer>

  </div>
</template>

<script>
import navbar from '@/components/navigation/navbar.vue';
import sidebar from '@/components/navigation/sidebar.vue';
import customerSectionFolder from '@/components/section/customerSectionFolder.vue';
import affairIndexSection from '@/components/section/affairIndexSection.vue';
import clientsMonthlyChart from '@/components/charts/ClientsMonthlyChart.vue';

export default {
    name: 'DashboardLayout',
    components: {
      navbar,
      sidebar,
      customerSectionFolder,
      affairIndexSection
      , clientsMonthlyChart
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

.sidebar-area {
  grid-area: sidebar;
  background-color:#006EA6;
  color: white;
  padding: 1rem;
  overflow-y: auto;
  border-right: 1px solid #e5e7eb;
}

.header-area {
  grid-area: header;
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
}

.main-area {
  grid-area: main;
  background-color: #f9fafb; /* Légère différence de fond pour mieux voir la séparation */
  overflow-y: auto;
  padding: 2rem;
}

.footer-area {
  grid-area: footer;
  background-color: #ffffff;
  border-top: 1px solid #e5e7eb;
  padding: 1rem;
  text-align: center;
  font-size: 0.9rem;
  color: #666;
}

/* Responsive - Masquer le sidebar sur mobile */
@media (max-width: 768px) {
  .dashboard-container {
    grid-template-columns: 1fr;
    grid-template-areas: 
      "header"
      "main"
      "footer";
  }

  .sidebar-area {
    display: none; /* À remplacer par un menu hamburger mobile */
  }

  .header-area{
    display: none;
  }
}
</style>