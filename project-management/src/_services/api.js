import axios from "axios"
import router from "@/router"

const api = axios.create({
    baseURL: 'http://localhost:8000',
    timeout:100000,
    withCredentials: true
})

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config
    },
    (error) => {
        return Promise.reject(error);
    }
)

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 &&
            !originalRequest._retry &&
            !originalRequest.url.includes('/account/token/refresh')
        ) {
            originalRequest._retry = true;
            const refreshToken = localStorage.getItem('refresh'); // On va mettre un nom codé

            if (refreshToken){
                try {
                    const refreshResponse = await axios.post(
                        'http://localhost:8000/account/token/refresh',
                        {refresh: refreshToken}
                    );

                    const newAccessToken = refreshResponse.data.access;
                    localStorage.setItem('authToken', newAccessToken);

                    // Mettre à jour le header et relancer la requête originale
                    originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                    return api(originalRequest);
                }   catch(refreshError){
                    console.error('Refresh token failed:', refreshError);

                    // Deconexion si le refresh echoue
                    localStorage.removeItem('authToken');
                    localStorage.removeItem('refresh');

                    router.push('/login?session_expired=true');
                    return Promise.reject(refreshError);
                }
            }   else {
                // Pas de refresh token disponible on nettoie tout
                localStorage.removeItem('authToken');
                localStorage.removeItem('refresh');
                router.push('/login');
            }
        }

        return Promise.reject(error)
    }
);



export function simulateApiConnexion (){
    setTimeout(()=>{
        console.log("Connexion réussie")
    },3000)
};

export default api;