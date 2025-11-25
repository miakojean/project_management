import axios from "axios"
import router from "@/router"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    withCredentials: true
})

// Service de stockage
const storage = {
    getToken: () => {
        // ✅ Chercher d'abord dans localStorage (plus fiable)
        return localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
    },
    getRefreshToken: () => {
        return localStorage.getItem('refresh') || sessionStorage.getItem('refresh');
    },
    setTokens: (authToken, refreshToken) => {
        // ✅ Stocker dans localStorage par défaut
        localStorage.setItem('authToken', authToken);
        if (refreshToken) {
            localStorage.setItem('refresh', refreshToken);
        }
        console.log('✅ Tokens stockés:', { hasToken: !!authToken, hasRefresh: !!refreshToken });
    },
    clearTokens: () => {
        sessionStorage.removeItem('authToken');
        sessionStorage.removeItem('refresh');
        localStorage.removeItem('authToken');
        localStorage.removeItem('refresh');
        console.log('🗑️ Tokens supprimés');
    }
};

// --- INTERCEPTEUR DE REQUÊTE ---
api.interceptors.request.use(
    (config) => {
        const token = storage.getToken();
        
        // Liste des URLs publiques (pas besoin de token)
        const publicEndpoints = [
            '/account/login',
            '/account/register',
            '/account/token/refresh'
        ];

        const isPublicEndpoint = publicEndpoints.some(endpoint => config.url.includes(endpoint));

        // ✅ Ajouter le token seulement si on n'est pas sur un endpoint public
        if (token && !isPublicEndpoint) {
            config.headers.Authorization = `Bearer ${token}`;
            console.log('🔑 Token ajouté à la requête:', config.url);
        }
        
        // Timestamp anti-cache pour les GET
        if (config.method === 'get') {
            config.params = {
                ...config.params,
                _t: Date.now()
            };
        }
        
        return config;
    },
    (error) => {
        console.error('❌ Erreur intercepteur requête:', error);
        return Promise.reject(error);
    }
);

// --- INTERCEPTEUR DE RÉPONSE ---
api.interceptors.response.use(
    (response) => {
        console.log('✅ Réponse reçue:', response.config.url, response.status);
        return response;
    },
    async (error) => {
        const originalRequest = error.config;

        console.log('❌ Erreur intercepteur réponse:', {
            url: originalRequest?.url,
            status: error.response?.status,
            message: error.message
        });

        // ✅ Gestion du 401 (token expiré)
        if (error.response?.status === 401 &&
            !originalRequest._retry &&
            !originalRequest.url.includes('/account/token/refresh') &&
            !originalRequest.url.includes('/account/login')
        ) {
            originalRequest._retry = true;
            const refreshToken = storage.getRefreshToken();

            console.log('🔄 Tentative de refresh token...');

            if (refreshToken) {
                try {
                    const refreshResponse = await axios.post(
                        `${API_BASE_URL}/account/token/refresh`,
                        { refresh: refreshToken },
                        { 
                            withCredentials: true,
                            timeout: 5000 
                        }
                    );

                    const newAccessToken = refreshResponse.data.access;
                    
                    // ✅ Stocker le nouveau token
                    storage.setTokens(newAccessToken, refreshToken);
                    console.log('✅ Token refreshé avec succès');

                    // ✅ Relancer la requête avec le nouveau token
                    originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                    return api(originalRequest);
                    
                } catch (refreshError) {
                    console.error('❌ Échec du refresh token:', refreshError);
                    
                    // ✅ Déconnexion si le refresh échoue
                    storage.clearTokens();
                    
                    if (router.currentRoute.value.path !== '/login') {
                        router.push('/login?session_expired=true');
                    }
                    return Promise.reject(refreshError);
                }
            } else {
                console.log('❌ Pas de refresh token disponible');
                storage.clearTokens();
                if (router.currentRoute.value.path !== '/login') {
                    router.push('/login');
                }
            }
        }

        // ✅ Gestion des autres erreurs
        if (error.response?.status === 403) {
            console.error('🚫 Accès refusé (403)');
        }
        
        if (error.response?.status >= 500) {
            console.error('🔥 Erreur serveur (500+)');
        }

        return Promise.reject(error);
    }
);

// Fonctions utilitaires pour l'authentification
export const authService = {
    login: async (credentials) => {
        try {
            console.log('🔐 Tentative de login...');
            const response = await api.post('/account/login', credentials);
            
            console.log('✅ Réponse login reçue:', response.data);
            
            if (response.data.access || response.data.access_token) {
                const token = response.data.access || response.data.access_token;
                const refreshToken = response.data.refresh || response.data.refresh_token;
                
                // ✅ Stocker les tokens AVANT toute autre requête
                storage.setTokens(token, refreshToken);
                
                // ✅ Petit délai pour s'assurer que le token est bien stocké
                await new Promise(resolve => setTimeout(resolve, 100));
                
                console.log('✅ Login réussi, tokens stockés');
                return response;
            }
            
            throw new Error('Token non reçu dans la réponse');
            
        } catch (error) {
            console.error('❌ Erreur login:', error.response?.data || error.message);
            throw error;
        }
    },
    
    logout: async () => {
        try {
            console.log('🚪 Déconnexion en cours...');
            const refresh = storage.getRefreshToken();
            if (refresh) {
                await api.post('/account/logout', { refresh });
            }
        } catch (error) {
            console.error('❌ Erreur logout:', error);
        } finally {
            storage.clearTokens();
            console.log('✅ Déconnexion terminée');
            router.push('/login');
        }
    },
    
    getCurrentUser: async () => {
        try {
            console.log('👤 Récupération utilisateur actuel...');
            
            // ✅ Vérifier qu'on a bien un token avant de faire la requête
            const token = storage.getToken();
            if (!token) {
                throw new Error('Pas de token disponible');
            }
            
            const response = await api.get('/account/me');
            
            console.log('✅ Utilisateur récupéré:', response.data);
            
            // Le backend retourne { user: {...} }
            if (response.data.user) {
                return response.data.user;
            }
            
            // Au cas où le backend retournerait directement l'objet user
            return response.data;
            
        } catch (error) {
            console.error('❌ Erreur récupération utilisateur:', error.response?.data || error.message);
            
            // Si erreur 401, on déconnecte
            if (error.response?.status === 401) {
                console.log('🚫 Token invalide, déconnexion...');
                storage.clearTokens();
                router.push('/login');
            }
            
            throw error;
        }
    },
    
    isAuthenticated: () => {
        const hasToken = !!storage.getToken();
        console.log('🔍 Vérification authentification:', hasToken);
        return hasToken;
    }
};

export default api;