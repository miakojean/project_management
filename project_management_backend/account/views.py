from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.translation import gettext_lazy as _
from .serializers import UtilisateurCreateSerializer

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
