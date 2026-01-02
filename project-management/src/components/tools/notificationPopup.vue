<template>
  <!-- Overlay: capture clicks outside the popup to close it -->
  <transition name="notification-slide">
    <div v-if="visible" class="notification-overlay" @click="close">
      <div class="notification-popup" :class="type" @click.stop>
        <div class="notification-content">
          <div class="notification-text">
            <p class="notification-message">{{ message }}</p>
          </div>
          <button class="notification-close" @click="close" aria-label="Fermer la notification">
            x
          </button>
        </div>
        <div class="progress-bar">
          <div 
            class="progress-fill" 
            :class="type"
            :style="{ width: progress + '%' }"
          ></div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { ref, onMounted, watch, onUnmounted } from 'vue'

export default {
  name: 'NotificationPopup',
  props: {
    message: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'success',
      validator: (value) => ['success', 'error', 'info'].includes(value)
    },
    duration: {
      type: Number,
      default: 3000
    },
    visible: {
      type: Boolean,
      default: true
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const progress = ref(100)
    let progressInterval = null
    let startTime = null
    // Clamp total duration to a maximum of 3000ms
    const totalDuration = Math.min(props.duration || 3000, 3000)

    const close = () => {
      if (progressInterval) {
        clearInterval(progressInterval)
        progressInterval = null
      }
      emit('close')
    }

    const startProgress = () => {
      progress.value = 100
      startTime = Date.now()
      
      progressInterval = setInterval(() => {
        const elapsed = Date.now() - startTime
        const remaining = Math.max(0, totalDuration - elapsed)
        progress.value = (remaining / totalDuration) * 100
        
        if (remaining <= 0) {
          close()
        }
      }, 50)
    }

    onMounted(() => {
      if (props.visible) {
        startProgress()
      }
    })

    watch(() => props.visible, (newVal) => {
      if (newVal) {
        startProgress()
      } else {
        if (progressInterval) {
          clearInterval(progressInterval)
          progressInterval = null
        }
      }
    })

    onUnmounted(() => {
      if (progressInterval) {
        clearInterval(progressInterval)
      }
    })

    return {
      progress,
      close
    }
  }
}
</script>

<style scoped>
.notification-popup {
  position: fixed;
  bottom: 20px;
  left: 20px;
  width: 380px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
}

/* Full-screen overlay to detect outside clicks */
.notification-overlay {
  position: fixed;
  inset: 0; /* top:0; right:0; bottom:0; left:0 */
  background: transparent;
  z-index: 999; /* below the popup but above page content */
  display: flex;
  align-items: flex-end; /* keep popup at bottom */
}

.notification-popup.success {
  border-left: 4px solid #10b981;
  background: linear-gradient(135deg, #b2e8c2, #ffffff);
}

.notification-popup.error {
  border-left: 4px solid #ef4444;
  background: linear-gradient(135deg, #fef2f2, #ffffff);
}

.notification-popup.info {
  border-left: 4px solid #3b82f6;
  background: linear-gradient(135deg, #eff6ff, #ffffff);
}

.notification-content {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  gap: 12px;
}

.notification-icon {
  font-size: 20px;
  flex-shrink: 0;
  margin-top: 2px;
}

.notification-text {
  flex: 1;
}

.notification-message {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  color: #374151;
  font-weight: 500;
}

.notification-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #9ca3af;
  padding: 4px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.notification-close:hover {
  background-color: #f3f4f6;
  color: #374151;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background-color: #f3f4f6;
  position: relative;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width 0.05s linear;
  border-radius: 0 2px 2px 0;
}

.progress-fill.success {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.progress-fill.error {
  background: linear-gradient(90deg, #ef4444, #f87171);
}

.progress-fill.info {
  background: linear-gradient(90deg, #3b82f6, #60a5fa);
}

/* Animations */
.notification-slide-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.notification-slide-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 1, 1);
}

.notification-slide-enter-from {
  transform: translateX(-100%);
  opacity: 0;
}

.notification-slide-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

/* Responsive */
@media (max-width: 480px) {
  .notification-popup {
    width: calc(100% - 40px);
    left: 20px;
    right: 20px;
    bottom: 20px;
  }
  
  .notification-content {
    padding: 14px;
  }
  
  .notification-message {
    font-size: 13px;
  }
}
</style>