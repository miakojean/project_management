<template>
  <div class="folder-card">
    <div class="folder-card__icon-wrapper">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.2" stroke="currentColor" class="folder-icon">
        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
      </svg>
    </div>

    <div class="folder-card__footer">
      <h3 class="folder-card__name">{{ folderName }}</h3>
      
      <span v-if="itemCount !== undefined" class="folder-card__count">
        {{ itemCount }} {{ itemCount > 1 ? 'fichiers' : 'fichier' }}
      </span>
    </div>
  </div>
</template>

<script setup>
// Props pour rendre la carte réutilisable à l'infini !
defineProps({
  folderName: {
    type: String,
    required: true,
    default: 'Nouveau dossier'
  },
  itemCount: {
    type: Number,
    default: 0 // Si tu ne passes rien, ça affichera "0 fichier"
  }
})
</script>

<style scoped>
/* 🎨 Variables (à adapter selon ton projet) */
:root {
  --primary-color: #2563eb;
}

.folder-card {
    /* Dimensions pensées pour une grille (idéal avec display: grid) */
    width: 100%;
    max-width: 220px;
    aspect-ratio: 1 / 1; /* Rend la carte parfaitement carrée */
    
    /* Structure interne */
    display: flex;
    flex-direction: column;
    justify-content: flex-end; /* Pousse le contenu vers le bas */
    align-items: center;
    padding: 1.5rem;
    
    /* Design Premium */
    background: #ffffff;
    border-radius: 16px;
    border: 2px solid transparent; /* Prépare le terrain pour le hover */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    
    cursor: pointer;
    position: relative;
    
    /* Transition globale ultra fluide */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* --- Effet au survol de la carte --- */
.folder-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(37, 99, 235, 0.15); /* Ombre légèrement teintée */
    border-color: var(--primary-color);
}

/* --- Zone de l'icône --- */
.folder-card__icon-wrapper {
    /* Positionnement pour centrer l'icône au milieu de l'espace restant */
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    
    /* État par défaut (Gris doux) */
    color: #9ca3af;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); /* Effet ressort */
}

.folder-icon {
    width: 72px;
    height: 72px;
}

/* Quand on survole la carte entière, l'icône réagit ! */
.folder-card:hover .folder-card__icon-wrapper {
    color: var(--primary-color);
    transform: scale(1.15); /* L'icône grossit légèrement vers l'utilisateur */
}

/* --- Zone du texte (En bas) --- */
.folder-card__footer {
    width: 100%;
    text-align: center;
    margin-top: 1rem;
}

.folder-card__name {
    margin: 0;
    color: #374151;
    font-size: 1.05rem;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis; /* Ajoute des "..." si le nom du dossier est trop long */
    transition: color 0.3s ease;
}

.folder-card:hover .folder-card__name {
    color: var(--primary-color);
}

.folder-card__count {
    display: block;
    margin-top: 0.3rem;
    font-size: 0.8rem;
    color: #6b7280;
    font-weight: 500;
}
</style>