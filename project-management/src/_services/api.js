import axios from "axios"
import router from "@/router"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000, // 10s
    withCredentials: true
})

// Service de stockage
const storage = {
    getToken: () => {
        return sessionStorage.getItem('authToken') || localStorage.getItem('authToken');
    },
    getRefreshToken: () => {
        return sessionStorage.getItem('refresh') || localStorage.getItem('refresh');
    },
    setTokens: (authToken, refreshToken) => {
        sessionStorage.setItem('authToken', authToken);
        if (refreshToken) {
            sessionStorage.setItem('refresh', refreshToken);
        }
    },
    clearTokens: () => {
        sessionStorage.removeItem('authToken');
        sessionStorage.removeItem('refresh');
        localStorage.removeItem('authToken');
        localStorage.removeItem('refresh');
    }
};

// --- INTERCEPTEUR DE REQUÊTE (C'est ici que la correction est appliquée) ---
api.interceptors.request.use(
    (config) => {
        const token = storage.getToken();
        
        // Liste des URLs où il ne faut PAS envoyer le token Bearer
        // pour éviter l'erreur "token_not_valid" sur des endpoints publics
        const publicEndpoints = [
            '/account/login',
            '/account/register',
            '/account/token/refresh'
        ];

        // Vérifie si l'URL actuelle fait partie des endpoints publics
        const isPublicEndpoint = publicEndpoints.some(endpoint => config.url.includes(endpoint));

        // On ajoute le token SEULEMENT si on n'est pas sur une page de login/refresh
        if (token && !isPublicEndpoint) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        
        // Ajouter un timestamp pour éviter le cache sur les GET
        if (config.method === 'get') {
            config.params = {
                ...config.params,
                _t: Date.now()
            };
        }
        
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// --- INTERCEPTEUR DE RÉPONSE ---
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Si erreur 401 et pas déjà tenté de refresh
        if (error.response?.status === 401 &&
            !originalRequest._retry &&
            !originalRequest.url.includes('/account/token/refresh') &&
            !originalRequest.url.includes('/account/login')
        ) {
            originalRequest._retry = true;
            const refreshToken = storage.getRefreshToken();

            if (refreshToken) {
                try {
                    // On utilise axios directement ici pour éviter de déclencher l'intercepteur principal
                    const refreshResponse = await axios.post(
                        `${API_BASE_URL}/account/token/refresh`,
                        { refresh: refreshToken },
                        { 
                            withCredentials: true,
                            timeout: 5000 
                        }
                    );

                    const newAccessToken = refreshResponse.data.access;
                    
                    // Stocker le nouveau token
                    storage.setTokens(newAccessToken, refreshToken);

                    // Mettre à jour le header et relancer la requête originale
                    originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                    return api(originalRequest);
                    
                } catch (refreshError) {
                    console.error('Refresh token failed:', refreshError);
                    
                    // Déconnexion si le refresh échoue
                    storage.clearTokens();
                    
                    // Redirection vers login avec message
                    if (router.currentRoute.value.path !== '/login') {
                        router.push('/login?session_expired=true');
                    }
                    return Promise.reject(refreshError);
                }
            } else {
                // Pas de refresh token disponible
                storage.clearTokens();
                if (router.currentRoute.value.path !== '/login') {
                    router.push('/login');
                }
            }
        }

        // Logs d'erreurs optionnels
        if (error.response?.status === 403) {
            console.error('Accès refusé (403)');
        }
        
        if (error.response?.status >= 500) {
            console.error('Erreur serveur (500)');
        }

        return Promise.reject(error);
    }
);

// Fonctions utilitaires pour l'authentification
export const authService = {
    login: async (credentials) => {
        try {
            const response = await api.post('/account/login', credentials);
            
            if (response.data.access || response.data.access_token) {
                const token = response.data.access || response.data.access_token;
                const refreshToken = response.data.refresh || response.data.refresh_token;
                
                storage.setTokens(token, refreshToken);
                return response;
            }
            
            throw new Error('Token non reçu dans la réponse');
            
        } catch (error) {
            throw error;
        }
    },
    
    logout: async () => {
        try {
            const refresh = storage.getRefreshToken();
            if (refresh) {
                await api.post('/account/logout', { refresh });
            }
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            storage.clearTokens();
            router.push('/login');
        }
    },
    
    getCurrentUser: async () => {
        try {
            const response = await api.get('/account/me');
            
            // Le backend retourne { user: {...} }
            if (response.data.user) {
                return response.data.user;
            }
            
            // Au cas où le backend retournerait directement l'objet user
            return response.data;
            
        } catch (error) {
            console.error('Get current user error:', error);
            
            // Si erreur 401, on déconnecte
            if (error.response?.status === 401) {
                storage.clearTokens();
                router.push('/login');
            }
            
            throw error;
        }
    },
    
    isAuthenticated: () => {
        return !!storage.getToken();
    }
};

export default api;