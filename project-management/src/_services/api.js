import axios from "axios"
import router from "@/router"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    withCredentials: true,  // ✅ ESSENTIEL pour les cookies
})

// --- INTERCEPTEUR DE REQUÊTE ---
api.interceptors.request.use(
    (config) => {
        // console.log('📤 Requête:', config.method.toUpperCase(), config.url);
        // console.log('📤 Requête:', config.method.toUpperCase(), config.url);
        
        // Timestamp anti-cache pour les GET (optionnel)
        if (config.method === 'get') {
            config.params = {
                ...config.params,
                _t: Date.now()
            };
        }
        
        // ✅ PAS besoin d'ajouter un header Authorization manuellement
        // Le cookie `access_token` (HttpOnly) sera envoyé automatiquement
        // Le middleware backend déplacera le cookie vers l'en-tête Authorization
        
        return config;
    },
    (error) => {
        // console.error('Erreur intercepteur requête:', error);
        return Promise.reject(error);
    }
);

// --- INTERCEPTEUR DE RÉPONSE ---
api.interceptors.response.use(
    (response) => {
        // console.log('Réponse reçue:', response.config.url, response.status);
        return response;
    },
    async (error) => {
        const originalRequest = error.config;

        /* console.log('Erreur intercepteur réponse:', {
            url: originalRequest?.url,
            status: error.response?.status,
            message: error.message
        });*/

        // ✅ Gestion du 401 (session expirée)
        if (error.response?.status === 401 &&
            !originalRequest._retry &&
            !originalRequest.url.includes('/account/token/refresh/') &&
            !originalRequest.url.includes('/account/login')
        ) {
            originalRequest._retry = true;

            // console.log('🔄 Tentative de refresh token via cookie...');

            try {
                // Le refresh token est dans un cookie HttpOnly
                // Il sera envoyé automatiquement avec `withCredentials: true`
                await api.post('/account/token/refresh/');
                // console.log('Token refreshé avec succès via cookie');
                
                // Relancer la requête originale
                return api(originalRequest);
                
            } catch (refreshError) {
                // console.error('❌ Échec du refresh token:', refreshError);
                
                // Redirection vers login
                if (router.currentRoute.value.path !== '/login') {
                    router.push('/login?session_expired=true');
                }
                return Promise.reject(refreshError);
            }
        }

        // Gestion des autres erreurs
        if (error.response?.status === 403) {
            // console.error('Accès refusé (403)');
            router.push('/unauthorized');
        }
        
        return Promise.reject(error);
    }
);

// ============================================================
// 🍪 SERVICE D'AUTHENTIFICATION COOKIES-ONLY
// ============================================================

export const authService = {
    login: async (credentials) => {
        try {
            // console.log('🔑 Tentative de login...');
            
            // ✅ Login standard - les cookies seront automatiquement définis par le backend
            const response = await api.post('/account/login', credentials);
            
            // console.log('✅ Login réussi');
            return response.data; // Retourne les données utilisateur
            
        } catch (error) {
            // console.error('❌ Erreur login:', error.response?.data || error.message);
            throw error;
        }
    },
    
    logout: async () => {
        try {
            // console.log('🚪 Déconnexion en cours...');
            // ✅ Le backend supprimera les cookies
            await api.post('/account/logout');
            // console.log('✅ Déconnexion API réussie');
            
        } catch (error) {
            // console.error('❌ Erreur logout:', error);
            // On continue quand même pour nettoyer côté frontend
        } finally {
            // Redirection gérée par le store ou le composant
            // console.log('✅ Déconnexion terminée côté frontend');
        }
    },
    
    getCurrentUser: async () => {
        try {
            // console.log('👤 Récupération utilisateur actuel...');
            
            // ✅ Le cookie access_token (HttpOnly) est envoyé automatiquement
            const response = await api.get('/account/me');
            
            // console.log('✅ Utilisateur récupéré');
            
            // Format de réponse attendu: { user: {...} } ou directement l'objet user
            return response.data.user || response.data;
            
        } catch (error) {
            // console.error('❌ Erreur récupération utilisateur:', error.response?.data || error.message);
            
            // Si erreur 401, la redirection est déjà gérée par l'intercepteur
            throw error;
        }
    }
};

// ✅ Fonction utilitaire pour vérifier l'état de l'authentification
export const checkAuth = async () => {
    try {
        await authService.getCurrentUser();
        return true;
    } catch {
        return false;
    }
};

export default api;