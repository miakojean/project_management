<template>
  <div class="skeleton-container">
    <!-- Option de grille flexible -->
    <div class="skeleton-controls" v-if="showControls">
      <div class="controls">
        <label for="columns">Colonnes:</label>
        <select id="columns" v-model="columns">
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>
        
        <label for="viewMode">Mode:</label>
        <select id="viewMode" v-model="viewMode">
          <option value="mixed">Mixte (dossiers + documents)</option>
          <option value="folders">Dossiers seulement</option>
          <option value="documents">Documents seulement</option>
        </select>
      </div>
    </div>

    <!-- Grille de skeleton -->
    <div class="skeleton-grid" :class="`grid-cols-${columns}`">
      <!-- Items de skeleton -->
      <div 
        v-for="(item, index) in skeletonItems" 
        :key="index" 
        class="skeleton-item"
        :class="item.type"
      >
        <!-- Pour les dossiers -->
        <div v-if="item.type === 'folder'" class="folder-skeleton">
          <div class="folder-icon shimmer"></div>
          <div class="folder-name shimmer"></div>
          <div class="folder-info shimmer"></div>
        </div>
        
        <!-- Pour les documents -->
        <div v-else class="document-skeleton">
          <div class="document-icon shimmer"></div>
          <div class="document-name shimmer"></div>
          <div class="document-meta">
            <div class="meta-item shimmer"></div>
            <div class="meta-item shimmer"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SkeletonGrid',
  props: {
    // Nombre d'éléments à afficher
    itemCount: {
      type: Number,
      default: 8
    },
    // Afficher les contrôles
    showControls: {
      type: Boolean,
      default: false
    },
    // État de chargement
    isLoading: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      columns: 4,
      viewMode: 'mixed'
    };
  },
  computed: {
    skeletonItems() {
      const items = [];
      
      for (let i = 0; i < this.itemCount; i++) {
        let type = 'document';
        
        // Déterminer le type selon le mode
        if (this.viewMode === 'folders') {
          type = 'folder';
        } else if (this.viewMode === 'documents') {
          type = 'document';
        } else {
          // Mode mixte: alterner entre dossiers et documents
          type = i % 3 === 0 ? 'folder' : 'document';
        }
        
        items.push({ type, id: i });
      }
      
      return items;
    }
  }
};
</script>

<style scoped>
.skeleton-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Contrôles */
.skeleton-controls {
  margin-bottom: 30px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.controls {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.controls label {
  font-weight: 600;
  color: #495057;
  font-size: 14px;
}

.controls select {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ced4da;
  background-color: white;
  font-size: 14px;
  color: #495057;
  cursor: pointer;
  transition: border-color 0.2s;
}

.controls select:focus {
  outline: none;
  border-color: #4361ee;
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
}

/* Grille de skeleton */
.skeleton-grid {
  display: grid;
  gap: 24px;
}

.grid-cols-2 {
  grid-template-columns: repeat(2, 1fr);
}

.grid-cols-3 {
  grid-template-columns: repeat(3, 1fr);
}

.grid-cols-4 {
  grid-template-columns: repeat(4, 1fr);
}

.grid-cols-5 {
  grid-template-columns: repeat(5, 1fr);
}

/* Item de skeleton */
.skeleton-item {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e9ecef;
  transition: transform 0.2s, box-shadow 0.2s;
  height: 180px;
  display: flex;
  flex-direction: column;
}

.skeleton-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.08);
}

/* Styles pour les dossiers */
.folder-skeleton {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  justify-content: center;
}

.folder-icon {
  width: 70px;
  height: 60px;
  background-color: #e9ecef;
  border-radius: 10px;
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
}

.folder-icon::after {
  content: '';
  position: absolute;
  top: -5px;
  left: 10px;
  width: 50px;
  height: 10px;
  background-color: #dee2e6;
  border-radius: 4px 4px 0 0;
}

.folder-name {
  width: 80%;
  height: 16px;
  background-color: #e9ecef;
  border-radius: 4px;
  margin-bottom: 12px;
}

.folder-info {
  width: 60%;
  height: 12px;
  background-color: #e9ecef;
  border-radius: 4px;
}

/* Styles pour les documents */
.document-skeleton {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.document-icon {
  width: 60px;
  height: 80px;
  background-color: #e9ecef;
  border-radius: 8px;
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
}

.document-icon::after {
  content: '';
  position: absolute;
  top: 10px;
  left: 5px;
  right: 5px;
  height: 40px;
  background-color: #dee2e6;
  border-radius: 4px;
}

.document-name {
  width: 90%;
  height: 16px;
  background-color: #e9ecef;
  border-radius: 4px;
  margin-bottom: 15px;
}

.document-meta {
  display: flex;
  justify-content: space-between;
  margin-top: auto;
}

.meta-item {
  width: 40%;
  height: 12px;
  background-color: #e9ecef;
  border-radius: 4px;
}

/* Effet de shimmer */
.shimmer {
  position: relative;
  overflow: hidden;
}

.shimmer::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.6), transparent);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

/* État de chargement */
.skeleton-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  margin-top: 20px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e9ecef;
  border-top: 4px solid #4361ee;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.skeleton-loading p {
  color: #6c757d;
  font-size: 16px;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 1024px) {
  .grid-cols-4, .grid-cols-5 {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .grid-cols-3, .grid-cols-4, .grid-cols-5 {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .controls {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}

@media (max-width: 480px) {
  .skeleton-grid {
    grid-template-columns: 1fr;
  }
  
  .skeleton-item {
    height: 160px;
  }
}
</style>