// src/stores/auth.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService } from '@/_services/api';

export const useAuthStore = defineStore('auth', () => {
    // --- STATE ---
    const user = ref(null);
    const isLoading = ref(false);
    const error = ref(null);
    const isInitialized = ref(false);

    // --- GETTERS ---
    const isAuthenticated = computed(() => !!user.value);
    
    // Exemple d'accès direct aux attributs en cache
    const userProfile = computed(() => user.value || {}); 

    // --- ACTIONS PRIVÉES (Gestion du cache) ---
    
    // Sauvegarder l'user dans le storage
    function cacheUser(userData) {
        try {
            // On ne garde que les infos nécessaires, pas tout
            const safeData = {
                id: userData.id,
                first_name: userData.first_name,
                last_name: userData.last_name,
                email: userData.email,
                category_title: userData.category_title
                // Surtout PAS de password ici
            };
            sessionStorage.setItem('cachedUser', JSON.stringify(safeData));
            user.value = userData; // Mise à jour du state Pinia
        } catch (e) {
            console.error('Erreur sauvegarde cache utilisateur', e);
        }
    }

    // Récupérer l'user depuis le storage
    function loadUserFromCache() {
        try {
            const cached = sessionStorage.getItem('cachedUser');
            if (cached) {
                user.value = JSON.parse(cached);
                return true;
            }
        } catch (e) {
            sessionStorage.removeItem('cachedUser');
        }
        return false;
    }

    // Nettoyer le cache
    function clearUserCache() {
        sessionStorage.removeItem('cachedUser');
        user.value = null;
    }

    // --- ACTIONS PUBLIQUES ---

    async function initializeAuth() {
        if (isInitialized.value) return;
        
        // 1. D'abord, on essaie de charger depuis le cache pour un affichage immédiat
        const hasCachedUser = loadUserFromCache();
        if (hasCachedUser) {
            console.log('⚡ Utilisateur chargé depuis le cache (affichage rapide)');
        }

        const token = sessionStorage.getItem('authToken') || localStorage.getItem('authToken');
        
        if (token) {
            // 2. On lance quand même une requête pour vérifier que les données sont à jour (Hydratation)
            // C'est transparent pour l'utilisateur
            try {
                await fetchCurrentUser();
            } catch (e) {
                // Si le token est invalide, on nettoie tout
                if (!hasCachedUser) await logout(); 
            }
        } else {
             // Pas de token, on nettoie tout par sécurité
             clearUserCache();
        }
        
        isInitialized.value = true;
    }

    async function fetchCurrentUser() {
        isLoading.value = true;
        try {
            const userData = await authService.getCurrentUser();
            // On met à jour Pinia ET le Cache
            cacheUser(userData); 
            return user.value;
        } catch (err) {
            throw err;
        } finally {
            isLoading.value = false;
        }
    }

    async function login(credentials) {
        isLoading.value = true;
        try {
            const response = await authService.login(credentials);
            
            if (response.data && response.data.user) {
                // Si le login renvoie déjà l'user, on le cache direct
                cacheUser(response.data.user);
            } else {
                // Sinon on va le chercher
                await fetchCurrentUser();
            }
            
            return response;
        } catch (err) {
            throw err;
        } finally {
            isLoading.value = false;
        }
    }

    async function logout() {
        try {
            await authService.logout();
        } finally {
            // Nettoyage complet
            clearUserCache();
            isInitialized.value = false;
            // On nettoie aussi les tokens (géré dans api.js normalement, mais par sécurité)
            sessionStorage.removeItem('authToken');
            sessionStorage.removeItem('refresh');
        }
    }

    return {
        user,
        userProfile, // Nouveau getter pratique
        isLoading,
        isAuthenticated,
        login,
        logout,
        initializeAuth,
        fetchCurrentUser
    };
});