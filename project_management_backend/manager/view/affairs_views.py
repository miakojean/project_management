from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction # Utile pour garantir l'intégrité

from ..serializers import DossierSerializer
# Pas besoin du modèle directement si tout passe par le serializer

class DossierCreateAPIView(APIView):
    """
    Vue dédiée à la création d'un nouveau dossier.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        # 1. Instanciation du serializer avec les données reçues
        serializer = DossierSerializer(data=request.data)

        # 2. Validation
        if serializer.is_valid():
            try:
                # 3. Sauvegarde (Transaction atomique conseillée car ton save() fait beaucoup de choses)
                with transaction.atomic():
                    # On passe l'utilisateur connecté manuellement ici
                    dossier = serializer.save(cree_par=request.user)
                
                # 4. Réponse de succès
                # On peut renvoyer les données complètes ou juste un ID
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                # Si ton modèle plante lors de la création du dossier physique par exemple
                return Response(
                    {"error": f"Erreur technique lors de la création : {str(e)}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # 5. Réponse d'erreur de validation
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)