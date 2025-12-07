<template>
  <div class="document-card" :style="{ borderLeftColor: computedColor }">
    <!-- En-tête de la carte -->
    <div class="card-header">
      <div class="document-type">
        <div class="type-icon" :style="{ backgroundColor: computedColor + '20' }">
          <span class="type-text">{{ documentTypeText }}</span>
        </div>
      </div>
      
      <div class="card-actions">
        <button class="action-btn" @click="handleView" title="Voir">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
          </svg>
        </button>
        
        <button class="action-btn" @click="handleDownload" title="Télécharger">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
          </svg>
        </button>
        
        <button class="action-btn action-more" @click="handleShare" title="Plus d'options">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM12.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM18.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
            </svg>
        </button>
      </div>
    </div>
    
    <!-- Contenu principal -->
    <div class="card-content">
      <h3 class="document-title">{{ title }}</h3>
      
      <div class="document-meta">
        <span class="meta-item">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
          </svg>
          {{ formattedDate }}
        </span>
        
        <span class="meta-item">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          {{ size }}
        </span>
      </div>
    </div>
    
    <!-- Indicateur de statut 
    <div class="card-status" :class="statusClass">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
        <path v-if="isCompleted" stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
        <path v-else-if="isOverflow" stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
        <path v-else stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
      </svg>
      {{ status }}
    </div> -->
  </div>
</template>

<script>
export default {
  name: 'DocumentCard',
  
  // Props pour recevoir les données du parent
  props: {
    // Informations principales
    title: {
      type: String,
      required: true,
      default: 'Document sans titre'
    },
    
    // Type de document (détermine la couleur)
    documentType: {
      type: String,
      default: 'pdf',
      validator: (value) => ['pdf', 'word', 'excel', 'powerpoint', 'image', 'webd', 'other'].includes(value)
    },
    
    // Couleur personnalisée (optionnelle)
    color: {
      type: String,
      default: ''
    },
    
    // Dates
    lastModified: {
      type: [String, Date],
      default: () => new Date()
    },
    
    // Taille du fichier
    size: {
      type: String,
      default: '0 KB'
    },
    
    // Progression
    progress: {
      type: [Number, String],
      default: 0,
      validator: (value) => {
        const num = Number(value)
        return num >= 0
      }
    },
    
    totalSteps: {
      type: [Number, String],
      default: 10
    },
    
    completedSteps: {
      type: [Number, String],
      default: 0
    },
    
    // Options supplémentaires
    showActions: {
      type: Boolean,
      default: true
    },
    
    showProgress: {
      type: Boolean,
      default: true
    },
    
    status: {
      type: String,
      default: "En cours"
    },
    
    // Événements personnalisés
    customActions: {
      type: Array,
      default: () => []
    }
  },
  
  // Événements émis vers le parent
  emits: ['view', 'download', 'share', 'custom-action'],
  
  // Computed properties
  computed: {
    // Type de document formaté
    documentTypeText() {
      return this.documentType.toUpperCase()
    },
    
    // Couleur calculée selon le type
    computedColor() {
      if (this.color) return this.color
      
      const colorMap = {
        pdf: '#3b82f6',      // Bleu
        word: '#10b981',     // Vert
        excel: '#f59e0b',    // Jaune
        powerpoint: '#ef4444', // Rouge
        image: '#8b5cf6',    // Violet
        webd: '#06b6d4',     // Cyan
        other: '#64748b'     // Gris
      }
      
      return colorMap[this.documentType] || '#3b82f6'
    },
    
    // Date formatée
    formattedDate() {
      if (!this.lastModified) return 'Date inconnue'
      
      try {
        const date = this.lastModified instanceof Date 
          ? this.lastModified 
          : new Date(this.lastModified)
        
        if (isNaN(date.getTime())) return 'Date invalide'
        
        return date.toLocaleDateString('fr-FR', {
          day: 'numeric',
          month: 'short',
          year: 'numeric'
        })
      } catch (e) {
        return 'Date invalide'
      }
    },
    
  },
  
  // Méthodes
  methods: {
    handleView() {
      console.log('Voir document:', this.title)
      this.$emit('view', {
        title: this.title,
        type: this.documentType,
        lastModified: this.lastModified,
        progress: this.progress
      })
    },
    
    handleDownload() {
      console.log('Télécharger document:', this.title)
      this.$emit('download', {
        title: this.title,
        type: this.documentType,
        size: this.size
      })
    },
    
    handleShare() {
      console.log('Partager document:', this.title)
      this.$emit('share', {
        title: this.title,
        type: this.documentType
      })
    },
    
    handleCustomAction(action) {
      console.log('Action personnalisée:', action, this.title)
      this.$emit('custom-action', {
        action: action,
        document: {
          title: this.title,
          type: this.documentType,
          progress: this.progress
        }
      })
    },
    
    // Méthode utilitaire pour formater la taille
    formatFileSize(bytes) {
      if (typeof this.size === 'string') return this.size
      
      if (!bytes || isNaN(bytes)) return 'Taille inconnue'
      
      const sizes = ['octets', 'Ko', 'Mo', 'Go', 'To']
      if (bytes === 0) return '0 octet'
      
      const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)))
      return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i]
    }
  },
  
  // Hooks de cycle de vie
  mounted() {
    console.log('DocumentCard monté:', this.title)
    
    // Validation des props
    if (this.progress < 0) {
      console.warn('La progression ne peut pas être négative:', this.progress)
    }
    
    if (Number(this.completedSteps) > Number(this.totalSteps)) {
      console.warn('Le nombre de steps complétés dépasse le total:', this.completedSteps, '/', this.totalSteps)
    }
  },
  
  // Données locales
  data() {
    return {
      // Données locales si nécessaire
      isHovered: false,
      localProgress: Number(this.progress)
    }
  },
  
  // Watchers
  watch: {
    progress(newVal) {
      this.localProgress = Number(newVal)
      console.log('Progression mise à jour:', this.localProgress)
    },
    
    title(newVal) {
      console.log('Titre mis à jour:', newVal)
    }
  }
}
</script>

<style scoped>
.document-card {
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  border-left: 4px solid;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  cursor: pointer;
  min-width: 300px;
  margin: 20px auto;
}

.document-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.type-icon {
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  display: inline-block;
}

.type-text {
  font-size: 0.75rem;
  font-weight: 600;
  color: inherit;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #f8fafc;
  color: #3b82f6;
  border-color: #cbd5e1;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

/* Content */
.card-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.document-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.document-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.75rem;
  color: #64748b;
}

.meta-item svg {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

/* Progress */
.card-progress {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.progress-label {
  font-size: 0.875rem;
  color: #64748b;
}

.progress-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #0f172a;
}

.progress-bar {
  height: 6px;
  background: #f1f5f9;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-stats {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.progress-percentage {
  font-size: 0.875rem;
  font-weight: 600;
  color: #0f172a;
}

.progress-overflow {
  font-size: 0.75rem;
  color: #ef4444;
  font-weight: 500;
}

/* Status */
.card-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
}

.card-status svg {
  width: 14px;
  height: 14px;
}

.status-completed {
  background: #dcfce7;
  color: #166534;
}

.status-pending {
  background: #fef3c7;
  color: #92400e;
}

.status-overflow {
  background: #fee2e2;
  color: #991b1b;
}

/* Responsive */
@media (max-width: 640px) {
  .document-card {
    padding: 1rem;
    max-width: 100%;
  }
  
  .card-actions {
    flex-direction: row;
  }
}

/* Animation pour la progression */
@keyframes progressPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

.progress-fill.animated {
  animation: progressPulse 2s infinite;
}
</style>