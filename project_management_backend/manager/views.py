from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Client
from .serializers import ClientSerializer, ClientCreateSerializer, ClientListSerializer
from account.models import Utilisateur
import logging
from django.db.models import Q, Count 
from django.db.models.functions import TruncMonth
from notification.utils import notify_users

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
            serializer = ClientCreateSerializer(
                data=request.data, 
                context={'request': request}
            )
            
            if serializer.is_valid():
                with transaction.atomic():
                    client = serializer.save()
                    actor_user = request.user
                    self._log_creation(client, request.user)

                    try:
                        # Définir les destinataires : Tous les utilisateurs actifs SAUF l'acteur
                        # On suppose que 'Utilisateur' a un champ 'is_active'
                        recipients = Utilisateur.objects.filter(is_active=True).exclude(pk=actor_user.pk)
                        
                        notify_users(
                            recipients=list(recipients),
                            verb='CLIENT_AJOUTE', # Correspond à EVENT_CHOICES dans models.py
                            message=f"Le nouveau client '{client.nom_complet}' a été ajouté par {actor_user.get_full_name()}.",
                            content_object=client, # L'objet source pour la GFK
                            actor=actor_user,
                        )
                        
                    except Exception as e:
                        # IMPORTANT : En cas d'erreur de notification, on log et on continue la transaction.
                        logger.error(f"Erreur lors de la création des notifications pour le client {client.id}: {e}")
                        
                    # --- 3. Log et Réponse ---
                    self._log_creation(client, actor_user)
                    
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

class ClientListAPIView(APIView):
    """
    API View pour lister et filtrer les clients
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Récupère la liste des clients avec filtres et pagination
        """
        try:
            # Récupération des paramètres de requête
            type_client = request.GET.get('type_client')
            statut = request.GET.get('statut') 
            search = request.GET.get('search')
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 20))
            
            # Construction de la queryset de base
            clients = Client.objects.all()
            
            # Application des filtres
            if type_client:
                clients = clients.filter(type_client=type_client)
            
            if statut:
                clients = clients.filter(statut=statut)
            
            if search:
                clients = clients.filter(
                    Q(nom__icontains=search) |
                    Q(prenoms__icontains=search) |
                    Q(raison_sociale__icontains=search) |
                    Q(reference_client__icontains=search) |
                    Q(telephone_1__icontains=search) |
                    Q(email__icontains=search) |
                    Q(ville__icontains=search)
                )
            
            # Tri par défaut
            clients = clients.order_by('-date_creation')
            
            # Pagination
            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            
            total_clients = clients.count()
            clients_page = clients[start_index:end_index]
            
            # Sérialisation
            serializer = ClientListSerializer(clients_page, many=True)
            
            return Response({
                'success': True,
                'clients': serializer.data,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': total_clients,
                    'pages': (total_clients + page_size - 1) // page_size
                },
                'filters': {
                    'type_client': type_client,
                    'statut': statut,
                    'search': search
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des clients: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erreur lors de la récupération des clients',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ClientSearchAPIView(APIView):
    """
    API View pour la recherche avancée de clients
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Recherche avancée dans les clients
        """
        try:
            query = request.GET.get('q', '')
            
            if not query or len(query) < 2:
                return Response({
                    'success': False,
                    'message': 'Le terme de recherche doit contenir au moins 2 caractères'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Recherche dans tous les champs pertinents
            clients = Client.objects.filter(
                Q(nom__icontains=query) |
                Q(prenoms__icontains=query) |
                Q(raison_sociale__icontains=query) |
                Q(reference_client__icontains=query) |
                Q(telephone_1__icontains=query) |
                Q(telephone_2__icontains=query) |
                Q(email__icontains=query) |
                Q(adresse__icontains=query) |
                Q(ville__icontains=query) |
                Q(commune__icontains=query) |
                Q(representant_legal_nom__icontains=query) |
                Q(numero_rccm__icontains=query) |
                Q(numero_cc__icontains=query)
            ).order_by('-date_creation')[:50]  # Limite pour les performances
            
            serializer = ClientListSerializer(clients, many=True)
            
            return Response({
                'success': True,
                'results': serializer.data,
                'count': len(serializer.data),
                'query': query
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Erreur lors de la recherche: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erreur lors de la recherche',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientMonthlyRegistrationStatsAPIView(APIView):
    """Retourne le nombre de clients créés par mois."""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Agrégation par mois en utilisant TruncMonth
            qs = (
                Client.objects
                .annotate(month=TruncMonth('date_creation'))
                .values('month')
                .annotate(count=Count('id'))
                .order_by('month')
            )

            labels = [item['month'].strftime('%Y-%m') if item['month'] else None for item in qs]
            data = [item['count'] for item in qs]

            return Response({'success': True, 'labels': labels, 'data': data}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Erreur lors de la génération des stats clients mensuelles: {e}")
            return Response({'success': False, 'message': 'Erreur lors de la récupération des statistiques', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ClientDetailView(APIView):
    """
    Docstring for ClientDetailView
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, client_id, *args, **kwargs):
        try:
            client = Client.objects.get(id=client_id)
            serializer = ClientSerializer(client)
            return Response({
                'message': 'Détails du client récupérés avec succès',
                'success': True,
                'client': serializer.data
            }, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            return Response({
                'message': 'Client non trouvé',
                'success': False
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, client_id, *args, **kwargs):
        try:
            client = Client.objects.get(id=client_id)
            serializer = ClientCreateSerializer(client, data=request.data, partial=True, context={'request': request})
            
            if serializer.is_valid():
                with transaction.atomic():
                    updated_client = serializer.save()
                    
                    # Log de la modification
                    actor_user = request.user
                    logger.info(f"Le client '{updated_client.nom_complet}' a été mis à jour par {actor_user.get_full_name()}.")
                    
                    # Création d'une notification
                    recipients = Utilisateur.objects.filter(is_active=True).exclude(pk=actor_user.pk)
                    notify_users(
                        recipients=list(recipients),
                        verb='CLIENT_MODIFIE',
                        message=f"Le client '{updated_client.nom_complet}' a été mis à jour par {actor_user.get_full_name()}.",
                        content_object=updated_client,
                        actor=actor_user,
                    )
                    
                client_serializer = ClientSerializer(updated_client)
                return Response({
                    'success': True,
                    'message': 'Client mis à jour avec succès',
                    'client': client_serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Erreur de validation',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Client.DoesNotExist:
            return Response({
                'message': 'Client non trouvé',
                'success': False
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du client {client_id}: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erreur interne du serveur',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)