import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService } from '@/_services/api';
import { useRouter } from 'vue-router';
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

    // --- ACTIONS PRIVÉES (Cache utilisateur uniquement) ---
    
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
            user.value = safeData;
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
        loadUserFromCache();
        
        // 2. Vérifier si l'utilisateur est toujours connecté via l'API
        // ⚠️ Ne pas nettoyer automatiquement en cas d'erreur
        // L'intercepteur d'API gérera le refresh automatique
        if (user.value) {
            try {
                await fetchCurrentUser();
                console.log('✅ Session valide');
            } catch (error) {
                console.log('⚠️ Session potentiellement expirée, laissé à l\'intercepteur');
                // Ne pas nettoyer automatiquement - l'intercepteur gèrera
            }
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
            
            // Ne pas nettoyer le cache utilisateur automatiquement
            // L'intercepteur d'API gérera le refresh si nécessaire
            
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
            
            // ✅ 1. Effectuer le login (les cookies sont définis automatiquement)
            const response = await authService.login(credentials);
            console.log('✅ Login réussi');
            
            // ✅ 2. Récupérer et stocker les infos utilisateur
            if (response.user) {
                console.log('✅ Utilisateur reçu dans la réponse login');
                cacheUser(response.user);
            } else {
                console.log('📡 Récupération des infos utilisateur...');
                await fetchCurrentUser();
            }
            
            console.log('✅ Connexion terminée avec succès');
            return response;
            
        } catch (err) {
            console.error('❌ Erreur lors de la connexion:', err);
            
            // Extraire le message d'erreur du backend
            const errorData = err.response?.data || {};
            if (errorData.error) {
                error.value = errorData.error;
            } else if (errorData.message) {
                error.value = errorData.message;
            } else if (err.response?.status === 401) {
                error.value = 'Email ou mot de passe incorrect';
            } else {
                error.value = err.message || 'Erreur de connexion';
            }
            
            // Nettoyer le cache en cas d'erreur d'authentification
            clearUserCache();
            
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
            // ✅ 1. Appeler l'API de déconnexion (supprime les cookies côté serveur)
            await authService.logout();
            console.log('✅ Déconnexion API réussie');
        } catch (err) {
            if (!silent) {
                console.error('❌ Erreur lors de la déconnexion API:', err);
            }
            // Continuer quand même pour nettoyer côté client
        } finally {
            // ✅ 2. Nettoyage LOCAL seulement
            clearUserCache();
            
            // ✅ 3. Reset other stores
            try {
                const dossierStore = useDossierStore();
                if (dossierStore && typeof dossierStore.reset === 'function') {
                    dossierStore.reset();
                    console.log('🗑️ Cache dossier nettoyé via auth.logout');
                }
            } catch (e) {
                console.warn('⚠️ Impossible de réinitialiser dossierStore:', e);
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

    // ✅ Nouvelle fonction pour vérifier facilement l'état
    async function checkAuth() {
        try {
            await fetchCurrentUser();
            return true;
        } catch {
            return false;
        }
    }

    // ✅ Fonction pour réinitialiser l'erreur
    function clearError() {
        error.value = null;
    }

    return {
        // State
        user,
        isLoading,
        error,
        isInitialized,
        
        // Getters
        isAuthenticated,
        userProfile,
        
        // Actions
        login,
        logout,
        initializeAuth,
        fetchCurrentUser,
        checkAuth,
        clearError
    };
});