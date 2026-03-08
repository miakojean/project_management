from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.translation import gettext_lazy as _
from .serializers import UtilisateurCreateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Utilisateur, PasswordResetToken
from django.contrib.auth import authenticate
from .utils import generate_password_reset_token, send_password_reset_email
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

# Create your views here.
class CreateUserView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UtilisateurCreateSerializer(data=request.data)

        try:
            if serializer.is_valid():
                user = serializer.save()
                return Response(
                    {
                        "data": {
                            "id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name
                        },
                        "message": _("Votre compte a été créé avec succès.")
                    },
                    status=status.HTTP_201_CREATED
                )
            
            # Formatage des erreurs en français
            formatted_errors = {}
            for field, messages in serializer.errors.items():
                if isinstance(messages, list):
                    # Conversion des codes d'erreur en messages français
                    french_messages = []
                    for message in messages:
                        if "This field is required." in str(message):
                            french_messages.append(_("Ce champ est obligatoire."))
                        elif "Enter a valid email address." in str(message):
                            french_messages.append(_("Veuillez saisir une adresse email valide."))
                        elif "Ensure this field has no more than" in str(message):
                            french_messages.append(_("Ce champ dépasse la longueur maximale autorisée."))
                        elif "This password is too common." in str(message):
                            french_messages.append(_("Ce mot de passe est trop courant."))
                        elif "The password is too similar to the" in str(message):
                            french_messages.append(_("Le mot de passe est trop similaire à vos informations personnelles."))
                        elif "This password is entirely numeric." in str(message):
                            french_messages.append(_("Le mot de passe ne peut pas être entièrement numérique."))
                        elif "This password is too short." in str(message):
                            french_messages.append(_("Le mot de passe doit contenir au moins 8 caractères."))
                        else:
                            french_messages.append(str(message))
                    formatted_errors[field] = french_messages
                else:
                    formatted_errors[field] = [str(messages)]
            
            return Response(
                {
                    "errors": formatted_errors,
                    "message": _("Impossible de créer votre compte. Veuillez corriger les champs indiqués")
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except serializers.ValidationError as e:
            # Gestion spécifique des erreurs de validation
            return Response(
                {
                    "errors": e.detail,
                    "message": _("❌ Données invalides. Veuillez vérifier les informations saisies.")
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            # Log l'erreur complète pour le débogage
            print(f"Erreur lors de la création d'utilisateur: {str(e)}")
            
            return Response(
                {
                    "message": _("🚨 Une erreur inattendue est survenue. Nos équipes ont été informées."),
                    "details": str(e) if settings.DEBUG else _("Erreur technique")
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserLoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        # Vérification des champs obligatoires
        if not password:
            return Response(
                {'error': 'Veuillez fournir un mot de passe.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not email and not username:
            return Response(
                {'error': 'Veuillez fournir un email ou un nom d\'utilisateur.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authentification par email
        if email:
            try:
                user = Utilisateur.objects.get(email=email)
                username = user.username  # On récupère le username pour l'authentification
            except Utilisateur.DoesNotExist:
                return Response(
                    {'error': 'Email ou mot de passe incorrect.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            # Authentification par username
            username = username

        # CORRECTION: authenticate() ne prend pas 'email' comme paramètre
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                return Response(
                    {'error': 'Votre compte est désactivé.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Création de la reponse
            response = Response({
               'user': {
                   'user':user.id,
                    'username': user.username,
                    'email':user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'category_title': user.category_title
                },
                'message':'Connexion Réussie.'
            }, status=status.HTTP_200_OK
            )

            # Définir les cookies HttpOnly
            # Access Token cookie (15 minutes ou 1 jour selon votre configuration)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                max_age=24 * 60 * 60,  # 1 jour (votre settings)
            )

            # Refresh Token cookie (7 jours)
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                max_age=7 * 24 * 60 * 60,  # 7 jours
            )

            return response
        
        else:
            return Response(
                {'error': 'Email/Nom d\'utilisateur ou mot de passe incorrect.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
class CustomTokenRefreshView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Récupérer le refresh token depuis le cookie
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            return Response(
                {'error': 'Refresh token manquant. Veuillez vous reconnecter.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            # Valider et rafraîchir le token
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            
            # Créer la réponse
            response = Response({
                'message': 'Token rafraîchi avec succès.'
            }, status=status.HTTP_200_OK)
            
            # Mettre à jour le cookie access_token
            response.set_cookie(
                key='access_token',
                value=new_access_token,
                httponly=True,
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                max_age=24 * 60 * 60,  # 1 jour
            )
            
            # Si rotation des refresh tokens est activée
            if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS', False):
                # Blacklist l'ancien refresh token
                if settings.SIMPLE_JWT.get('BLACKLIST_AFTER_ROTATION', False):
                    try:
                        refresh.blacklist()
                    except AttributeError:
                        # Si blacklist n'est pas configuré
                        pass
                
                # Créer un nouveau refresh token
                user_id = refresh.payload.get('user_id')
                if user_id:
                    try:
                        user = Utilisateur.objects.get(id=user_id)
                        new_refresh = RefreshToken.for_user(user)
                        
                        # Mettre à jour le cookie refresh_token
                        response.set_cookie(
                            key='refresh_token',
                            value=str(new_refresh),
                            httponly=True,
                            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                            max_age=7 * 24 * 60 * 60,  # 7 jours
                        )
                    except Utilisateur.DoesNotExist:
                        pass
            
            return response
            
        except (TokenError, InvalidToken) as e:
            return Response(
                {'error': 'Token invalide ou expiré. Veuillez vous reconnecter.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

class UserLogoutView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 1. Récupération du refresh token. 
            # Si tes cookies sont HttpOnly, utilise request.COOKIES.get('nom_du_cookie_refresh')
            # Sinon, si le front l'envoie manuellement : request.data.get("refresh")
            refresh_token = request.COOKIES.get("refresh_token") or request.data.get("refresh")
            
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()  # Blacklist le token côté serveur
                except Exception as e:
                    print(f"Erreur lors du blacklist du token: {e}")
            
            # 2. On prépare la réponse
            response = Response(
                {
                    'message': 'Déconnexion réussie.'
                },
                status=status.HTTP_200_OK
            )
            
            # 3. ON SUPPRIME LES COOKIES CÔTÉ CLIENT
            # Remplace 'access_token' et 'refresh_token' par les noms exacts de tes cookies
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            
            # Note : Si tu as défini des attributs spécifiques lors de la CRÉATION du cookie 
            # (comme domain, path ou samesite), tu dois les préciser ici aussi pour que ça marche.
            # Exemple : response.delete_cookie('access_token', path='/', samesite='Lax')

            return response
        
        except Exception as e:
            return Response(
                {
                    'message': 'Une erreur est survenue lors de la déconnexion',
                    'error': str(e) if settings.DEBUG else None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

# About password reseting
class PasswordResetRequestView(APIView): # First step
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response(
                {'error': 'Veuillez fournir une adresse e-mail.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier d'abord si l'email existe dans la base
        try:
            user = Utilisateur.objects.get(email=email)
            
            # Si l'utilisateur existe et est actif, générer et envoyer le token
            if user.is_active:
                # Générer le token de réinitialisation
                token = generate_password_reset_token(user)
                reset_link = f'{settings.FRONTEND_URL}/reset-password/{token}'

                # Envoyer l'email uniquement si l'utilisateur existe
                try:
                    send_password_reset_email(user, reset_link)
                except Exception as mail_err:
                    # Log interne seulement
                    print(f"Erreur d'envoi email reset pour {user.email}: {mail_err}")
                    # Ne pas exposer l'erreur à l'utilisateur
        
        except Utilisateur.DoesNotExist:
            # Email n'existe pas dans la base, on ne fait rien (pas d'email envoyé)
            # Mais on ne le révèle pas à l'utilisateur
            pass
        
        # Toujours retourner le même message, que l'email existe ou non
        return Response(
            {'message': 'Si un compte existe avec cet email, un lien de réinitialisation a été envoyé.'},
            status=status.HTTP_200_OK
        )

class PasswordResetTokenVerifyView(APIView): # Second step
    """
    Vérifie la validité d'un token de réinitialisation
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response(
                {"valid": False, "message": "Token requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reset_token = PasswordResetToken.objects.get(
                token=token,
                expires_at__gt=timezone.now()  # Vérifie que le token n'a pas expiré
            )
            
            # Vérifier que l'utilisateur est toujours actif
            if not reset_token.user.is_active:
                return Response({
                    "valid": False,
                    "message": "Ce compte utilisateur n'est plus actif"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            return Response({
                "valid": True,
                "message": "Token valide",
                "email": reset_token.user.email
            })
            
        except PasswordResetToken.DoesNotExist:
            return Response({
                "valid": False,
                "message": "Token invalide ou expiré"
            }, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView): # Third step
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        new_password2 = request.data.get('new_password2')

        if not token or not new_password:
            return Response(
                {'error': 'Token et nouveau mot de passe requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérification de la confirmation du mot de passe
        if new_password != new_password2:
            return Response(
                {'error': 'Les mots de passe ne correspondent pas.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Validation de la force du mot de passe
            validate_password(new_password)
        except ValidationError as e:
            return Response(
                {'error': ' '.join(e.messages)},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reset_token = PasswordResetToken.objects.get(
                token=token,
                expires_at__gt=timezone.now()
            )
        except PasswordResetToken.DoesNotExist:
            return Response(
                {'error': 'Lien invalide ou expiré.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier que l'utilisateur est actif
        user = reset_token.user
        if not user.is_active:
            return Response(
                {'error': 'Ce compte utilisateur n\'est plus actif.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mettre à jour le mot de passe
        user.set_password(new_password)  # CORRECTION: Utiliser set_password() au lieu de make_password()
        user.save()

        # TODO: ENVOI DE L'EMAIL DE CONFIRMATION DE CHANGEMENT
        # send_password_change_confirmation(user)

        # Supprimer le token utilisé (empêche la réutilisation)
        reset_token.delete()

        # Supprimer tous les autres tokens existants pour cet utilisateur
        PasswordResetToken.objects.filter(user=user).delete()

        return Response(
            {'message': 'Mot de passe réinitialisé avec succès.'},
            status=status.HTTP_200_OK
        )

# Vue pour obtenir les informations de l'utilisateur connecté
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Récupérer le token depuis le cookie (optionnel, pour debug)
        access_token = request.COOKIES.get('access_token')
        
        response_data = {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'nom_complet': user.get_full_name(),
                'phone_number': user.phone_number,
                'category_title': user.category_title,
                'date_joined': user.date_joined,
                'last_login': user.last_login
            }
        }
        
        # En développement, on peut ajouter un indicateur de présence du cookie
        if settings.DEBUG and access_token:
            response_data['debug'] = {
                'cookie_present': True,
                'cookie_length': len(access_token)
            }
        
        return Response(response_data)