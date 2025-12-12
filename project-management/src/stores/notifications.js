import { defineStore } from "pinia";
import { ref, computed } from 'vue';
import api from '@/_services/api'; // Service API (e.g., Axios instance)

export const useNotificationStore = defineStore('notif', () => {
    
    // ===================================
    // 1. ÉTAT (State)
    // ===================================

    /** @type {import('vue').Ref<number>} Le nombre de notifications non lues. */
    const unreadCount = ref(0);
    
    /** @type {import('vue').Ref<Array<Object>>} La liste détaillée des notifications. */
    const notifications = ref([]);
    
    /** @type {import('vue').Ref<boolean>} Indicateur de chargement. */
    const isLoading = ref(false);

    // ===================================
    // 2. GETTERS (Computed)
    // ===================================

    /** Vérifie s'il y a des notifications non lues. */
    const hasUnread = computed(() => unreadCount.value > 0);

    /** Renvoie le nombre formaté (ex: 12, ou '99+' si > 99). */
    const displayCount = computed(() => {
        return unreadCount.value > 99 ? '99+' : unreadCount.value.toString();
    });

    /** Renvoie uniquement les notifications non lues */
    const unreadNotifications = computed(() => {
        return notifications.value.filter(n => !n.is_read);
    });

    // ===================================
    // 3. ACTIONS
    // ===================================

    /** * Récupère le compte des notifications non lues depuis le backend.
     * C'est la fonction principale utilisée pour rafraîchir la bulle.
     */
    const loadUnreadCount = async () => {
        isLoading.value = true;
        try {
            // Supposons que cet endpoint renvoie directement le compte ou un objet avec 'count'
            const response = await api.get('/notification/notif-index'); 
            
            // Adapter la lecture de la réponse selon la structure réelle de votre backend
            const count = response.data.count || 0; 

            unreadCount.value = count;

            return count;

        } catch (error) {
            console.error("Erreur Pinia - chargement du compte de notifications:", error);
            // Ne pas modifier le compte en cas d'erreur pour éviter une désynchronisation
        } finally {
            isLoading.value = false;
        }
    };

    /** * Récupère la liste complète des notifications pour le dropdown.
     */
    const loadNotifications = async () => {
        isLoading.value = true;
        try {
            const response = await api.get('/notification/notif-index'); 
            
            // Assurez-vous que la réponse contient les notifications et potentiellement le compte non lu
            const data = response.data.data;
            notifications.value = data.dossiers || response.data; // Adapter si la réponse est directe ou structurée
            
            // Tenter de mettre à jour le compte par la même occasion
            if (data.metadata && data.metadata.count !== undefined) {
                 // Supposons que le backend renvoie le count total et on filtre les non-lus
                 unreadCount.value = unreadNotifications.value.length; 
            } else {
                // Si l'endpoint principal donne la liste, on compte les non-lus
                unreadCount.value = notifications.value.filter(n => !n.is_read).length;
            }

            return notifications.value;
        } catch (error) {
            console.error("Erreur Pinia - chargement de la liste de notifications:", error);
            notifications.value = [];
        } finally {
            isLoading.value = false;
        }
    };

    /** * Marque toutes les notifications non lues comme lues et met à jour le store.
     */
    const markAllAsRead = async () => {
        if (!hasUnread.value) return 0;
        
        try {
            // Endpoint pour marquer tout comme lu
            const response = await api.put('/api/notifications/mark-as-read'); 

            const clearedCount = unreadCount.value;
            
            // Mettre à jour l'état local après succès
            unreadCount.value = 0;
            // Optionnel : mettre à jour le statut dans la liste locale
            notifications.value.forEach(n => n.is_read = true);

            return clearedCount;
        } catch (error) {
            console.error("Erreur Pinia - marquage des notifications:", error);
            return 0;
        }
    };
    
    // Optionnel : Fonction pour ajouter une notification (si vous utilisez les WebSockets ou le polling en temps réel)
    const addNotification = (newNotification) => {
        notifications.value.unshift(newNotification);
        if (!newNotification.is_read) {
            unreadCount.value++;
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
        addNotification,
    };
});