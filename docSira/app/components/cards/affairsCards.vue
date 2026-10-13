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
                class="size-8 cursor-pointer"
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
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25M9 16.5v.75m3-3v3M15 12v5.25m-4.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                    </svg>
                </span>
                <span class="footer__content">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25M9 16.5v.75m3-3v3M15 12v5.25m-4.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                    </svg>
                </span>
            </div>

            <div class="info">
                <p>2 fichier(s)</p>

                <div class="progress-ring" :title="progress + '% complété'">
                    <svg width="36" height="36" viewBox="0 0 36 36">
                        <circle
                            class="progress-ring__track"
                            stroke-width="3"
                            fill="transparent"
                            :r="radius"
                            cx="18"
                            cy="18"
                        />
                        <circle
                            class="progress-ring__circle"
                            stroke-width="3"
                            fill="transparent"
                            :r="radius"
                            cx="18"
                            cy="18"
                            :stroke-dasharray="circumference"
                            :stroke-dashoffset="progressOffset"
                        />
                    </svg>
                    <span class="progress-ring__text">{{ progress }}%</span>
                </div>
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

        <transition :name="menuPositionX === 'right' ? 'slide-right' : 'slide-left'">
            <div
                v-if="isOpen"
                class="dropbox"
                :class="['dropbox--' + menuPositionX, 'dropbox--' + menuPositionY]"
            >
                <ul>
                    <li @click="$emit('goTo')">
                        Ouvrir
                    </li>
                    <li @click="() => { isOpen = false, $emit('open')}" class="w-full flex items-center justify-start gap-2" >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 1 1-3 0m3 0a1.5 1.5 0 1 0-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-9.75 0h9.75" />
                        </svg>
                        Détails
                    </li>
                    <li @click="() => { isOpen = false, $emit('rename')}" class="w-full flex items-center justify-start gap-2" >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                        </svg>
                        Renommer
                    </li>
                    <li @click="() => { isOpen = false, $emit('share')}" class="w-full flex items-center justify-start gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M7.217 10.907a2.25 2.25 0 1 0 0 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186 9.566-5.314m-9.566 7.5 9.566 5.314m0 0a2.25 2.25 0 1 0 3.935 2.186 2.25 2.25 0 0 0-3.935-2.186Zm0-12.814a2.25 2.25 0 1 0 3.933-2.185 2.25 2.25 0 0 0-3.933 2.185Z" />
                        </svg>
                        Partager
                    </li>
                    <li @click="() => { isOpen = false, $emit('link')}" class="w-full flex items-center justify-start gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
                        </svg>
                        Créer un lien
                    </li>
                    <li @click="isOpen = false" class="w-full flex items-center justify-start gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                        </svg>
                        Télécharger
                    </li>
                    <li @click="() => { isOpen = false, $emit('archive') }" class="w-full flex items-center justify-start gap-2" >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m20.25 7.5-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z" />
                        </svg>
                        Archiver
                    </li>
                    <li class="danger" @click="() => { isOpen = false, $emit('delete') }">Supprimer</li>
                </ul>
            </div>
        </transition>

    </div>
</template>

<script lang="ts">
import { ref, computed } from 'vue';

export default {
    props: {
        title: {
            type: String,
            default: 'Dossiers'
        },
        content: {
            type: String,
            default: 'Lorem ipsum, dolor sit amet consectetur adipisicing elit. Harum cum eligendi.'
        },
        // Nouvelle prop pour la progression (de 0 à 100)
        progress: {
            type: Number,
            default: 35
        }
    },

    emits: ['goTo','open', 'rename', 'share', 'link', 'download', 'archive', 'delete'],

    setup(props, { emit }) {
        const isOpen = ref<boolean>(false);
        const cardRef = ref<HTMLElement | null>(null);

        const menuPositionX = ref<'left' | 'right'>('right');
        const menuPositionY = ref<'top' | 'bottom'>('top');

        // --- Logique de l'anneau de progression ---
        const radius = 15; // Rayon du cercle
        const circumference = 2 * Math.PI * radius; // Calcul de la circonférence [cite: 14, 15]

        // Calcul du décalage pour simuler la progression
        const progressOffset = computed(() => {
            // Sécurité pour s'assurer que la valeur reste entre 0 et 100
            const validProgress = Math.max(0, Math.min(100, props.progress));
            return circumference - (validProgress / 100) * circumference;
        });

        const toggleMenu = () => {
            isOpen.value = !isOpen.value;

            if (isOpen.value && cardRef.value) {
                const rect = cardRef.value.getBoundingClientRect();

                const spaceOnRight = window.innerWidth - rect.right;
                const spaceOnBottom = window.innerHeight - rect.top;

                if (spaceOnRight < 200) {
                    menuPositionX.value = 'left';
                } else {
                    menuPositionX.value = 'right';
                }

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
            toggleMenu,
            // Retour des variables de progression
            radius,
            circumference,
            progressOffset
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

/* --- ⚡️ Section Superposition des Icônes --- */
.icons {
    display: flex;
    align-items: center;
}

.card__footer .footer__content {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0.4rem;
    background: var(--primary-color, #2563eb);
    width: 38px;
    height: 38px;
    border-radius: 999px;
    flex-shrink: 0;
    border: 2px solid #ffffff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
    position: relative;
    transition: transform 0.2s ease;
}

.card__footer .footer__content + .footer__content {
    margin-left: -14px;
}

.card__footer .footer__content:hover {
    transform: scale(1.1);
    z-index: 10;
}

.card__footer .footer__content svg {
    width: 20px;
    height: 20px;
    color: #ffffff;
    stroke: #ffffff;
}

.card__footer p {
    color: #7d8796;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 0;
}

/* --- Dropbox --- */
.dropbox {
    position: absolute;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
    border: 1px solid #f3f4f6;
    min-width: 170px;
    z-index: 55;
    overflow: hidden;
    padding: 0.5rem;
}

.dropbox--top {
    top: 0;
    bottom: auto;
}
.dropbox--bottom {
    bottom: 0;
    top: auto;
}

.dropbox--right {
    left: calc(100% + 15px);
    right: auto;
}
.dropbox--left {
    right: calc(100% + 15px);
    left: auto;
}

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
    padding: 0.7rem;
    font-size: 0.875rem;
    color: #374151;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s ease, color 0.2s ease;
    border-radius: 0.5rem;
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

/* --- ⚡️ Section Info & Anneau de progression --- */
.info {
    display: flex;
    align-items: center;
    gap: 0.75rem; /* Espacement entre le texte et l'anneau [cite: 26] */
}

.progress-ring {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
}

.progress-ring svg {
    /* Fait pivoter le SVG de -90deg pour que la progression commence à midi (en haut) [cite: 28] */
    transform: rotate(-90deg);
}

.progress-ring__track {
    stroke: #e5e7eb; /* Couleur de la piste de fond (gris clair) [cite: 28] */
}

.progress-ring__circle {
    stroke: var(--primary-color, #2563eb);
    stroke-linecap: round; /* Bords arrondis pour la barre de progression [cite: 29] */
    transition: stroke-dashoffset 0.5s ease-in-out; /* Animation fluide lors du changement de valeur [cite: 30] */
}

.progress-ring__text {
    position: absolute;
    font-size: 0.6rem;
    font-weight: 700;
    color: #4b5563; /* [cite: 31] */
}
</style>
