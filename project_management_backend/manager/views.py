from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Client
from .serializers import ClientSerializer, ClientCreateSerializer
from account.models import Utilisateur
import logging

# views.py - Version simplifiée

# Configuration basique du logger
logger = logging.getLogger(__name__)

class ClientCreateAPIView(APIView):
    """
    API View pour l'ajout d'un nouveau client
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        Création d'un nouveau client
        """
        try:
            # Plus besoin de traiter les dates ici, c'est fait dans le serializer
            serializer = ClientCreateSerializer(
                data=request.data, 
                context={'request': request}
            )
            
            if serializer.is_valid():
                with transaction.atomic():
                    client = serializer.save()
                    self._log_creation(client, request.user)
                    
                    client_serializer = ClientSerializer(client)
                    
                    return Response({
                        'success': True,
                        'message': 'Client créé avec succès',
                        'client': client_serializer.data
                    }, status=status.HTTP_201_CREATED)
            
            else:
                return Response({
                    'success': False,
                    'message': 'Erreur de validation',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Erreur lors de la création du client',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # --- AJOUTEZ CETTE MÉTHODE ---
    def _log_creation(self, client, user):
        """
        Enregistre l'action de création dans les logs ou la BDD
        """
        try:
            # Exemple 1 : Juste un print dans la console du serveur
            print(f"📝 LOG : Le client {client.id} ({client.nom}) a été créé par {user.username}")
            
            # Exemple 2 : Si vous avez un modèle d'historique (décommentez si besoin)
            # ActionLog.objects.create(
            #     user=user,
            #     action="CREATION_CLIENT",
            #     details=f"Création du client {client.nom}"
            # )
            
        except Exception as e:
            # On ne veut pas que le log fasse planter la création du client
            print(f"Erreur lors du logging: {e}")
    

class ClientBulkCreateAPIView(APIView):
    """
    API View pour l'ajout multiple de clients
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        Création de plusieurs clients en une seule requête
        """
        try:
            clients_data = request.data.get('clients', [])
            
            if not isinstance(clients_data, list):
                return Response({
                    'success': False,
                    'message': 'Le format des données est invalide. Attendu: {"clients": []}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            results = {
                'success': [],
                'errors': []
            }
            
            with transaction.atomic():
                for index, client_data in enumerate(clients_data):
                    try:
                        serializer = ClientCreateSerializer(
                            data=client_data, 
                            context={'request': request}
                        )
                        
                        if serializer.is_valid():
                            client = serializer.save()
                            results['success'].append({
                                'index': index,
                                'reference': client.reference_client,
                                'nom_complet': client.nom_complet
                            })
                        else:
                            results['errors'].append({
                                'index': index,
                                'errors': serializer.errors
                            })
                            
                    except Exception as e:
                        results['errors'].append({
                            'index': index,
                            'error': str(e)
                        })
            
            return Response({
                'success': True,
                'message': f"{len(results['success'])} clients créés, {len(results['errors'])} erreurs",
                'results': results
            }, status=status.HTTP_207_MULTI_STATUS)
                
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Erreur lors de la création multiple des clients',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ClientWithDossierCreateAPIView(APIView):
    """
    API View pour créer un client avec son premier dossier
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        Création d'un client et de son premier dossier associé
        """
        try:
            client_data = request.data.get('client', {})
            dossier_data = request.data.get('dossier', {})
            
            if not client_data:
                return Response({
                    'success': False,
                    'message': 'Les données client sont obligatoires'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                # Création du client
                client_serializer = ClientCreateSerializer(
                    data=client_data, 
                    context={'request': request}
                )
                
                if not client_serializer.is_valid():
                    return Response({
                        'success': False,
                        'message': 'Erreur de validation du client',
                        'errors': client_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                client = client_serializer.save()
                
                # Création du dossier si des données sont fournies
                dossier = None
                if dossier_data:
                    from .serializers import DossierSerializer
                    
                    # Ajouter le client au dossier
                    dossier_data['client'] = client.id
                    dossier_data['cree_par'] = request.user.id
                    
                    dossier_serializer = DossierSerializer(
                        data=dossier_data,
                        context={'request': request}
                    )
                    
                    if dossier_serializer.is_valid():
                        dossier = dossier_serializer.save()
                    else:
                        # Si le dossier n'est pas valide, on rollback la transaction
                        transaction.set_rollback(True)
                        return Response({
                            'success': False,
                            'message': 'Erreur de validation du dossier',
                            'errors': dossier_serializer.errors
                        }, status=status.HTTP_400_BAD_REQUEST)
                
                # Préparer la réponse
                response_data = {
                    'success': True,
                    'message': 'Client créé avec succès',
                    'client': ClientSerializer(client).data
                }
                
                if dossier:
                    response_data['dossier'] = DossierSerializer(dossier).data
                    response_data['message'] = 'Client et dossier créés avec succès'
                
                return Response(response_data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Erreur lors de la création du client avec dossier',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)