<template>
  <main>
    <div class="content-container">
      <loginForm/>
    </div>

    <div class="svg-pattern">
      <div 
        v-for="(icon, index) in icons" 
        :key="index" 
        class="svg-icon"
        :style="icon.style"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
        </svg>
      </div>
    </div>
  </main>
</template>

<script>
import registrationForm from '@/components/forms/registrationForm.vue';
import loginForm from '@/components/forms/loginForm.vue';

export default {
  components: {
    registrationForm,
    loginForm
  },
  data() {
    return {
      icons: []
    };
  },
  mounted() {
    // Génération de 50 icônes avec positions et vitesses aléatoires
    this.icons = Array.from({ length: 50 }, () => ({
      style: {
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 5}s`,
        animationDuration: `${6 + Math.random() * 4}s`, // Entre 6 et 10 secondes
        opacity: 0.05 + Math.random() * 0.1 // Opacité variable pour effet de profondeur
      }
    }));
  }
}
</script>

<style scoped>
main {
  position: relative;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: #f8f9fa; /* Fond gris très clair */
}

/* CONTENEUR DU FORMULAIRE */
.content-container {
  position: relative;
  z-index: 10; /* IMPORTANT: Au-dessus des icônes */
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* CONTENEUR DU FOND */
.svg-pattern {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1; /* En dessous du formulaire */
  pointer-events: none; /* S'assure que les clics passent à travers si jamais */
}

/* STYLE DE L'ICONE */
.svg-icon {
  position: absolute;
  width: 40px; /* Taille du dossier */
  height: 40px;
  color: #2f80ed; /* Bleu (tu peux changer ici) */
  animation-name: float;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-15px) rotate(5deg);
  }
}
</style>