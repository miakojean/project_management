import axios from "axios"
import router from "@/router"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000, // Réduit à 10s (plus raisonnable)
    withCredentials: true
})

// Service de stockage cohérent
const storage = {
    getToken: () => {
        // Priorité à sessionStorage, fallback à localStorage
        return sessionStorage.getItem('authToken') || localStorage.getItem('authToken');
    },
    getRefreshToken: () => {
        return sessionStorage.getItem('refresh') || localStorage.getItem('refresh');
    },
    setTokens: (authToken, refreshToken) => {
        // Utilise sessionStorage pour plus de sécurité
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

api.interceptors.request.use(
    (config) => {
        const token = storage.getToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        
        // Ajouter un timestamp pour éviter le cache
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

        // Gestion d'autres erreurs courantes
        if (error.response?.status === 403) {
            console.error('Accès refusé');
            // Optionnel: rediriger vers une page d'erreur
        }
        
        if (error.response?.status === 500) {
            console.error('Erreur serveur');
        }
        
        if (error.code === 'ECONNABORTED') {
            console.error('Timeout de la requête');
        }

        return Promise.reject(error);
    }
);

// Fonctions utilitaires pour l'authentification
export const authService = {
    login: async (credentials) => {
        try {
            const response = await api.post('/account/login', credentials);
            
            if (response.data.access_token || response.data.access) {
                const token = response.data.access_token || response.data.access;
                const refreshToken = response.data.refresh_token || response.data.refresh;
                
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
            // Appeler l'endpoint de logout si disponible
            await api.post('/account/logout');
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
            return response.data;
        } catch (error) {
            throw error;
        }
    },
    
    isAuthenticated: () => {
        return !!storage.getToken();
    }
};

export function simulateApiConnexion() {
    return new Promise((resolve) => {
        setTimeout(() => {
            console.log("Connexion réussie");
            resolve();
        }, 3000);
    });
}

export default api;