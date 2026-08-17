<template>
    <div class="card">
        
        <div class="card__header w-full flex justify-between">
            <button class="card__badge">
                {{ title }}
            </button>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
            </svg>
        </div>

        <div class="card__body">
            <p class="card__text">
                {{ content }}
            </p>
        </div>

        <div class="card__footer">
            
        </div>

    </div>
</template>

<script lang="ts">
export default{

    props:{
        title: {
            type: String,
            default: 'Dossiers'
        },
        content: {
            type: String,
            default: 'Lorem ipsum, dolor sit amet consectetur adipisicing elit. Harum cum eligendi.'
        }
    }

}
</script>

<style scoped>
/* 🎨 Variables (si tu ne les as pas déjà en global) */
:root {
  --primary-color: #2563eb; /* Un beau bleu moderne */
}

.card {
    /* Largeur et respiration */
    width: 100%;
    max-width: 280px; 
    padding: 0.5rem;
    
    /* Structure */
    display: flex;
    flex-direction: column;
    gap: 1rem;
    
    /* Design Premium */
    background: #ffffff;
    border-radius: 16px;
    
    /* Transition douce globale */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    
    /* ⚡️ CRUCIAL : Nécessaire pour positionner l'action à l'intérieur */
    position: relative; 
    
    /* Curseur pointer si toute la carte est un lien */
    cursor: pointer;
}

/* Ombre douce par défaut */
.card {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* --- Effet Hover global sur la carte --- */
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}


/* --- Stylisation des éléments existants --- */
.card__badge {
    padding: 0.4rem 1.2rem;
    background: var(--primary-color);
    color: #ffffff;
    border: none;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.3px;
    cursor: pointer;
}

.card__text {
    margin: 0;
    color: #4b5563; /* Gris doux */
    font-size: 0.95rem;
    line-height: 1.5;
}

/* --- ⚡️ Stylisation de la NOUVELLE Action --- */

.card__action {
    /* Positionnement en bas à droite */
    position: absolute;
    bottom: 1.5rem;
    right: 1.5rem;
    
    /* Structure de l'élément rond */
    display: flex;
    justify-content: center;
    align-items: center;
    width: 38px;
    height: 38px;
    background-color: var(--primary-color);
    border-radius: 50%; /* ⚡️ C'est rond ! */
    
    /* Design de la flèche */
    color: #ffffff;
    
    /* --- État par défaut (Caché) --- */
    opacity: 0;
    
    /* Légère rotation et échelle pour l'effet d'entrée */
    transform: translate(10px, 10px) scale(0.6); 
    
    /* Transition douce sur les propriétés */
    transition: 
        opacity 0.3s ease, 
        transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), /* Effet ressort (rebound) */
        background-color 0.2s ease;
}

/* --- Effet Hover pour révéler l'action --- */
.card:hover .card__action {
    opacity: 1;
    /* Revient à sa position et échelle normale */
    transform: translate(0, 0) scale(1);
}

/* Stylisation du SVG de la flèche */
.card__arrow {
    width: 18px;
    height: 18px;
}


/* --- ⚡️ L'animation du Background (Ripple/Pulsation) --- */

/* On crée un pseudo-élément ::after pour l'effet de ripple */
.card__action::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--primary-color);
    border-radius: 50%;
    
    /* L'animation est désactivée par défaut */
    opacity: 0;
}

/* On lance l'animation sur ::after uniquement quand la carte est survolée */
.card:hover .card__action::after {
    animation: pulse-ripple 1.2s infinite;
}

/* Définition de l'animation */
@keyframes pulse-ripple {
    0% {
        transform: scale(1);
        opacity: 0.6;
    }
    /* L'élément grandit et devient transparent */
    100% {
        transform: scale(1.6);
        opacity: 0;
    }
}
</style>