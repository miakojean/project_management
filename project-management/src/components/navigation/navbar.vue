<template>
    <nav>
        <div class="research__box">
            <researchfamily/>
        </div>
        <addButton @click="handleAddClick"/>
        <div class="btn__frame">
            <!-- Icône de notification avec bulle -->
            <div class="notification-wrapper" @click="handleNotificationClick">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1" stroke="currentColor" class="size-8">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
                </svg>
                <!-- Bulle de notification -->
                <span v-if="notificationCount > 0" class="notification-bubble">
                    {{ notificationCount > 99 ? '99+' : notificationCount }}
                </span>
            </div>
        </div>
    </nav>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import researchfamily from '../input/researchfamily.vue';
import addButton from '../button/addButton.vue';
import { useRouter } from 'vue-router';

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

        // Réactives
        const notificationCount = ref(0);
        const isLoading = ref(false);

        // Méthodes API
        const loadNotifications = async () => {
            isLoading.value = true;
            try {
                // Simuler un appel API
                const response = await fetch('/api/notifications/count');
                const data = await response.json();
                notificationCount.value = data.count;
                
                return { 
                    success: true, 
                    count: data.count 
                };
            } catch (error) {
                console.error('Erreur chargement notifications:', error);
                return { 
                    success: false, 
                    error: error.message 
                };
            } finally {
                isLoading.value = false;
            }
        };

        const addNotification = async (notificationData) => {
            try {
                // Simuler un appel API
                const response = await fetch('/api/notifications', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(notificationData)
                });
                const data = await response.json();
                
                notificationCount.value++;
                
                return { 
                    success: true, 
                    data: data 
                };
            } catch (error) {
                console.error('Erreur ajout notification:', error);
                return { 
                    success: false, 
                    error: error.message 
                };
            }
        };

        const markNotificationsAsRead = async () => {
            if (notificationCount.value === 0) {
                return { 
                    success: true, 
                    message: 'Aucune notification à marquer comme lue' 
                };
            }

            try {
                const response = await fetch('/api/notifications/mark-as-read', {
                    method: 'PUT'
                });
                const data = await response.json();
                const previousCount = notificationCount.value;
                notificationCount.value = 0;
                
                return { 
                    success: true, 
                    data: data,
                    clearedCount: previousCount
                };
            } catch (error) {
                console.error('Erreur marquage notifications:', error);
                return { 
                    success: false, 
                    error: error.message 
                };
            }
        };

        const getNotificationDetails = async () => {
            try {
                const response = await fetch('/api/notifications');
                const data = await response.json();
                
                return { 
                    success: true, 
                    data: data,
                    count: data.length
                };
            } catch (error) {
                console.error('Erreur détails notifications:', error);
                return { 
                    success: false, 
                    error: error.message 
                };
            }
        };

        // Gestion des événements
        const handleNotificationClick = async () => {
            if (notificationCount.value > 0) {
                const result = await markNotificationsAsRead();
                if (result.success) {
                    emit('notifications-cleared', result.clearedCount);
                }
            }
            
            emit('notification-click', {
                count: notificationCount.value,
                hasUnread: notificationCount.value > 0
            });
        };

        const handleAddClick = () => {
            emit('add-click');
            router.push('/customer')
        };

        // Méthodes utilitaires
        const simulateNotification = async (type = 'info', message = 'Nouvelle notification') => {
            const notificationData = {
                type: type,
                message: message,
                timestamp: new Date().toISOString(),
                read: false
            };

            const result = await addNotification(notificationData);
            if (result.success) {
                emit('notification-added', result.data);
            }
            return result;
        };

        const clearNotifications = async () => {
            const result = await markNotificationsAsRead();
            return result;
        };

        const refreshNotifications = async () => {
            const result = await loadNotifications();
            return result;
        };

        const getNotificationStatus = () => {
            return {
                count: notificationCount.value,
                hasNotifications: notificationCount.value > 0,
                isLoading: isLoading.value,
                displayCount: notificationCount.value > 99 ? '99+' : notificationCount.value.toString()
            };
        };

        // Watcher pour les changements du compteur
        watch(notificationCount, (newCount, oldCount) => {
            if (newCount !== oldCount) {
                emit('notification-count-changed', {
                    newCount,
                    oldCount,
                    hasIncreased: newCount > oldCount
                });
            }
        });

        // Lifecycle
        onMounted(() => {
            loadNotifications();
        });

        // Retour des éléments exposés
        return {
            // Réactives
            router,
            notificationCount,
            isLoading,
            
            // Méthodes API
            loadNotifications,
            addNotification,
            markNotificationsAsRead,
            getNotificationDetails,
            
            // Gestion des événements
            handleNotificationClick,
            handleAddClick,
            
            // Méthodes utilitaires
            simulateNotification,
            clearNotifications,
            refreshNotifications,
            getNotificationStatus
        };
    }
}
</script>

<style scoped>
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

input{
    border: 1px solid #dbdbdb;
    border-radius: 0.5rem;
    padding: 0.7rem;
    width: 100%;
}

ul{
    display:flex;
    align-items: center;
    gap: 1rem;
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

/* Styles pour la bulle de notification */
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

/* Animation pour attirer l'attention */
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

/* Version alternative sans animation */
.notification-bubble.no-animation {
    animation: none;
}

/* Différentes couleurs selon le nombre de notifications */
.notification-bubble.low {
    background: #4CAF50; /* Vert pour peu de notifications */
}

.notification-bubble.medium {
    background: #FF9800; /* Orange pour un nombre moyen */
}

.notification-bubble.high {
    background: #ff4444; /* Rouge pour beaucoup de notifications */
}
</style>