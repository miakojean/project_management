<template>
  <nav>
    <h4>DocSira</h4>
    <profileButton class="profile-btn" />
  </nav>
</template>

<script>
import profileButton from '../buttons/profileButton.vue'
export default {
  components: { profileButton }
}
</script>

<style scoped>
nav {
  position: fixed;
  top: 5px;
  right: 5px;
  /* les deux width: 100% sont en double, on garde une seule */
  width: 100%;
  max-width: 1024px;
  display: flex;
  align-items: center;
  padding: 1rem;
  /* on enlève justify-content: space-between */
}

nav h4 {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--primary-color);
  margin: 0; /* pour éviter un décalage */
}

.profile-btn {
  margin-left: auto; /* clé : pousse le bouton à droite */
}

@media (min-width: 1024px) {
  nav h4 {
    display: none; /* logo caché sur PC */
  }
}
</style>