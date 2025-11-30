<template>
  <div class="file-uploader">
    <!-- Zone de dépôt -->
    <div 
      class="drop-zone"
      :class="{ 'drag-over': isDragOver, }"
    >
      <!-- État initial -->
      <div class="upload-prompt">
        <div class="upload-icon center__flex">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
        </div>
        <button class="browse-btn" @click="handleNavigateTo()">
          Ajouter fichiers
        </button>
        <p class="file-info">
          Formats acceptés : {{ allowedExtensions.join(', ') }}<br>
          Taille max : {{ maxFileSizeMB }}MB par fichier
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
    name: 'AdministrativeFileUploader',
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

    setup(){
        const router = useRouter();

        function handleNavigateTo(){
            router.push('/upload-file')
        }

        return{
            router,
            handleNavigateTo
        }
    }
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

</style>