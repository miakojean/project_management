from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.translation import gettext_lazy as _
from .serializers import UtilisateurCreateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Utilisateur, PasswordResetToken
from django.contrib.auth import authenticate
from .utils import generate_password_reset_token
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# Create your views here.
class CreateUserView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UtilisateurCreateSerializer(data = request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "data": serializer.data,
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
                        if "This field is required." in message:
                            french_messages.append(_("Ce champ est obligatoire."))
                        elif "Enter a valid email address." in message:
                            french_messages.append(_("Veuillez saisir une adresse email valide."))
                        elif "Ensure this field has no more than" in message:
                            french_messages.append(_("Ce champ dépasse la longueur maximale autorisée."))
                        elif "This password is too common." in message:
                            french_messages.append(_("Ce mot de passe est trop courant."))
                        else:
                            french_messages.append(message)
                    formatted_errors[field] = [f"{msg}" for msg in french_messages]
                else:
                    formatted_errors[field] = [f"{messages}"]
            
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
                    "details": _("Erreur technique")  # Message générique pour l'utilisateur
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserLoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args , **kwargs):

        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        # On vérifie si l'email, le nom d'utilisateur et le mot de passe sont fournis.

        if not password or (not email and not username):
            return Response(
                {'error':'Veuillez fournir un email/nom d\'utilisateur et un mot de passe.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if email:
            user = Utilisateur.objects.filter(email=email).first()
            if not user:
                return Response(
                    {'error': 'Email ou mot de passe incorrect.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            username = user.username

        user = authenticate(request, username=username,email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user':{
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_200_OK)
        
        else:
            return Response(
                {'error': 'Identifiants incorrects.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
class UserLogoutView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {
                        'message': 'Déconnexion réussie.'
                    },
                    status=status.HTTP_205_RESET_CONTENT
                )
        
        except Exception as e:
            return Response(
                {
                    'message': 'Une erreur est survenue lors de la déconnexion'
                },status=status.HTTP_400_BAD_REQUEST
            )
        
# About password reseting

class PasswordResetRequestView(APIView): # First step
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response(
                {'error':'Veuillez fournir une addresse e-mail.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            # On ne dit pas si l'email existe pour des raisons de sécurité
            return Response(
                {'message': 'Si un compte existe, un email a été envoyé'},
                status=status.HTTP_200_OK
            )
        
        token = generate_password_reset_token(user)
        reset_link = f'{settings.FRONTEND_URL}/reset-passwor/{token}'

        # Ajouter l'envoie d'email de réinitialisation ici

        return Response(
            {'message': 'Si un compte existe, un email a été envoyé.'},
            status=status.HTTP_200_OK
        )
    
class PasswordResetTokenVerifyView(APIView): # Second step
    """
    Vérifie la validité d'un token de réinitialisation
    Exemple de requête : POST /api/password-reset/verify-token/
    {
        "token": "abc123..."
    }
    """
    authentication_classes = []
    permission_classes = []

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
            return Response({
                "valid": True,
                "message": "Token valide",
                "email": reset_token.user.email  # Optionnel : pour confirmation frontend
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

        if not token or not new_password:
            return Response(
                {'error': 'Token et nouveau mot de passe requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reset_token = PasswordResetToken.objects.get(
                token=token,
                expires_at__gt=timezone.now()  # Vérifie que le token n'a pas expiré
            )
        except PasswordResetToken.DoesNotExist:
            return Response(
                {'error': 'Lien invalide ou expiré.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mettre à jour le mot de passe
        user = reset_token.user
        user.password = make_password(new_password)  # Hash le mot de passe
        user.save()

        # ENVOI DE L'EMAIL DE CONFIRMATION DE CHANGEMENT
        #send_password_change_confirmation(user)

        # Supprimer le token utilisé (empêche la réutilisation)
        reset_token.delete()

        return Response(
            {'message': 'Mot de passe réinitialisé avec succès.'},
            status=status.HTTP_200_OK
        )