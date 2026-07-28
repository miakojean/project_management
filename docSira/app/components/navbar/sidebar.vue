<template>
  <aside class="sidebar" :class="{ 'is-reduced': isReduced }">
    <!-- LOGO -->
    <div class="logo hidden-mobile">
      <!-- Icône affichée lorsque la sidebar est réduite -->
      <svg 
        v-if="isReduced" 
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke-width="1.5" 
        stroke="currentColor" 
        class="logo-icon"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 21v-8.25M15.75 21v-8.25M8.25 21v-8.25M3 9l9-6 9 6m-1.5 12V10.332A48.36 48.36 0 0012 9.75c-2.551 0-5.056.2-7.5.582V21M3 21h18M12 6.75h.008v.008H12V6.75z" />
      </svg>

      <!-- Texte affiché lorsque la sidebar est ouverte -->
      <span class="logo-text" v-else>DocSira</span>

      <!-- Bouton de bascule (toujours visible) -->
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke-width="1.5" 
        stroke="currentColor" 
        class="toggle-icon" 
        @click="toggleReduce"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z" />
      </svg>
    </div>

    <!-- NAVIGATION -->
    <nav class="nav-menu">
      <button 
        class="nav-item" 
        :class="{ active: route.path.includes('/profile/Dashboard') }"
        @click="router.push('/profile/Dashboard')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Dashboard</span>
      </button>

      <button 
        class="nav-item"
        :class="{ active: route.path.includes('/profile/Contract') }"
        @click="router.push('/profile/Contract')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44l-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44z" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Affaires</span>
      </button>

      <button 
        class="nav-item"
        :class="{ active: route.path.includes('/profile/CustomContract') }"
        @click="router.push('/profile/CustomContract')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m3.75 9v6m3-3H9m1.5-12H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Clients</span>
      </button>

      <button 
        class="nav-item"
        :class="{ active: route.path.includes('/profile/Experts') }"
        @click="router.push('/profile/Experts')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 21v-8.25M15.75 21v-8.25M8.25 21v-8.25M3 9l9-6 9 6m-1.5 12V10.332A48.36 48.36 0 0012 9.75c-2.551 0-5.056.2-7.5.582V21M3 21h18M12 6.75h.008v.008H12V6.75z" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Experts</span>
      </button>

      <button 
        class="nav-item"
        :class="{ active: route.path.includes('/profile/Support') }"
        @click="router.push('/profile/Support')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Support client</span>
      </button>

      <button 
        class="nav-item"
        :class="{ active: route.path.includes('/profile/Settings') }"
        @click="router.push('/profile/Settings')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.43l-1.003.767c-.3.23-.452.617-.432.998.003.074.005.147.005.22s-.002.146-.005.22c-.02.381.13.768.432.998l1.003.767a1.125 1.125 0 0 1 .26 1.43l-1.296 2.247a1.125 1.125 0 0 1-1.37.49l-1.216-.456c-.356-.133-.751-.072-1.076.124a6.57 6.57 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.43l1.004-.767c.301-.23.452-.617.432-.998-.003-.074-.005-.147-.005-.22s.002-.146.005-.22c.02-.381-.13-.768-.432-.998L2.26 9.17a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.49l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.28Z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Paramètres</span>
      </button>
    </nav>

    <!-- DÉCONNEXION -->
    <div class="logout">
      <button class="nav-item" @click="authStore.logout">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Déconnexion</span>
      </button>
    </div>
  </aside>
</template>

<script lang="ts">
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';


export default {
  name: 'Sidebar',
  setup() {
    const isReduced = ref(false);
    const router = useRouter();
    const route = useRoute();

    const toggleReduce = () => {
      isReduced.value = !isReduced.value;
    };

    return { 
      isReduced, 
      router,
      route,
      toggleReduce
    };
  }
}
</script>

<style scoped>
.sidebar {
  --sb-bg: #000e2ddd;
  --sb-text: #ffffff;
  --sb-text-active: #ffffff;
  --sb-accent: #5452f4;
  --sb-border: rgba(255, 255, 255, 0.08);
  --sb-hover-bg: #000e2d44;
}

.sidebar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: calc(65px + env(safe-area-inset-bottom));
  background-color: var(--sb-bg);
  border-top: 1px solid var(--sb-border);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding-bottom: env(safe-area-inset-bottom);
  z-index: 100;
  box-shadow: 0 -4px 20px rgba(15, 23, 42, 0.1);
}

.nav-menu {
  display: flex;
  width: 100%;
  justify-content: flex-start;
  align-items: center;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  gap: 0.5rem;
  padding: 0 1rem;
  scrollbar-width: none;
}
.nav-menu::-webkit-scrollbar {
  display: none;
}

.nav-item {
  background: none;
  border: none;
  color: var(--sb-text);
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
  width: 100px;
  min-height: 50px;
  font-size: 0.5rem;
  font-weight: 500;
  transition: all 0.2s ease;
  text-decoration: none;
}
.icon {
  width: 24px;
  height: 24px;
  margin-bottom: 0.2rem;
  transition: transform 0.2s ease;
}
.nav-item.active {
  color: var(--sb-accent);
}
.nav-item.active .icon {
  transform: translateY(-2px);
}
.nav-item:hover:not(.active) {
  color: var(--sb-text-active);
}

.hidden-mobile {
  display: none;
}
.logout span {
  color: #ef4444;
}
.logout .nav-item {
  color: #ef4444;
}

/* --- DESKTOP --- */
@media (min-width: 1024px) {
  .hidden-mobile {
    display: flex;
  }

  .sidebar {
    position: relative;
    bottom: auto;
    left: auto;
    width: 260px;
    height: 100vh;
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
    padding: 1rem 1rem;
    border-top: none;
    border-right: 1px solid var(--sb-border);
    box-shadow: none;
    gap: 1rem;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .sidebar.is-reduced {
    width: 88px;
    padding: 1.5rem 0.5rem;
  }

  .logo {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0.5rem;
  }
  .sidebar.is-reduced .logo {
    justify-content: center;
    padding: 0;
    gap: 0.5rem;
  }
  .logo-text {
    font-weight: 700;
    font-size: 1.25rem;
    color: var(--secondary-light-color, #fff);
    letter-spacing: -0.02em;
    margin: 1rem;
  }
  .logo-icon {
    width: 32px;
    height: 32px;
    color: var(--sb-text);
    flex-shrink: 0;
  }
  .toggle-icon {
    width: 28px;
    height: 28px;
    color: var(--sb-text);
    cursor: pointer;
    transition: color 0.2s ease;
  }
  .toggle-icon:hover {
    color: var(--sb-accent);
  }

  .nav-menu {
    flex-direction: column;
    width: 100%;
    gap: 0.5rem;
  }

  .nav-item {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    gap: 1rem;
    padding: 0.5rem;
    border-radius: 12px;
    font-size: 0.8rem;
  }
  .nav-item:hover {
    background-color: rgba(53, 95, 203, 0.932);
    color: #ffffff;
  }
  .nav-item.active {
    background-color: rgba(53, 95, 203, 0.932);
    color: #ffffff;
  }
  .nav-item.active .icon {
    transform: none;
  }
  .sidebar.is-reduced .nav-item {
    justify-content: center;
    padding: 0.8rem 0;
  }
  .nav-label {
    white-space: nowrap;
    animation: fadeIn 0.2s ease forwards;
  }

  .logout {
    margin-top: auto;
    width: 100%;
    border-top: 1px solid var(--sb-border);
    padding-top: 1rem;
  }
  .logout .nav-item:hover {
    background-color: rgba(239, 68, 68, 0.1);
    color: #ef4444;
  }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateX(-5px); }
  to { opacity: 1; transform: translateX(0); }
}
</style>