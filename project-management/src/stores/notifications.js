import { defineStore } from "pinia";
import { ref, computed } from 'vue';
import api from '@/_services/api';

export const useNotificationStore = defineStore('notif', () => {
    
    // ===================================
    // 1. ÉTAT (State)
    // ===================================
    const unreadCount = ref(0);
    const notifications = ref([]);
    const isLoading = ref(false);

    // ===================================
    // 2. GETTERS (Computed)
    // ===================================
    const hasUnread = computed(() => unreadCount.value > 0);
    const displayCount = computed(() => {
        return unreadCount.value > 99 ? '99+' : unreadCount.value.toString();
    });
    const unreadNotifications = computed(() => {
        return notifications.value.filter(n => !n.is_read_for_current_user);
    });

    // ===================================
    // 3. ACTIONS
    // ===================================
    
    /**
     * Récupère uniquement le compte des notifications non lues
     * Utilisée pour la bulle de notification
     */
    const loadUnreadCount = async () => {
        try {
            // Appel l'API qui retourne les métadonnées avec les counts
            const response = await api.get('notification/notif-index'); // Assurez-vous que c'est la bonne URL
            
            // Votre API Django retourne un format avec 'metadata'
            if (response.data.metadata) {
                unreadCount.value = response.data.metadata.unread_count || 0;
                console.log('notifications', response.data)
                return unreadCount.value;
            }
            
            // Fallback si l'API a un format différent
            unreadCount.value = response.data.unread_count || 0;
            console.log('notifications', response.data)
            return unreadCount.value;
            
        } catch (error) {
            console.error("Erreur - chargement du compte de notifications:", error);
            return 0;
        }
    };

    /**
     * Récupère la liste complète des notifications avec détails
     * Utilisée pour le dropdown
     */
    const loadNotifications = async () => {
        isLoading.value = true;
        try {
            const response = await api.get('notification/notif-index');
            
            // Votre API retourne les notifications dans 'notifications'
            if (response.data.notifications) {
                notifications.value = response.data.notifications;
                
                // Met à jour aussi le compteur depuis les métadonnées
                if (response.data.metadata) {
                    unreadCount.value = response.data.metadata.unread_count || 0;
                } else {
                    // Fallback: compte les non-lues dans la liste
                    unreadCount.value = notifications.value.filter(
                        n => !n.is_read_for_current_user
                    ).length;
                }
            }
            console.log('notifications', response.data)
            
            return notifications.value;
        } catch (error) {
            console.error("Erreur - chargement de la liste de notifications:", error);
            notifications.value = [];
            return [];
        } finally {
            isLoading.value = false;
        }
    };

    /**
     * Marque toutes les notifications non lues comme lues
     */
    const markAllAsRead = async () => {
        if (!hasUnread.value) return 0;
        
        try {
            // Utilise la méthode POST sur l'endpoint de liste
            const response = await api.post('notification/notif-index');
            
            // Votre API retourne 'marked_read' dans la réponse
            const markedRead = response.data.marked_read || 0;
            
            // Met à jour l'état local
            unreadCount.value = 0;
            // Met à jour le statut de lecture dans la liste locale
            notifications.value.forEach(n => {
                n.is_read_for_current_user = true;
            });
            
            return markedRead;
        } catch (error) {
            console.error("Erreur - marquage des notifications:", error);
            return 0;
        }
    };
    
    /**
     * Marque une notification spécifique comme lue
     */
    const markAsRead = async (notificationId) => {
        try {
            // Utilise PUT sur l'endpoint de détail
            const response = await api.put(`/api/notifications/${notificationId}/`, {
                is_read: true
            });
            
            // Met à jour l'état local
            const notification = notifications.value.find(n => n.id === notificationId);
            if (notification) {
                notification.is_read_for_current_user = true;
            }
            
            // Décrémente le compteur si la notification n'était pas déjà lue
            if (notification && !notification.is_read_for_current_user) {
                unreadCount.value = Math.max(0, unreadCount.value - 1);
            }
            
            return true;
        } catch (error) {
            console.error("Erreur - marquage d'une notification:", error);
            return false;
        }
    };

    // ===================================
    // EXPOSITION DES ÉLÉMENTS DU STORE
    // ===================================
    return {
        // État
        unreadCount,
        notifications,
        isLoading,

        // Getters
        hasUnread,
        displayCount,
        unreadNotifications,

        // Actions
        loadUnreadCount,
        loadNotifications,
        markAllAsRead,
        markAsRead,
    };
});