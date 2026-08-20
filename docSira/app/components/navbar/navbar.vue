<template>
  <nav>
    <ul class="breadcrumbs">
      <li>
        <router-link to="">Accueil</router-link>
        <span v-if="breadcrumbs.length" class="separator"> > </span>
      </li>

      <li v-for="(crumb, index) in breadcrumbs" :key="index">
        <router-link
          v-if="index < breadcrumbs.length - 1"
          :to="crumb.path"
        >
          {{ crumb.label }}
        </router-link>

        <span v-else class="current-page">{{ crumb.label }}</span>

        <span v-if="index < breadcrumbs.length - 1" class="separator"> > </span>
      </li>
    </ul>

  </nav>
</template>

<script>
import profileButton from '../buttons/profileButton.vue'
import { useRoute } from 'vue-router'
import { computed } from 'vue' // 💡 N'oublie pas d'importer computed

export default {
  components: { profileButton },

  setup() {
    const route = useRoute();

    // 🧠 Création dynamique du fil d'Ariane basée sur l'URL
    const breadcrumbs = computed(() => {
      // 1. On récupère le chemin brut (ex: "/admin/coupons/create")
      // 2. On le découpe et on retire les éléments vides
      const paths = route.path.split('/').filter(p => p);
      let currentPath = '';

      return paths.map((path) => {
        // On reconstruit le chemin étape par étape
        currentPath += `/${path}`;

        // On formate le label (ex: "create-coupon" -> "Create coupon")
        // On met la 1ère lettre en majuscule et on remplace les tirets par des espaces
        const label = path.charAt(0).toUpperCase() + path.slice(1).replace(/-/g, ' ');

        return {
          label: label,
          path: currentPath
        };
      });
    });

    return {
      route,
      breadcrumbs
    }
  }
}
</script>

<style scoped>
nav {
  position: sticky;
  top: 30px;
  width: 100%;
  display: flex;
  align-items: center;
  padding: 1rem;
  z-index: 30;
  background: #e9ebee;
}

/* =========================================
   Styles du Breadcrumb
   ========================================= */
.breadcrumbs {
  list-style: none;
  display: flex;
  align-items: center;
  padding: 0;
  margin: 0;
}

.breadcrumbs li {
  display: flex;
  align-items: center;
  font-size: 1.1rem;
}

.breadcrumbs a {
  text-decoration: none;
  color: #64748b; /* Gris doux pour les liens cliquables */
  transition: color 0.2s ease;
}

.breadcrumbs a:hover {
  color: var(--primary-color); /* Met en valeur au survol */
}

.current-page {
  font-weight: 600;
  color: var(--primary-color); /* Met en valeur la page actuelle */
}

.separator {
  margin: 0 0.6rem;
  color: #cbd5e1; /* Gris très clair pour le séparateur */
  font-size: 0.9rem;
}

.profile-btn {
  margin-left: auto;
}

@media (min-width: 1024px) {
  .breadcrumbs li {
    font-size: 1rem;
  }
}
</style>
