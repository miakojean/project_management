// src/stores/auth.js
import { defineStore } from 'pinia';
import { authService } from '@/_services/api';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        isLoading: false,
        error: null,
        isInitialized: false
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
        async initializeAuth() {
            if (this.isInitialized) return;
            
            this.isLoading = true;
            try {
                const token = sessionStorage.getItem('authToken') || localStorage.getItem('authToken');
                console.log('🔄 Initialisation auth - Token présent:', !!token);
                
                if (token && !this.user) {
                    await this.fetchCurrentUser();
                }
                this.isInitialized = true;
            } catch (error) {
                console.error('❌ Erreur initialisation auth:', error);
                this.logout();
            } finally {
                this.isLoading = false;
            }
        },
        
        async fetchCurrentUser() {
            this.isLoading = true;
            this.error = null;
            
            try {
                console.log('🔄 Récupération infos utilisateur...');
                this.user = await authService.getCurrentUser();
                console.log('✅ Utilisateur chargé:', this.user);
            } catch (error) {
                console.error('❌ Erreur récupération utilisateur:', error);
                this.error = error.message;
                this.user = null;
                throw error;
            } finally {
                this.isLoading = false;
            }
        },
        
        async login(credentials) {
            try {
                console.log('🔐 Tentative de connexion...');
                const response = await authService.login(credentials);
                
                // Récupérer immédiatement les infos utilisateur
                if (response.data.user) {
                    this.user = response.data.user;
                } else {
                    await this.fetchCurrentUser();
                }
                
                console.log('✅ Connexion réussie');
                return response;
            } catch (error) {
                console.error('❌ Erreur connexion:', error);
                this.error = error.message;
                throw error;
            }
        },
        
        async logout() {
            console.log('🚪 Déconnexion...');
            try {
                await authService.logout();
            } catch (error) {
                console.error('❌ Erreur lors de la déconnexion:', error);
            } finally {
                this.user = null;
                this.error = null;
                this.isInitialized = false;
                console.log('✅ Déconnexion effectuée');
            }
        },
        
        async checkAuth() {
            try {
                if (this.isAuthenticated) {
                    // Vérifier que le token est toujours valide
                    await this.fetchCurrentUser();
                    return true;
                }
                return false;
            } catch (error) {
                console.error('❌ Check auth failed:', error);
                await this.logout();
                return false;
            }
        }
    }
});