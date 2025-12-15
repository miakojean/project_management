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
        <button class="action-btn" @click="handleDelete" title="Supprimer">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
          </svg>
        </button>
        
        <button class="action-btn" @click="handleDownload" title="Télécharger">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
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

      <div class="comment_content w-full flex justify-items-normal gap-3">
        <div class="w-1/3 flex justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 text-gray-400">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z" />
          </svg>
        </div>
        
        <div class="w-2/3">
          <p class="text-gray-500 text-sm leading-relaxed">
            {{ description }}
          </p>
        </div>
      </div>
    </div>
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
    },

    description:{
      type: String,
      default:"Lorem ipsum dolor sit amet consectetur adipisicing elit. Laboriosam quisquam maxime at sapiente aliquam quibusdam!"
    }
  },
  
  // Événements émis vers le parent
  emits: ['delete', 'download',],
  
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

    handleDelete(){
      this.$emit("delete"),
      console.log("Evènement de suppression émis!!!")
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