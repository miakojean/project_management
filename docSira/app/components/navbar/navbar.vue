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
  position: sticky;
  top: 30px;
  width: 100%;
  /* max-width: 1024px; */
  display: flex;
  align-items: center;
  padding: 1rem;
  z-index: 1000;
  background: none;
}

nav h4 {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--primary-color);
  margin: 0;
}

.profile-btn {
  margin-left: auto;
}

@media (min-width: 1024px) {
  nav h4 {
    display: none;
  }
}
</style>