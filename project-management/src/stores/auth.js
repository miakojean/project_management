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
    const userProfile = computed(() => user.value || {}); 

    // --- ACTIONS PRIVÉES (Gestion du cache) ---
    
    function cacheUser(userData) {
        try {
            const safeData = {
                id: userData.id,
                first_name: userData.first_name,
                last_name: userData.last_name,
                email: userData.email,
                category_title: userData.category_title
            };
            localStorage.setItem('cachedUser', JSON.stringify(safeData));
            user.value = userData;
            console.log('💾 Utilisateur mis en cache:', safeData);
        } catch (e) {
            console.error('❌ Erreur sauvegarde cache utilisateur:', e);
        }
    }

    function loadUserFromCache() {
        try {
            const cached = localStorage.getItem('cachedUser');
            if (cached) {
                user.value = JSON.parse(cached);
                console.log('⚡ Utilisateur chargé depuis le cache');
                return true;
            }
        } catch (e) {
            console.error('❌ Erreur chargement cache:', e);
            localStorage.removeItem('cachedUser');
        }
        return false;
    }

    function clearUserCache() {
        localStorage.removeItem('cachedUser');
        sessionStorage.removeItem('cachedUser');
        user.value = null;
        console.log('🗑️ Cache utilisateur nettoyé');
    }

    // --- ACTIONS PUBLIQUES ---

    async function initializeAuth() {
        if (isInitialized.value) {
            console.log('✅ Auth déjà initialisé');
            return;
        }
        
        console.log('🚀 Initialisation de l\'authentification...');
        
        // 1. Charger depuis le cache pour affichage immédiat
        const hasCachedUser = loadUserFromCache();
        
        // 2. Vérifier si on a un token
        const token = localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
        
        if (token) {
            console.log('🔑 Token trouvé, vérification en cours...');
            
            // 3. Vérifier que le token est toujours valide
            try {
                await fetchCurrentUser();
                console.log('✅ Token valide, utilisateur chargé');
            } catch (e) {
                console.error('❌ Token invalide, déconnexion:', e);
                // Si le token est invalide, on déconnecte
                await logout();
            }
        } else {
            console.log('⚠️ Pas de token trouvé');
            // Pas de token, on nettoie tout
            clearUserCache();
        }
        
        isInitialized.value = true;
        console.log('✅ Initialisation terminée');
    }

    async function fetchCurrentUser() {
        isLoading.value = true;
        error.value = null;
        
        try {
            console.log('👤 Récupération des données utilisateur...');
            const userData = await authService.getCurrentUser();
            
            // ✅ Mettre à jour Pinia ET le cache
            cacheUser(userData);
            console.log('✅ Utilisateur récupéré:', userData);
            
            return user.value;
        } catch (err) {
            console.error('❌ Erreur récupération utilisateur:', err);
            error.value = err.message;
            throw err;
        } finally {
            isLoading.value = false;
        }
    }

    async function login(credentials) {
        isLoading.value = true;
        error.value = null;
        
        try {
            console.log('🔐 Connexion en cours...');
            
            // ✅ 1. Effectuer le login
            const response = await authService.login(credentials);
            console.log('✅ Login réussi');
            
            // ✅ 2. Attendre un peu pour s'assurer que les tokens sont stockés
            await new Promise(resolve => setTimeout(resolve, 200));
            
            // ✅ 3. Récupérer les infos utilisateur
            if (response.data && response.data.user) {
                console.log('✅ Utilisateur reçu dans la réponse login');
                cacheUser(response.data.user);
            } else {
                console.log('📡 Récupération des infos utilisateur...');
                await fetchCurrentUser();
            }
            
            console.log('✅ Connexion terminée avec succès');
            return response;
            
        } catch (err) {
            console.error('❌ Erreur lors de la connexion:', err);
            error.value = err.response?.data?.message || err.message || 'Erreur de connexion';
            
            // ✅ Nettoyer en cas d'erreur
            clearUserCache();
            localStorage.removeItem('authToken');
            localStorage.removeItem('refresh');
            
            throw err;
        } finally {
            isLoading.value = false;
        }
    }

    async function logout() {
        console.log('🚪 Déconnexion...');
        
        try {
            await authService.logout();
        } catch (err) {
            console.error('❌ Erreur lors de la déconnexion:', err);
        } finally {
            // ✅ Nettoyage complet
            clearUserCache();
            isInitialized.value = false;
            
            // Nettoyer aussi les tokens
            localStorage.removeItem('authToken');
            localStorage.removeItem('refresh');
            sessionStorage.removeItem('authToken');
            sessionStorage.removeItem('refresh');
            
            console.log('✅ Déconnexion terminée');
        }
    }

    return {
        // State
        user,
        isLoading,
        error,
        
        // Getters
        isAuthenticated,
        userProfile,
        
        // Actions
        login,
        logout,
        initializeAuth,
        fetchCurrentUser
    };
});