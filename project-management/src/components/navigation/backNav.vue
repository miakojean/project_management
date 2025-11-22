<template>
  <div class="nav__section">
    <button 
      class="nav__btn flex items-center justify-center gap-3"
      @click="handleGoBack"
      :disabled="isGoingBack"
    >
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke-width="2" 
        stroke="currentColor" 
        class="nav__icon"
        :class="{ 'nav__icon--animated': isGoingBack }"
      >
        <path 
          stroke-linecap="round" 
          stroke-linejoin="round" 
          d="M6.75 15.75 3 12m0 0 3.75-3.75M3 12h18" 
        />
      </svg>
      <span class="nav__text">{{ isGoingBack ? 'Retour...' : 'Retour' }}</span>
    </button>
  </div>
</template>

<script>
export default {
  name: 'BackButton',
  data() {
    return {
      isGoingBack: false
    }
  },
  methods: {
    handleGoBack() {
      this.isGoingBack = true;
      
      // Utilise Vue Router pour revenir en arrière
      if (this.$router) {
        this.$router.go(-1);
      } else {
        // Fallback: retour navigateur natif
        window.history.back();
      }
      
      // Réinitialiser l'état après un délai
      setTimeout(() => {
        this.isGoingBack = false;
      }, 1000);
    }
  }
}
</script>

<style scoped>
.nav__section {
  width: 100%;
  padding: 1rem;
}

.nav__btn {
  width: 100%;
  max-width: 200px;
  padding: 0.8rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  position: relative;
  overflow: hidden;
}

.nav__btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
}

.nav__btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.nav__btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

.nav__btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.nav__btn:hover::before {
  left: 100%;
}

.nav__icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s ease;
}

.nav__btn:hover .nav__icon {
  transform: translateX(-2px);
}

.nav__icon--animated {
  animation: bounceLeft 0.6s ease infinite;
}

.nav__text {
  font-size: 0.95rem;
  font-weight: 600;
  letter-spacing: 0.025em;
}

/* Animation pour le loading */
@keyframes bounceLeft {
  0%, 100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(-4px);
  }
}

/* Variantes de style optionnelles */
.nav__btn--outline {
  background: transparent;
  color: #3b82f6;
  border: 2px solid #3b82f6;
  box-shadow: none;
}

.nav__btn--outline:hover {
  background: #3b82f6;
  color: white;
}

.nav__btn--small {
  max-width: 150px;
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
}

.nav__btn--large {
  max-width: 250px;
  padding: 1rem 2rem;
  font-size: 1.1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .nav__section {
    padding: 0.75rem;
  }
  
  .nav__btn {
    max-width: 180px;
    padding: 0.65rem 1.25rem;
    font-size: 0.9rem;
  }
  
  .nav__icon {
    width: 18px;
    height: 18px;
  }
}

@media (max-width: 480px) {
  .nav__btn {
    max-width: 160px;
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
  }
  
  .nav__text {
    font-size: 0.85rem;
  }
}
</style>