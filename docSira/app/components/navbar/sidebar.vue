<template>
  <aside class="sidebar" :class="{ 'is-reduced': isReduced }">
    <!-- LOGO -->
    <div class="logo hidden-mobile">
      <!-- Icône affichée lorsque la sidebar est réduite -->

      <!-- Texte affiché lorsque la sidebar est ouverte -->
      <span class="logo-text" v-if="!isReduced">DocSira</span>

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
        :class="{ active: route.path.includes('/Dashboard/index/ ') }"
        @click="router.push('/Dashboard')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Dashboard</span>
      </button>

      <button 
        class="nav-item"
        :class="{ active: route.path.includes('/dashboard/affairs') }"
        @click="router.push('/dashboard/affairs')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44l-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44z" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Affaires</span>
      </button>

      <button 
        class="nav-item"
        :class="{ active: route.path.includes('/dashboard/Customer') }"
        @click="router.push('/dashboard/Customer')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Clients</span>
      </button>

      <button 
        class="nav-item"
        :class="{ active: route.path.includes('/dashboard/Archives') }"
        @click="router.push('/dashboard/Archives')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 3.75H6.912a2.25 2.25 0 0 0-2.15 1.588L2.35 13.177a2.25 2.25 0 0 0-.1.661V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 0 0-2.15-1.588H15M2.25 13.5h3.86a2.25 2.25 0 0 1 2.012 1.244l.256.512a2.25 2.25 0 0 0 2.013 1.244h3.218a2.25 2.25 0 0 0 2.013-1.244l.256-.512a2.25 2.25 0 0 1 2.013-1.244h3.859M12 3v8.25m0 0-3-3m3 3 3-3" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Archives</span>
      </button>

      <button 
        class="nav-item"
        :class="{ active: route.path.includes('/profile/Support') }"
        @click="router.push('/profile/Support')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17 17.25 21A2.652 2.652 0 0 0 21 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 1 1-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 0 0 4.486-6.336l-3.276 3.277a3.004 3.004 0 0 1-2.25-2.25l3.276-3.276a4.5 4.5 0 0 0-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437 1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008Z" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Support client</span>
      </button>

      <button 
        class="nav-item"
        :class="{ active: route.path.includes('/profile/Settings') }"
        @click="router.push('/profile/Settings')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 0 1 1.45.12l.773.774c.39.389.44 1.002.12 1.45l-.527.737c-.25.35-.272.806-.107 1.204.165.397.505.71.93.78l.893.15c.543.09.94.559.94 1.109v1.094c0 .55-.397 1.02-.94 1.11l-.894.149c-.424.07-.764.383-.929.78-.165.398-.143.854.107 1.204l.527.738c.32.447.269 1.06-.12 1.45l-.774.773a1.125 1.125 0 0 1-1.449.12l-.738-.527c-.35-.25-.806-.272-1.203-.107-.398.165-.71.505-.781.929l-.149.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527c-.447.32-1.06.269-1.45-.12l-.773-.774a1.125 1.125 0 0 1-.12-1.45l.527-.737c.25-.35.272-.806.108-1.204-.165-.397-.506-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.109v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.143-.854-.108-1.204l-.526-.738a1.125 1.125 0 0 1 .12-1.45l.773-.773a1.125 1.125 0 0 1 1.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.929l.15-.894Z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
        </svg>

        <span class="nav-label" v-if="!isReduced">Paramètres</span>
      </button>
    </nav>

    <!-- DÉCONNEXION 
    <div class="logout">
      <button class="nav-item" @click="authStore.logout">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Déconnexion</span>
      </button>
    </div> -->
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
  --sb-bg: #fcfcfb;
  --sb-text: #000e2d;
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
  color: var(--primary-color);
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
  font-weight: 600;
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

  .logo svg{
    color: var(--primary-color);
  }

  .sidebar.is-reduced .logo {
    justify-content: center;
    padding: 0;
    gap: 0.5rem;
  }
  .logo-text {
    font-weight: 700;
    font-size: 1.25rem;
    color: var(--primary-color);
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
    color: var(--primary-color);
    cursor: pointer;
    transition: color 0.2s ease;
  }
  
  .toggle-icon:hover {
    color: var(--primary-color);
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
    border-radius: 8px;
    font-size: 0.8rem;
  }
  .nav-item:hover {
    background-color: var(--primary-color);
    color: #ffffff;
  }
  .nav-item.active {
    background-color: var(--primary-color);
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