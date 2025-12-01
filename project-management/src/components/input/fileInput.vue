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
      <!-- État initial -->
      <div v-if="files.length === 0" class="upload-prompt">
        <div class="upload-icon center__flex">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
        </div>
        <h3 class="">Déposez fichiers ici</h3>
        <p>ou</p>
        <button class="browse-btn" @click="triggerFileInput">
          Parcourir les fichiers
        </button>
        <p class="file-info">
          Formats acceptés : {{ allowedExtensions.join(', ') }}<br>
          Taille max : {{ maxFileSizeMB }}MB par fichier
        </p>
      </div>

      <!-- Liste des fichiers sélectionnés -->
      <div v-else class="files-list">
        <h3>Fichiers sélectionnés ({{ files.length }})</h3>
        <div class="files-container">
          <div 
            v-for="(file, index) in files" 
            :key="index"
            class="file-item"
            :class="{ 'uploading': file.status === 'uploading', 'success': file.status === 'success', 'error': file.status === 'error' }"
          >
            <div class="file-info">
              <div class="file-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
                  <polyline points="13 2 13 9 20 9"/>
                </svg>
              </div>
              <div class="file-details">
                <span class="file-name">{{ file.name }}</span>
                <span class="file-size">{{ formatFileSize(file.size) }}</span>
                <div v-if="file.status === 'uploading'" class="upload-progress">
                  <div class="progress-bar">
                    <div class="progress" :style="{ width: file.progress + '%' }"></div>
                  </div>
                  <span>{{ file.progress }}%</span>
                </div>
                <div v-else-if="file.status === 'error'" class="error-message">
                  {{ file.error }}
                </div>
              </div>
            </div>
            <div class="file-actions">
                <button 
                    v-if="file.status === 'success'" 
                    class="action-btn success"
                    @click="downloadFile(file)"
                    title="Télécharger"
                >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                    </svg>
                </button>
                
                <button 
                    class="action-btn delete"
                    @click="removeFile(index)"
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
      </div>
    </div>

    <!-- Input file caché -->
    <input
      ref="fileInput"
      type="file"
      multiple
      :accept="allowedExtensions.join(',')"
      @change="onFileSelect"
      style="display: none"
    />

    <!-- Catégories de fichiers administratifs -->
    <div class="file-categories" v-if="showCategories">
      <h4>Catégories de documents administratifs</h4>
      <div class="categories-grid">
        <div 
          v-for="category in administrativeCategories" 
          :key="category.id"
          class="category-card"
          :class="{ 'selected': selectedCategory === category.id }"
          @click="selectCategory(category.id)"
        >
          <div class="category-icon">{{ category.icon }}</div>
          <span class="category-name">{{ category.name }}</span>
        </div>
      </div>
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
    showCategories: {
      type: Boolean,
      default: true
    },
    uploadUrl: {
      type: String,
      default: '/api/upload'
    }
  },
  data() {
    return {
      files: [],
      isDragOver: false,
      isUploading: false,
      selectedCategory: null,
      administrativeCategories: [
        { id: 'identity', name: 'Pièce d\'identité', icon: '🆔' },
        { id: 'residence', name: 'Justificatif de domicile', icon: '🏠' },
        { id: 'income', name: 'Relevés de revenus', icon: '💰' },
        { id: 'tax', name: 'Avis d\'imposition', icon: '📊' },
        { id: 'contract', name: 'Contrats', icon: '📝' },
        { id: 'insurance', name: 'Assurances', icon: '🛡️' },
        { id: 'bank', name: 'Relevés bancaires', icon: '💳' },
        { id: 'other', name: 'Autres documents', icon: '📄' }
      ]
    }
  },
  computed: {
    canUpload() {
      return this.files.length > 0 && 
             this.files.every(file => file.status !== 'uploading' && file.status !== 'error') &&
             (!this.showCategories || this.selectedCategory);
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
      const remainingSlots = this.maxFiles - this.files.length;
      const filesToAdd = fileList.slice(0, remainingSlots);

      filesToAdd.forEach(file => {
        // Validation de la taille
        if (file.size > this.maxFileSizeMB * 1024 * 1024) {
          this.$emit('error', `Le fichier "${file.name}" dépasse la taille maximale de ${this.maxFileSizeMB}MB`);
          return;
        }

        // Validation de l'extension
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        if (!this.allowedExtensions.includes(fileExtension)) {
          this.$emit('error', `Le format "${fileExtension}" n'est pas autorisé pour le fichier "${file.name}"`);
          return;
        }

        // Ajouter le fichier à la liste
        this.files.push({
          file: file,
          name: file.name,
          size: file.size,
          type: file.type,
          status: 'pending',
          progress: 0,
          category: this.selectedCategory
        });
      });

      if (fileList.length > remainingSlots) {
        this.$emit('error', `Nombre maximum de fichiers (${this.maxFiles}) atteint. Seuls ${remainingSlots} fichiers ont été ajoutés.`);
      }
    },

    removeFile(index) {
      this.files.splice(index, 1);
    },

    async uploadFiles() {
      if (!this.canUpload) return;

      this.isUploading = true;
      const uploadPromises = this.files.map((fileObj, index) => 
        this.uploadSingleFile(fileObj, index)
      );

      try {
        await Promise.all(uploadPromises);
        this.$emit('upload-complete', {
          files: this.files,
          category: this.selectedCategory
        });
      } catch (error) {
        this.$emit('upload-error', error);
      } finally {
        this.isUploading = false;
      }
    },

    async uploadSingleFile(fileObj, index) {
      return new Promise((resolve, reject) => {
        fileObj.status = 'uploading';
        
        // Simulation d'upload - À remplacer par votre logique réelle
        const interval = setInterval(() => {
          fileObj.progress += Math.random() * 20;
          if (fileObj.progress >= 100) {
            fileObj.progress = 100;
            clearInterval(interval);
            fileObj.status = 'success';
            fileObj.uploadedUrl = `/uploads/${fileObj.name}`; // URL simulée
            resolve(fileObj);
          }
        }, 200);

        // Pour une implémentation réelle, utilisez axios/fetch :
        /*
        const formData = new FormData();
        formData.append('file', fileObj.file);
        formData.append('category', this.selectedCategory);

        axios.post(this.uploadUrl, formData, {
          onUploadProgress: (progressEvent) => {
            fileObj.progress = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
          }
        })
        .then(response => {
          fileObj.status = 'success';
          fileObj.uploadedUrl = response.data.url;
          resolve(fileObj);
        })
        .catch(error => {
          fileObj.status = 'error';
          fileObj.error = error.message;
          reject(error);
        });
        */
      });
    },

    selectCategory(categoryId) {
      this.selectedCategory = categoryId;
      // Mettre à jour la catégorie pour tous les fichiers
      this.files.forEach(file => {
        file.category = categoryId;
      });
    },

    downloadFile(fileObj) {
      // Implémentation du téléchargement
      const link = document.createElement('a');
      link.href = fileObj.uploadedUrl;
      link.download = fileObj.name;
      link.click();
    },

    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
  },
  emits: ['upload-complete', 'upload-error', 'error']
}
</script>

<style scoped>
.file-uploader {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
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
  margin-bottom: 1.5rem;
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

.upload-prompt h3 {
  margin: 1rem 0 0.5rem;
  color: #374151;
  font-weight: 600;
  font-size: 1.2rem;
  text-align: center;
}

.upload-prompt p {
  color: #6b7280;
  margin: 0.5rem 0;
}

.upload-icon {
  color: #9ca3af;
  margin-bottom: 1rem;
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
  margin: 0.5rem 0;
}

.browse-btn:hover {
  background: #2563eb;
}

.file-info {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 1rem;
}

.files-list h3 {
  margin-bottom: 1rem;
  color: #374151;
  font-weight: 600;
  font-size: 1.2rem;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  background: white;
  transition: all 0.2s;
}

.file-item:hover {
  border-color: #d1d5db;
}

.file-item.uploading {
  border-left: 4px solid #3b82f6;
}

.file-item.success {
  border-left: 4px solid #10b981;
}

.file-item.error {
  border-left: 4px solid #ef4444;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.file-icon {
  color: #6b7280;
}

.file-details {
  display: flex;
  flex-direction: column;
}

.file-name {
  font-weight: 500;
  color: #374151;
}

.file-size {
  font-size: 0.875rem;
  color: #6b7280;
}

.upload-progress {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.progress-bar {
  flex: 1;
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: #3b82f6;
  transition: width 0.3s;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.file-actions {
  display: flex;
  gap: 1rem;
}

.action-btn {
  padding: 0.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn.success {
  background: #dcfce7;
  color: #16a34a;
}

.action-btn.success:hover {
  background: #bbf7d0;
}

.action-btn.delete {
  background: #fef2f2;
  color: #ef4444;
}

.action-btn.delete:hover {
  background: #fecaca;
}

.upload-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
  gap: 1rem;
}

.add-more-btn {
  background: transparent;
  color: #3b82f6;
  border: 1px solid #d1d5db;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.add-more-btn:hover {
  background: #f8fafc;
  border-color: #3b82f6;
}

.upload-btn {
  background: #10b981;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

.upload-btn:hover:not(:disabled) {
  background: #059669;
}

.upload-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.file-categories {
  margin-top: 2rem;
}

.file-categories h4 {
  margin-bottom: 1rem;
  color: #374151;
  font-weight: 600;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
}

.category-card:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
}

.category-card.selected {
  border-color: #3b82f6;
  background: #eff6ff;
}

.category-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.category-name {
  font-size: 0.875rem;
  text-align: center;
  color: #374151;
  font-weight: 500;
}
</style>