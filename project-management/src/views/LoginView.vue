<template>
  <main>

    <simpleNavbar/>

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
          <path stroke-linecap="round" stroke-linejoin="round" :d="icon.path" />
        </svg>
      </div>
    </div>
  </main>
</template>

<script>
import registrationForm from '@/components/forms/registrationForm.vue';
import loginForm from '@/components/forms/loginForm.vue';
import simpleNavbar from '@/components/navigation/simpleNavbar.vue';

export default {
  components: {
    registrationForm,
    loginForm,
    simpleNavbar
  },
  data() {
    return {
      icons: [],
      // Liste des différents chemins SVG (Folder, Cloud Upload, Cloud Download, Document)
      iconPaths: [
        // Folder (Dossier)
        "M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z",
        // Arrow Down Tray (Téléchargement)
        "M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M12 9.75l-3 3m0 0 3 3m-3-3h7.5M9 12.75 12 15.75 15 12.75",
        // Cloud Arrow Up (Upload)
        "M12 16.5V9.75m0 0 3 3m-3-3-3 3M6.75 19.5a4.5 4.5 0 0 1-1.41-8.775 5.25 5.25 0 0 1 10.233-2.33 3 3 0 0 1 3.758 3.848A3.752 3.752 0 0 1 18 19.5H6.75Z",
        // Document Text
        "M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
      ]
    };
  },
  mounted() {
    // Génération de 20 icônes statiques
    this.icons = Array.from({ length: 20 }, () => {
      // Sélection aléatoire d'un type d'icône
      const randomPath = this.iconPaths[Math.floor(Math.random() * this.iconPaths.length)];
      
      return {
        path: randomPath,
        style: {
          left: `${Math.random() * 100}%`,
          top: `${Math.random() * 100}%`,
          // Ajout d'une rotation aléatoire pour l'effet "éparpillé"
          transform: `rotate(${Math.random() * 360}deg)`, 
          opacity: 0.08 + Math.random() * 0.1 // Opacité légère
        }
      };
    });
  }
}
</script>

<style scoped>
main {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background-color: #ffffff;
}

/* CONTENEUR DU FORMULAIRE */
.content-container {
  position: relative;
  z-index: 10; 
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
  z-index: 1; 
  pointer-events: none;
}

/* STYLE DE L'ICONE */
.svg-icon {
  position: absolute;
  width: 45px; /* Légèrement plus grand */
  height: 45px;
  color: #2f80ed;
  /* Plus d'animation ici, juste le positionnement absolu */
}
</style>