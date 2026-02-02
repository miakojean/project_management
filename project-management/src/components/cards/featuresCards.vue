<template>
  <div class="feature-card" :class="{ 'feature-card--hover': hoverAnimation }">
    <!-- Icon container with gradient background -->
    <div class="card-icon" :style="iconGradient">
      <slot name="icon">
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke-width="1.5" 
          stroke="currentColor" 
          class="size-6"
        >
          <path 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" 
          />
        </svg>
      </slot>
    </div>

    <!-- Content -->
    <div class="card-content">
      <h3 class="card-title">{{ title }}</h3>
      <p class="card-description">{{ description }}</p>
    </div>

    <!-- Optional decorative element -->
    <div v-if="showDecoration" class="card-decoration"></div>
    
    <!-- Optional badge -->
    <span v-if="badge" class="card-badge">
      {{ badge }}
    </span>
  </div>
</template>

<script>
export default {
  name: 'FeatureCard',
  props: {
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    // Icon customization
    iconColor: {
      type: String,
      default: 'primary' // primary, secondary, custom
    },
    iconGradient: {
      type: Object,
      default: () => ({
        background: 'linear-gradient(135deg, #0081C6 0%, #005380 100%)'
      })
    },
    // Visual options
    hoverAnimation: {
      type: Boolean,
      default: true
    },
    showDecoration: {
      type: Boolean,
      default: true
    },
    badge: {
      type: String,
      default: null
    },
    cardWidth: {
      type: String,
      default: '320px'
    }
  },
  computed: {
    iconClass() {
      const colors = {
        primary: 'icon-primary',
        secondary: 'icon-secondary',
        success: 'icon-success',
        warning: 'icon-warning',
        danger: 'icon-danger'
      };
      return colors[this.iconColor] || colors.primary;
    }
  }
};
</script>

<style scoped>
.feature-card {
  position: relative;
  background: white;
  border-radius: 16px;
  padding: 32px 24px;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  justify-content: start;
  gap: 24px;
  width: 100%;
  border: 1px solid rgba(99, 102, 241, 0.1);
  overflow: hidden;
}

.feature-card--hover:hover {
  transform: translateY(-8px);
  box-shadow: 
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: rgba(99, 102, 241, 0.2);
}

.card-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 20px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  padding: 20px;
  z-index: 2;
}

.card-icon svg {
  width: 32px;
  height: 32px;
  stroke: white;
  stroke-width: 1.5;
}

.card-content {
  text-align: center;
  z-index: 2;
}

.card-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 12px 0;
  line-height: 1.3;
}

.card-description {
  text-align: start;
  font-size: 15px;
  color: #6b7280;
  line-height: 1.6;
  margin: 0;
}

.card-decoration {
  position: absolute;
  top: 0;
  right: 0;
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
  border-radius: 0 16px 0 100px;
  z-index: 1;
}

.card-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  color: white;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
  z-index: 3;
}

/* Icon color variations */
.icon-primary {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
}

.icon-secondary {
  background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
}

.icon-success {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
}

.icon-warning {
  background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
}

.icon-danger {
  background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
}

/* Responsive */
@media (max-width: 768px) {
  .feature-card {
    padding: 24px 20px;
    gap: 20px;
    max-width: 280px;
  }

  .card-icon {
    width: 70px;
    height: 70px;
    padding: 16px;
    border-radius: 16px;
  }

  .card-icon svg {
    width: 32px;
    height: 32px;
  }

  .card-title {
    font-size: 18px;
  }

  .card-description {
    font-size: 14px;
  }

  .card-decoration {
    width: 100px;
    height: 100px;
  }
}

@media (max-width: 480px) {
  .feature-card {
    display: flex;
    justify-content: start;
    max-width: 380px;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .feature-card {
    background: #1f2937;
    border-color: rgba(99, 102, 241, 0.2);
  }

  .card-title {
    color: #f9fafb;
  }

  .card-description {
    color: #d1d5db;
  }

  .card-decoration {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
  }
}

/* Animation for card entrance */
@keyframes cardEntrance {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feature-card {
  animation: cardEntrance 0.6s ease-out;
}
</style>