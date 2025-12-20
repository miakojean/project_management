<template>
    <nav>
        <div class="research__box">
            <researchfamily 
                placeholder="Rechercher un dossier, client..."
                :searchFunction="customSearchFunction"
                :maxResults="8"
                @search="handleSearch"
                @select="handleSelect"
            />
        </div>
        <addButton @click="handleAddClick"/>
        <div class="btn__frame">
            <div class="notification-wrapper" @click="handleNotificationClick">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1" stroke="currentColor" class="size-8">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
                </svg>
                <span v-if="notifStore.hasUnread" class="notification-bubble">
                    {{ notifStore.displayCount }}
                </span>

                <div v-if="showNotificationsDropdown" class="notification-dropdown">
                    <div class="dropdown-header">
                        <h4>Notifications ({{ notifStore.unreadCount }} non lues)</h4>
                        <button v-if="notifStore.hasUnread" @click.stop="clearNotifications" class="btn-clear">
                            Tout marquer comme lu
                        </button>
                    </div>
                    <div class="dropdown-content">
                        <p v-if="notifStore.isLoading" class="loading-message">Chargement...</p>
                        <p v-else-if="notifStore.notifications.length === 0" class="empty-message">
                            Aucune notification
                        </p>
                        <ul v-else>
                            <!-- Afficher d'abord les non lues -->
                            <li v-for="notif in notifStore.unreadNotifications" 
                                :key="`unread-${notif.id}`" 
                                class="notification-item unread"
                                @click="markAsRead(notif.id)">
                                <div class="notification-content">
                                    <span class="unread-indicator">●</span>
                                    <div class="notification-text">
                                        <strong>{{ notif.verb_display || notif.verb }}</strong>
                                        <p>{{ notif.message }}</p>
                                    </div>
                                </div>
                                <span class="timestamp">{{ formatTime(notif.created_at) }}</span>
                            </li>
                            
                            <!-- Séparateur -->
                            <li v-if="notifStore.unreadNotifications.length > 0 && notifStore.notifications.length > notifStore.unreadNotifications.length" 
                                class="notification-separator">
                                <hr>
                            </li>
                            
                            <!-- Puis les lues -->
                            <li v-for="notif in notifStore.notifications.filter(n => n.is_read_for_current_user)" 
                                :key="`read-${notif.id}`" 
                                class="notification-item read">
                                <div class="notification-content">
                                    <div class="notification-text">
                                        <strong>{{ notif.verb_display || notif.verb }}</strong>
                                        <p>{{ notif.message }}</p>
                                    </div>
                                </div>
                                <span class="timestamp">{{ formatTime(notif.created_at) }}</span>
                            </li>
                            
                            <li v-if="notifStore.notifications.length >= 10" class="notification-item more-link">
                                Voir toutes les notifications
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
import { ref, onMounted, watch, onUnmounted } from 'vue';
import researchfamily from '../input/researchfamily.vue';
import addButton from '../button/addButton.vue';
import { useRouter } from 'vue-router';
import { useNotificationStore } from '@/stores/notifications';

export default {
    name: 'NavigationBar',
    components: {
        researchfamily,
        addButton
    },
    emits: [
        'notification-click',
        'notifications-cleared', 
        'notification-added',
        'add-click',
        'notification-count-changed'
    ],
    setup(props, { emit }) {

        // routing
        const router = useRouter();

        // 🚀 INITIALISATION DU STORE
        const notifStore = useNotificationStore();

        // Réactives
        // 🚀 Anciens: notificationCount et isLoading sont remplacés par le store
        const showNotificationsDropdown = ref(false); 

        // Méthode utilitaire de formatage de temps (simple pour l'exemple)
        const formatTime = (isoString) => {
            const date = new Date(isoString);
            return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
        };


        const refreshData = async () => {
            // Appelle directement loadUnreadCount qui met à jour unreadCount
            await notifStore.loadUnreadCount();
        };
        
        // Méthodes pour le composant (simplifiées grâce au store)
        
        // 🚀 Remplace markNotificationsAsRead
        const clearNotifications = async () => {
            if (!notifStore.hasUnread) return;

            const clearedCount = await notifStore.markAllAsRead(); 
            
            if (clearedCount > 0) {
                // Émet l'événement après succès
                emit('notifications-cleared', clearedCount);
            }
            
            return {
                success: clearedCount > 0,
                clearedCount: clearedCount
            };
        };

        // Gestion des événements
        const handleNotificationClick = async () => {
            
            // 1. Basculer l'état du dropdown
            showNotificationsDropdown.value = !showNotificationsDropdown.value;

            // 2. Si on ouvre le dropdown, charger les détails
            if (showNotificationsDropdown.value) {
                await notifStore.loadNotifications(); // Charge la liste détaillée
                
                // 3. (Optionnel) Marquer les notifications comme lues à l'ouverture
                // On laisse la méthode clearNotifications() gérer le marquage complet.
                // Si vous voulez marquer à la lecture, décommentez la ligne suivante :
                // await clearNotifications(); 
            }
            
            emit('notification-click', {
                count: notifStore.unreadCount,
                hasUnread: notifStore.hasUnread
            });
        };

        const handleAddClick = () => {
            emit('add-click');
            router.push('/customer')
        };

        const markAsRead = async (notificationId) => {
            if (!notificationId) return;
            
            try {
                // Marquer comme lue via le store
                await notifStore.markAsRead(notificationId);
                
                // Optionnel: Émettre un événement
                emit('notification-read', notificationId);
                
            } catch (error) {
                console.error('Erreur lors du marquage de la notification:', error);
            }
        };
        
        // Les méthodes simulateNotification, refreshNotifications, et getNotificationStatus peuvent
        // être retirées ou adaptées pour utiliser les actions directes du store.
        
        // Watcher pour les changements du compteur (observe la propriété du store)
        watch(() => notifStore.unreadCount, (newCount, oldCount) => {
            if (newCount !== oldCount) {
                emit('notification-count-changed', {
                    newCount,
                    oldCount,
                    hasIncreased: newCount > oldCount
                });
            }
        });

        onMounted(() => {
        // Charger le nombre de notifications non lues au montage
            refreshData();
            
            // Optionnel: recharger périodiquement (toutes les 30 secondes)
            const interval = setInterval(refreshData, 300000);
            
            // Nettoyer l'intervalle quand le composant est détruit
            onUnmounted(() => {
                clearInterval(interval);
            });
        });

        // Handle search event from the search component (optional: here we just log)
        const handleSearch = (payload) => {
            // payload: { query, results }
            console.log('Navigation bar search event:', payload);
            // In the future we could navigate or focus a specific section
        };

        // Retour des éléments exposés
        return {
            // Réactives/Store
            router,
            notifStore, // Exposer le store entier pour un accès facile
            showNotificationsDropdown,
            
            // Getters/State pour le template
            notificationCount: notifStore.unreadCount, // Reste pour la compatibilité
            isLoading: notifStore.isLoading,

            // Méthodes
            handleAddClick,
            handleNotificationClick,
            clearNotifications,
            formatTime,
            markAsRead,
            
            // Anciennes méthodes à garder si elles sont appelées de l'extérieur
            refreshNotifications: refreshData,
            // Search handler (exposed so template @search can call it)
            handleSearch,
        };
    }
}
</script>

<style scoped>
/* Les styles restent inchangés car ils sont déjà fonctionnels */
nav{
    padding: 1rem;
    display:flex;
    align-items:center;
    justify-content: end;
    gap: 1rem;
    width: 100%;
}

.research__box{
    width: 400px;
}
.btn__frame{
    display: flex;
    align-items: center;
    gap: 1rem;
}


/* Styles pour le wrapper de notification */
.notification-wrapper {
    position: relative; 
    display: inline-block;
    cursor: pointer;
}

svg{
    transition: all 0.3s ease;
}

svg:hover{
    background: #dbdbdb;
    border-radius: 50%;
}

/* Styles pour la bulle de notification (inchangés) */
.notification-bubble {
    position: absolute;
    top: -5px;
    right: -5px;
    background: #ff4444;
    color: white;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    font-size: 0.7rem;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    animation: pulse 2s infinite;
}

/* Styles pour le dropdown */
.notification-dropdown {
    position: absolute;
    top: 100%; 
    right: 0;
    width: 400px;
    max-height: 400px;
    overflow-y: auto;
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 1000; 
    margin-top: 10px; 
}

.dropdown-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 15px;
    border-bottom: 1px solid #f0f0f0;
}

.dropdown-header h4 {
    margin: 0;
    font-size: 1rem;
    color: #333;
}

.btn-clear {
    background: none;
    border: none;
    color: #007bff;
    cursor: pointer;
    font-size: 0.8rem;
    padding: 5px;
    border-radius: 4px;
    transition: background-color 0.2s;
}

.btn-clear:hover {
    background-color: #f0f0f0;
}

.dropdown-content {
    padding: 0;
}

.dropdown-content ul {
    list-style: none;
    padding: 0;
    margin: 0;
    flex-direction: column; 
}

.notification-item {
    padding: 10px 15px;
    border-bottom: 1px solid #f5f5f5;
    font-size: 0.9rem;
    color: #555;
    cursor: pointer;
    transition: background-color 0.2s;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.notification-item.is-read {
    background-color: #fafafa;
    color: #999;
}

.notification-item .timestamp {
    font-size: 0.75rem;
    color: #aaa;
    margin-left: 10px;
}

.notification-item:hover {
    background-color: #f0f0f0;
}

.notification-item:last-child {
    border-bottom: none;
}

.empty-message, .loading-message {
    padding: 15px;
    text-align: center;
    color: #777;
    font-style: italic;
}

.more-link {
    text-align: center;
    color: #007bff;
    font-weight: bold;    
    cursor: pointer;
}

/* Styles pour les notifications non lues */
.notification-item.unread {
    background-color: #f0f8ff; /* Bleu très clair */
    border-left: 3px solid #007bff; /* Bordure bleue à gauche */
    font-weight: 500;
}

.notification-item.unread:hover {
    background-color: #e6f2ff;
}

/* Indicateur de non-lu */
.unread-indicator {
    color: #007bff;
    font-size: 1.2rem;
    margin-right: 8px;
    animation: pulse 1.5s infinite;
}

/* Styles pour les notifications lues */
.notification-item.read {
    background-color: #fafafa;
    color: #777;
    border-left: 3px solid #ccc;
}

.notification-item.read:hover {
    background-color: #f0f0f0;
}

/* Contenu de la notification */
.notification-content {
    display: flex;
    align-items: flex-start;
    flex: 1;
}

.notification-text {
    flex: 1;
}

.notification-text strong {
    display: block;
    margin-bottom: 4px;
    color: inherit;
}

.notification-text p {
    margin: 0;
    font-size: 0.85rem;
    line-height: 1.3;
}

/* Séparateur entre lues et non lues */
.notification-separator {
    padding: 5px 0;
}

.notification-separator hr {
    border: none;
    border-top: 1px dashed #ddd;
    margin: 5px 15px;
}

/* Animation pour l'indicateur */
@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.5;
    }
}

/* Animations (inchangées) */
@keyframes pulse {
    0% {
     transform: scale(1);
     box-shadow: 0 0 0 0 rgba(255, 68, 68, 0.7);
    }
    50% {
     transform: scale(1.05);
     box-shadow: 0 0 0 5px rgba(255, 68, 68, 0);
    }
    100% {
     transform: scale(1);
     box-shadow: 0 0 0 0 rgba(255, 68, 68, 0);
    }
}
</style>