# account/middleware.py
from django.utils.deprecation import MiddlewareMixin

class JWTAuthFromCookieMiddleware(MiddlewareMixin):
    """
    Middleware qui déplace le JWT du cookie vers l'en-tête Authorization
    pour compatibilité avec rest_framework_simplejwt
    """
    
    def process_request(self, request):
        # Vérifier si l'utilisateur n'est pas déjà authentifié
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            # Récupérer le token depuis le cookie
            access_token = request.COOKIES.get('access_token')
            
            if access_token and 'HTTP_AUTHORIZATION' not in request.META:
                # Ajouter le token dans l'en-tête Authorization
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        
        return None