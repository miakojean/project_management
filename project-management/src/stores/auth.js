// stores/auth.js
import { defineStore } from 'pinia';
import { authService } from '@/services/api';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        isLoading: false,
        error: null
    }),
    
    getters: {
        isAuthenticated: (state) => !!state.user,
        fullName: (state) => {
            if (state.user) {
                return `${state.user.first_name} ${state.user.last_name}`;
            }
            return '';
        }
    },
    
    actions: {
        async fetchCurrentUser() {
            this.isLoading = true;
            this.error = null;
            
            try {
                this.user = await authService.getCurrentUser();
            } catch (error) {
                this.error = error.message;
                this.user = null;
                throw error;
            } finally {
                this.isLoading = false;
            }
        },
        
        async login(credentials) {
            try {
                const response = await authService.login(credentials);
                
                // Récupérer immédiatement les infos utilisateur
                if (response.data.user) {
                    this.user = response.data.user;
                } else {
                    await this.fetchCurrentUser();
                }
                
                return response;
            } catch (error) {
                this.error = error.message;
                throw error;
            }
        },
        
        async logout() {
            await authService.logout();
            this.user = null;
            this.error = null;
        }
    }
});