<template>
    <div class="options-container">
        <button 
            class="options-btn" 
            @click.stop="toggleDropdown"
            aria-label="Options du dossier"
            aria-expanded="showDropdown"
            aria-haspopup="true"
        >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
            </svg>
        </button>
        
        <transition name="dropdown">
            <div 
                v-if="showDropdown" 
                class="dropdown-menu"
                ref="dropdownRef"
                @mousedown.stop
            >
                <ul class="dropdown-list">
                    <li class="dropdown-item" @mousedown="handleAction('view')">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="dropdown-icon">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                        </svg>
                        <span>Voir le dossier</span>
                    </li>
                    <li class="dropdown-item" @mousedown="handleAction('edit')">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="dropdown-icon">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                        </svg>
                        <span>Modifier</span>
                    </li>
                    <li class="dropdown-item" @mousedown="handleAction('duplicate')">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M11.35 3.836c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m8.9-4.414c.376.023.75.05 1.124.08 1.131.094 1.976 1.057 1.976 2.192V16.5A2.25 2.25 0 0 1 18 18.75h-2.25m-7.5-10.5H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V18.75m-7.5-10.5h6.375c.621 0 1.125.504 1.125 1.125v9.375m-8.25-3 1.5 1.5 3-3.75" />
                        </svg>

                        <span>Marquer comme validé</span>
                    </li>
                    <li class="dropdown-divider"></li>
                    <li class="dropdown-item dropdown-item-danger" @mousedown="handleAction('archive')">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="dropdown-icon">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m20.25 7.5-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5m6 4.125 2.25 2.25m0 0 2.25 2.25M12 13.875l2.25-2.25M12 13.875l-2.25 2.25M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z" />
                        </svg>
                        <span>Archiver</span>
                    </li>
                    <li class="dropdown-item dropdown-item-danger" @mousedown="handleAction('delete')">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="dropdown-icon">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                        </svg>
                        <span>Supprimer</span>
                    </li>
                </ul>
            </div>
        </transition>
    </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';

export default {
    name: 'DropdownOptions',
    
    emits: ['action'],
    
    setup(props, { emit }) {
        const showDropdown = ref(false);
        const dropdownRef = ref(null);
        let clickOutsideHandler = null;
        
        // Fonction pour basculer l'état de la dropdown
        const toggleDropdown = () => {
            showDropdown.value = !showDropdown.value;
            
            if (showDropdown.value) {
                // Ajouter l'écouteur pour clic à l'extérieur après que le dropdown soit rendu
                setTimeout(() => {
                    clickOutsideHandler = (event) => {
                        if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
                            closeDropdown();
                        }
                    };
                    document.addEventListener('mousedown', clickOutsideHandler);
                }, 0);
            } else {
                // Retirer l'écouteur
                if (clickOutsideHandler) {
                    document.removeEventListener('mousedown', clickOutsideHandler);
                    clickOutsideHandler = null;
                }
            }
        };
        
        // Fermer la dropdown
        const closeDropdown = () => {
            showDropdown.value = false;
            
            // Retirer l'écouteur
            if (clickOutsideHandler) {
                document.removeEventListener('mousedown', clickOutsideHandler);
                clickOutsideHandler = null;
            }
        };
        
        // Gérer le clic sur un élément du dropdown
        const handleAction = (action) => {
            emit('action', action);
            closeDropdown();
        };
        
        // Fermer la dropdown avec la touche Escape
        const handleEscapeKey = (event) => {
            if (event.key === 'Escape' && showDropdown.value) {
                closeDropdown();
            }
        };
        
        // Configuration des écouteurs d'événements
        onMounted(() => {
            document.addEventListener('keydown', handleEscapeKey);
        });
        
        onUnmounted(() => {
            document.removeEventListener('keydown', handleEscapeKey);
            if (clickOutsideHandler) {
                document.removeEventListener('mousedown', clickOutsideHandler);
            }
        });
        
        return {
            showDropdown,
            dropdownRef,
            toggleDropdown,
            closeDropdown,
            handleAction
        };
    }
};
</script>

<style scoped>
.options-container {
    position: relative;
    display: inline-block;
}

.options-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s;
    color: #718096;
}

.options-btn:hover {
    background-color: #edf2f7;
    color: #4299e1;
}

.options-btn:focus {
    outline: 2px solid #4299e1;
    outline-offset: 2px;
}

.options-btn svg {
    width: 1.5rem;
    height: 1.5rem;
}

.dropdown-menu {
    position: absolute;
    top: 100%;
    right: 0;
    z-index: 1000;
    min-width: 200px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    border: 1px solid #e2e8f0;
    margin-top: 0.25rem;
    overflow: hidden;
}

/* Animation d'entrée/sortie */
.dropdown-enter-active {
    animation: dropdownFadeIn 0.2s ease;
}

.dropdown-leave-active {
    animation: dropdownFadeOut 0.15s ease;
}

@keyframes dropdownFadeIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes dropdownFadeOut {
    from {
        opacity: 1;
        transform: translateY(0);
    }
    to {
        opacity: 0;
        transform: translateY(-10px);
    }
}

.dropdown-list {
    list-style: none;
    padding: 0.5rem 0;
    margin: 0;
}

.dropdown-item {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
    font-size: 0.875rem;
    color: #4a5568;
    gap: 0.75rem;
    user-select: none;
}

.dropdown-item:hover {
    background-color: #f7fafc;
}

.dropdown-item:active {
    background-color: #edf2f7;
}

.dropdown-icon {
    width: 1.25rem;
    height: 1.25rem;
    flex-shrink: 0;
}

.dropdown-divider {
    height: 1px;
    background: #e2e8f0;
    margin: 0.5rem 0;
}

.dropdown-item-danger {
    color: #e53e3e;
}

.dropdown-item-danger:hover {
    background-color: #fed7d7;
}

.dropdown-item-danger:active {
    background-color: #feb2b2;
}

/* Responsive */
@media (max-width: 480px) {
    .dropdown-menu {
        position: fixed;
        right: 1rem;
        left: 1rem;
        bottom: 1rem;
        top: auto;
        max-height: 60vh;
        overflow-y: auto;
        margin-top: 0;
    }
}
</style>