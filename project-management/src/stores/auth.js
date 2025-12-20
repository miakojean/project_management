// src/stores/auth.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService} from '@/_services/api'; // Importez aussi api si besoin
import { useRouter } from 'vue-router';
import api from '@/_services/api';
import { useDossierStore } from '@/stores/dossierStore';

export const useAuthStore = defineStore('auth', () => {
    // --- ROUTER ---
    const router = useRouter();
    
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
                nom_complet: userData.nom_complet,
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

    function clearAuthTokens() {
        // Supprimer TOUS les tokens possibles
        const tokensToRemove = [
            'authToken', 'access', 'access_token',
            'refresh', 'refresh_token',
            'token', 'jwt_token'
        ];
        
        tokensToRemove.forEach(tokenKey => {
            localStorage.removeItem(tokenKey);
            sessionStorage.removeItem(tokenKey);
        });
        
        console.log('🗑️ Tokens d\'authentification nettoyés');
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
        const token = localStorage.getItem('authToken') || 
                      localStorage.getItem('access') || 
                      sessionStorage.getItem('authToken');
        
        if (token) {
            console.log('🔑 Token trouvé, vérification en cours...');
            
            // 3. Vérifier que le token est toujours valide
            try {
                await fetchCurrentUser();
                console.log('✅ Token valide, utilisateur chargé');
            } catch (e) {
                console.error('❌ Token invalide, déconnexion:', e);
                // Si le token est invalide, on déconnecte
                await logout({ silent: true }); // Déconnexion silencieuse
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
            console.log('✅ Login réussi', response.data);
            
            // ✅ 2. Stocker les tokens dans localStorage
            if (response.data.access) {
                localStorage.setItem('access', response.data.access);
                console.log('🔑 Access token stocké');
            }
            if (response.data.refresh) {
                localStorage.setItem('refresh', response.data.refresh);
                console.log('🔄 Refresh token stocké');
            }
            
            // ✅ 3. Récupérer et stocker les infos utilisateur
            if (response.data.user) {
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
            await logout({ silent: true });
            
            throw err;
        } finally {
            isLoading.value = false;
        }
    }

    async function logout(options = {}) {
        const { silent = false, redirect = true } = options;
        
        if (!silent) {
            console.log('🚪 Déconnexion...');
        }
        
        try {
            // ✅ 1. Récupérer le refresh token pour le blacklist côté serveur
            const refreshToken = localStorage.getItem('refresh') || 
                                sessionStorage.getItem('refresh');
            
            // ✅ 2. Appeler l'API de déconnexion si on a un token
            if (refreshToken) {
                try {
                    await api.post('account/logout', { 
                        refresh: refreshToken 
                    });
                    console.log('✅ Token blacklisté côté serveur');
                } catch (err) {
                    console.warn('⚠️ Impossible de blacklister le token:', err.message);
                    // On continue même si l'appel échoue
                }
            }
        } catch (err) {
            if (!silent) {
                console.error('❌ Erreur lors de la déconnexion API:', err);
            }
        } finally {
            // ✅ 3. Nettoyage complet LOCAL (toujours exécuté)
            clearUserCache();
            clearAuthTokens();
            // Reset other stores that may hold cached data
            try {
                const dossierStore = useDossierStore();
                if (dossierStore && typeof dossierStore.reset === 'function') {
                    dossierStore.reset();
                    console.log('🗑️ Cache dossier nettoyé via auth.logout');
                }
            } catch (e) {
                console.warn('⚠️ Impossible de réinitialiser dossierStore pendant la déconnexion:', e);
            }
            
            // ✅ 4. Réinitialiser l'état
            isInitialized.value = false;
            error.value = null;
            
            if (!silent) {
                console.log('✅ Déconnexion terminée');
                
                // ✅ 5. Redirection vers la page de login
                if (redirect) {
                    setTimeout(() => {
                        router.push('/login');
                    }, 100);
                }
            }
        }
    }

    return {
        // State
        user,
        isLoading,
        error,
        isInitialized, // Exportez aussi isInitialized si besoin
        
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