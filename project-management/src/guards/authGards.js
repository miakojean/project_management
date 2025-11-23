// src/guards/authGuard.js
import { authService } from "@/_services/api";

export const authGuard = (to, from, next) => {
    const isAuthenticated = authService.isAuthenticated();
    
    console.log('🔐 Auth Guard - Route:', to.name, 'Authentifié:', isAuthenticated);
    
    // Si la route nécessite une authentification et l'utilisateur n'est pas connecté
    if (to.meta.requiresAuth && !isAuthenticated) {
        console.log('🚫 Accès refusé, redirection vers login');
        next('/login');
    } 
    // Si l'utilisateur est déjà connecté et tente d'accéder à la page login
    else if (to.name === 'login' && isAuthenticated) {
        console.log('✅ Déjà connecté, redirection vers dashboard');
        next('/dashboard');
    } 
    // Accès autorisé
    else {
        console.log('✅ Accès autorisé');
        next();
    }
};