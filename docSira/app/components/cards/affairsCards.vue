<template>
    <div class="card" ref="cardRef" :class="{ 'card--active': isOpen }">
        
        <div class="card__header w-full flex justify-between">
            <button class="card__badge">
                {{ title }}
            </button>
            
            <svg 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" viewBox="0 0 24 24" 
                stroke-width="1.5" 
                stroke="currentColor" 
                class="size-6 cursor-pointer"
                @click.stop="toggleMenu"
            >
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
            </svg>
        </div>

        <div class="card__body">
            <p class="card__text">
                {{ content }}
            </p>
        </div>

        <div class="card__footer flex w-full items-center justify-between">
            <div class="icons">
                <span class="footer__content">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-10">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25M9 16.5v.75m3-3v3M15 12v5.25m-4.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                    </svg>
                </span>
            </div>
            <div class="info">
                <p>1 fichier(s)</p>
            </div>
        </div>

        <Teleport to="body">
            <transition name="fade">
                <div 
                    v-if="isOpen" 
                    class="overlay" 
                    @click="isOpen = false"
                ></div>
            </transition>
        </Teleport>

        <!-- ⚡️ Ajout des classes dynamiques pour le X (gauche/droite) et Y (haut/bas) -->
        <transition :name="menuPositionX === 'right' ? 'slide-right' : 'slide-left'">
            <div 
                v-if="isOpen" 
                class="dropbox" 
                :class="['dropbox--' + menuPositionX, 'dropbox--' + menuPositionY]"
            >
                <ul>
                    <li @click="isOpen = false">Ouvrir</li>
                    <li @click="isOpen = false">Renommer</li>
                    <li @click="isOpen = false">Partager</li>
                    <li @click="isOpen = false">Créer un lien</li>
                    <li @click="isOpen = false">Télécharger</li>
                    <li @click="isOpen = false">Archiver</li>
                    <li class="danger" @click="isOpen = false">Supprimer</li>
                </ul>
            </div>
        </transition>

    </div>
</template>

<script lang="ts">
import { ref } from 'vue';

export default {
    props: {
        title: {
            type: String,
            default: 'Dossiers'
        },
        content: {
            type: String,
            default: 'Lorem ipsum, dolor sit amet consectetur adipisicing elit. Harum cum eligendi.'
        }
    },

    setup() {
        const isOpen = ref<boolean>(false);
        const cardRef = ref<HTMLElement | null>(null);
        
        // On sépare la position X et Y
        const menuPositionX = ref<'left' | 'right'>('right');
        const menuPositionY = ref<'top' | 'bottom'>('top');

        const toggleMenu = () => {
            isOpen.value = !isOpen.value;
            
            if (isOpen.value && cardRef.value) {
                const rect = cardRef.value.getBoundingClientRect();
                
                // Calcul de l'espace disponible
                const spaceOnRight = window.innerWidth - rect.right;
                const spaceOnBottom = window.innerHeight - rect.top; // Espace vers le bas
                
                // Axe X : Gérer Gauche / Droite
                if (spaceOnRight < 200) {
                    menuPositionX.value = 'left';
                } else {
                    menuPositionX.value = 'right';
                }
                
                // Axe Y : Gérer Haut / Bas (Si l'espace en bas est < à 320px, on ouvre vers le haut)
                if (spaceOnBottom < 320) {
                    menuPositionY.value = 'bottom';
                } else {
                    menuPositionY.value = 'top';
                }
            }
        };

        return {
            isOpen,
            cardRef,
            menuPositionX,
            menuPositionY,
            toggleMenu
        }
    }
}
</script>

<style scoped>
.card {
    width: 100%;
    max-width: 310px; 
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    background: #ffffff;
    border-radius: 16px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    position: relative; 
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.card--active {
    z-index: 50; 
    position: relative; 
}

.card__badge {
    padding: 0.4rem 1.2rem;
    background: var(--primary-color, #2563eb);
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
    color: #4b5563; 
    font-size: 0.95rem;
    line-height: 1.5;
}

.card__footer .footer__content {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0.6rem;
    background: var(--primary-color, #2563eb);
    max-width: 32px;
    max-height: 32px;
    border-radius: 999px;
}

.card__footer .footer__content svg {
    width: 32px;
    height: 32px;
    color: #ffffff; 
    stroke: #ffffff;
}

.card__footer p {
    color: #7d8796;
    font-size: 0.8rem;
    font-weight: 500;
}

/* --- ⚡️ La Dropbox --- */
.dropbox {
    position: absolute;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
    border: 1px solid #f3f4f6;
    min-width: 170px;
    z-index: 55; 
    overflow: hidden; 
}

/* --- ⚡️ Modificateurs d'axe Y (Haut/Bas) --- */
.dropbox--top {
    top: 0;
    bottom: auto;
}
.dropbox--bottom {
    bottom: 0; /* Aligne le bas du menu avec le bas de la carte (pousse vers le haut) */
    top: auto;
}

/* --- ⚡️ Modificateurs d'axe X (Gauche/Droite) --- */
.dropbox--right {
    left: calc(100% + 15px); 
    right: auto;
}
.dropbox--left {
    right: calc(100% + 15px); 
    left: auto;
}

/* --- ⚡️ Modificateurs d'Origine pour l'Animation (Crucial pour l'effet rebond) --- */
.dropbox--right.dropbox--top { transform-origin: top left; }
.dropbox--right.dropbox--bottom { transform-origin: bottom left; }
.dropbox--left.dropbox--top { transform-origin: top right; }
.dropbox--left.dropbox--bottom { transform-origin: bottom right; }


.dropbox ul {
    list-style: none;
    margin: 0;
    padding: 0.5rem 0;
}

.dropbox li {
    padding: 0.7rem 1.2rem;
    font-size: 0.875rem;
    color: #374151;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s ease, color 0.2s ease;
}

.dropbox li:hover {
    background-color: #f3f4f6;
    color: var(--primary-color, #2563eb);
}

.dropbox li.danger {
    color: #dc2626;
}
.dropbox li.danger:hover {
    background-color: #fef2f2;
    color: #b91c1c;
}

/* --- Animations --- */
.slide-right-enter-active,
.slide-right-leave-active,
.slide-left-enter-active,
.slide-left-leave-active {
    transition: opacity 0.25s ease, transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-right-enter-from,
.slide-right-leave-to {
    opacity: 0;
    transform: translateX(-15px) scale(0.95);
}

.slide-left-enter-from,
.slide-left-leave-to {
    opacity: 0;
    transform: translateX(15px) scale(0.95);
}

/* --- Overlay --- */
:global(.overlay) {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(17, 24, 39, 0.25);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    z-index: 40; 
    cursor: default;
}

:global(.fade-enter-active),
:global(.fade-leave-active) {
    transition: opacity 0.3s ease;
}
:global(.fade-enter-from),
:global(.fade-leave-to) {
    opacity: 0;
}
</style>