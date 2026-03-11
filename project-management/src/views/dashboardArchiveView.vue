<!-- affairDashboard.vue -->
<template>
  <div :class="['dashboard-container', { 'sidebar-collapsed': isSidebarCollapsed, 'mobile': isMobile }]">
    
   <!-- Bouton hamburger visible uniquement sur mobile -->
    <button v-if="isMobile" class="hamburger-btn" @click="isSidebarCollapsed = false">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
      </svg>
    </button>

    <sidebar 
      :is-collapsed-prop="isSidebarCollapsed"
      @collapse-change="onCollapseChange"
    />

    <header class="header-area">
      <navbar />
    </header>

    <main class="main-area">
      <archiveSection/>
    </main>

    <footer class="footer-area">
      <p>&copy; 2025 Adn consulting</p>
    </footer>

  </div>
</template>

<script>
import navbar from '@/components/navigation/navbar.vue';
import sidebar from '@/components/navigation/sidebar.vue';
import archiveSection from '@/components/section/archiveSection.vue';
import affairIndexSection from '@/components/section/affairIndexSection.vue';
import { ref, onMounted, onUnmounted } from 'vue';

export default {
    name: 'DashboardLayout',
    components: {
      navbar,
      sidebar,
      affairIndexSection,
      archiveSection
    },
    setup() {
      const isSidebarCollapsed = ref(false);
      const isMobile = ref(false);

      const checkMobile = () => {
        isMobile.value = window.innerWidth < 768;
        if (isMobile.value) {
          isSidebarCollapsed.value = true;
        }
      };

      const onCollapseChange = (collapsed) => {
        isSidebarCollapsed.value = collapsed;
      };

      onMounted(() => {
        checkMobile();
        window.addEventListener('resize', checkMobile);
      });

      onUnmounted(() => {
        window.removeEventListener('resize', checkMobile);
      });

      return {
        isSidebarCollapsed,
        isMobile,
        onCollapseChange,
      };
    }
}
</script>

<style scoped>
/* --- Configuration de la Grille --- */
.dashboard-container {
  display: grid;
  height: 100vh;
  grid-template-columns: 260px 1fr;
  grid-template-rows: 60px 1fr auto;
  grid-template-areas: 
    "sidebar header"
    "sidebar main"
    "sidebar footer";
  transition: grid-template-columns 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Collapsed : sidebar réduite à 68px */
.dashboard-container.sidebar-collapsed {
  grid-template-columns: 68px 1fr;
}

/* --- Styles des Zones --- */
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
  background-color: #f9fafb;
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

/* --- Bouton hamburger mobile --- */
.hamburger-btn {
  display: none;
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 60;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  background: var(--primary-color, #006EA6);
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  transition: background 0.2s;
}

.hamburger-btn svg {
  width: 22px;
  height: 22px;
}

.hamburger-btn:hover {
  background: #37cd7f;
}

/* --- Responsive mobile --- */
@media (max-width: 768px) {
  .dashboard-container {
    grid-template-columns: 1fr;
    grid-template-rows: 60px 1fr auto;
    grid-template-areas:
      "header"
      "main"
      "footer";
    transition: none;
  }

  .dashboard-container.sidebar-collapsed {
    grid-template-columns: 1fr;
  }

  .hamburger-btn {
    display: flex;
  }

  .header-area {
    padding-left: 4rem;
  }
}
</style>