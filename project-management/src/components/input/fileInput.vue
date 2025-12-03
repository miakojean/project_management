<template>
  <div class="file-uploader">
    <!-- Zone de dépôt -->
    <div 
      class="drop-zone"
      :class="{ 'drag-over': isDragOver, 'has-files': files.length > 0 }"
      @drop="onDrop"
      @dragover.prevent="isDragOver = true"
      @dragleave="isDragOver = false"
      @dragenter.prevent
    >
      <!-- Prompt initial -->
      <div v-if="files.length === 0" class="upload-prompt">
        <div class="upload-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
        </div>
        <h3>Déposez vos fichiers ici</h3>
        <p>ou</p>
        <button class="browse-btn" type="button" @click="triggerFileInput">
          Parcourir les fichiers
        </button>
        <p class="file-info">
          Formats acceptés : {{ allowedExtensions.join(', ') }}<br>
          Taille max : {{ maxFileSizeMB }}MB par fichier
        </p>
      </div>

      <!-- Liste des fichiers -->
      <div v-else class="files-list">
        <h3>Fichiers sélectionnés ({{ files.length }})</h3>
        
        <div class="files-container">
          <div 
            v-for="(fileItem, index) in files" 
            :key="index"
            class="file-item"
          >
            <div class="file-info-row">
              <div class="file-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
                  <polyline points="13 2 13 9 20 9"/>
                </svg>
              </div>
              <div class="file-details">
                <span class="file-name">{{ fileItem.name }}</span>
                <span class="file-size">{{ formatFileSize(fileItem.size) }}</span>
              </div>
              <button 
                class="remove-btn"
                @click="removeFile(index)"
                type="button"
                title="Supprimer"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <div class="upload-actions">
          <button 
            class="add-more-btn" 
            type="button"
            @click="triggerFileInput"
          >
            Ajouter d'autres fichiers
          </button>
        </div>
      </div>
    </div>

    <!-- Input caché -->
    <input
      ref="fileInput"
      type="file"
      multiple
      :accept="acceptAttribute"
      @change="onFileSelect"
      style="display: none"
    />

    <!-- Message d'erreur -->
    <div v-if="errorMessage" class="error-banner">
      <span>{{ errorMessage }}</span>
      <button @click="errorMessage = ''" type="button">×</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FileInput',
  props: {
    maxFileSizeMB: {
      type: Number,
      default: 10
    },
    allowedExtensions: {
      type: Array,
      default: () => ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.xls', '.xlsx']
    },
    maxFiles: {
      type: Number,
      default: 10
    },
    modelValue: {
      type: Array,
      default: () => []
    }
  },
  emits: ['update:modelValue', 'error'],
  data() {
    return {
      files: [],
      isDragOver: false,
      errorMessage: ''
    }
  },
  computed: {
    acceptAttribute() {
      return this.allowedExtensions.join(',');
    }
  },
  watch: {
    files: {
      handler(newFiles) {
        // Émettre les fichiers bruts au parent
        const rawFiles = newFiles.map(item => item.file);
        this.$emit('update:modelValue', rawFiles);
      },
      deep: true
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    onFileSelect(event) {
      const selectedFiles = Array.from(event.target.files);
      this.processFiles(selectedFiles);
      event.target.value = ''; // Reset input
    },

    onDrop(event) {
      event.preventDefault();
      this.isDragOver = false;
      const droppedFiles = Array.from(event.dataTransfer.files);
      this.processFiles(droppedFiles);
    },

    processFiles(fileList) {
      // Vérifier le nombre max de fichiers
      const remainingSlots = this.maxFiles - this.files.length;
      
      if (remainingSlots <= 0) {
        this.showError(`Nombre maximum de fichiers (${this.maxFiles}) atteint.`);
        return;
      }

      const filesToAdd = fileList.slice(0, remainingSlots);
      let addedCount = 0;

      filesToAdd.forEach(file => {
        // Validation de la taille
        if (file.size > this.maxFileSizeMB * 1024 * 1024) {
          this.showError(`"${file.name}" dépasse ${this.maxFileSizeMB}MB`);
          return;
        }

        // Validation de l'extension
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        if (!this.allowedExtensions.includes(fileExtension)) {
          this.showError(`Format "${fileExtension}" non autorisé pour "${file.name}"`);
          return;
        }

        // Vérifier les doublons
        const isDuplicate = this.files.some(f => 
          f.name === file.name && f.size === file.size
        );
        
        if (isDuplicate) {
          this.showError(`"${file.name}" est déjà ajouté`);
          return;
        }

        // Ajouter le fichier
        this.files.push({
          file: file,
          name: file.name,
          size: file.size,
          type: file.type
        });
        addedCount++;
      });

      if (fileList.length > remainingSlots) {
        this.showError(`${fileList.length - remainingSlots} fichier(s) ignoré(s) (limite: ${this.maxFiles})`);
      }
    },

    removeFile(index) {
      this.files.splice(index, 1);
    },

    showError(message) {
      this.errorMessage = message;
      this.$emit('error', message);
      
      // Auto-clear après 5 secondes
      setTimeout(() => {
        this.errorMessage = '';
      }, 5000);
    },

    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    // Méthode publique pour réinitialiser
    reset() {
      this.files = [];
      this.errorMessage = '';
    },

    // Méthode publique pour obtenir les fichiers
    getFiles() {
      return this.files.map(item => item.file);
    }
  }
}
</script>

<style scoped>
.file-uploader {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.drop-zone {
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  background: #f9fafb;
  width: 100%;
  box-sizing: border-box;
}

.drop-zone.drag-over {
  border-color: #3b82f6;
  background-color: #eff6ff;
}

.drop-zone.has-files {
  border-style: solid;
  border-color: #e5e7eb;
  background: white;
}

.upload-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  gap: 0.75rem;
}

.upload-icon {
  color: #9ca3af;
  display: flex;
  justify-content: center;
}

.upload-prompt h3 {
  margin: 0;
  color: #374151;
  font-weight: 600;
  font-size: 1.2rem;
  text-align: center;
}

.upload-prompt p {
  color: #6b7280;
  margin: 0;
}

.browse-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

.browse-btn:hover {
  background: #2563eb;
}

.file-info {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.5rem;
}

.files-list {
  width: 100%;
}

.files-list h3 {
  margin: 0 0 1rem 0;
  color: #374151;
  font-weight: 600;
  font-size: 1.1rem;
  text-align: left;
}

.files-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.file-item {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s;
}

.file-item:hover {
  border-color: #d1d5db;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.file-info-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.file-icon {
  color: #6b7280;
  flex-shrink: 0;
}

.file-details {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.file-name {
  font-weight: 500;
  color: #374151;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-size {
  font-size: 0.875rem;
  color: #6b7280;
}

.remove-btn {
  padding: 0.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
  background: #fef2f2;
  color: #ef4444;
  flex-shrink: 0;
}

.remove-btn:hover {
  background: #fecaca;
}

.upload-actions {
  display: flex;
  justify-content: center;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.add-more-btn {
  background: transparent;
  color: #3b82f6;
  border: 1px solid #3b82f6;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.add-more-btn:hover {
  background: #eff6ff;
}

.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #dc2626;
  font-weight: 500;
}

.error-banner button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #dc2626;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.error-banner button:hover {
  background-color: #fecaca;
}

@media (max-width: 600px) {
  .drop-zone {
    padding: 1.5rem 1rem;
  }
  
  .file-name {
    font-size: 0.9rem;
  }
}
</style>