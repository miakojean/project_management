from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from ..models import Dossier
from ..serializers import DossierSerializer, DossierListSerializer
from account.models import Utilisateur
import logging


# About Notifications
from notification.utils import notify_users

logger = logging.getLogger(__name__)

class DossierCreateAPIView(APIView):
    """
    Vue dédiée à la création d'un nouveau dossier.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        
        # 1. Instanciation du serializer avec les données reçues
        serializer = DossierSerializer(data=request.data, context={'request': request})
        
        # 2. Validation
        if serializer.is_valid():
            try:
                # 3. Sauvegarde (Transaction atomique conseillée car ton save() fait beaucoup de choses)
                with transaction.atomic():
                    # On passe l'utilisateur connecté manuellement ici
                    dossier = serializer.save(cree_par=request.user)
                    # 🚀 2. LOGIQUE DE NOTIFICATION - CRÉATION
                    actor_user = request.user
                    try:
                        # Notifier tout le monde sauf l'acteur
                        recipients = Utilisateur.objects.filter(is_active=True).exclude(pk=actor_user.pk)
                        
                        notify_users(
                            recipients=list(recipients),
                            verb='DOSSIER_AJOUTE', # Utilisé par vous dans l'autre POST
                            message=f"Le dossier '{dossier.reference_dossier}' du client {dossier.client} a été ajouté.",
                            content_object=dossier,
                            actor=actor_user
                        )
                    except Exception as e:
                        # On log l'erreur mais on ne bloque pas la transaction
                        logger.error(f"Erreur lors de la création de la notification pour le dossier {dossier.id}: {e}")
                    # FIN DE NOTIFICATION
                
                # 4. Réponse de succès
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                # Si ton modèle plante lors de la création du dossier physique par exemple
                return Response(
                    {"error": f"Erreur technique lors de la création : {str(e)}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # 5. Réponse d'erreur de validation
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DossierListCreateAPIView(APIView): # Is about creation and reading
    """
    Vue pour lister et créer des dossiers
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Récupère la liste des dossiers avec filtres optionnels
        """
        try:
            # Récupération avec filtres optionnels
            dossiers = Dossier.objects.all()
            
            # Appliquer les filtres
            filters_applied = {}
            
            # Filtrage par statut
            statut = request.query_params.get('statut')
            if statut:
                dossiers = dossiers.filter(statut=statut)
                filters_applied['statut'] = statut
            
            # Filtrage par type
            type_dossier = request.query_params.get('type_dossier')
            if type_dossier:
                dossiers = dossiers.filter(type_dossier=type_dossier)
                filters_applied['type_dossier'] = type_dossier
            
            # Filtrage par priorité
            priorite = request.query_params.get('priorite')
            if priorite:
                dossiers = dossiers.filter(priorite=priorite)
                filters_applied['priorite'] = priorite
            
            # Filtrage par statut d'archive
            est_archive = request.query_params.get('est_archive')
            if est_archive is not None:
                # Convertir la chaîne en booléen
                if est_archive.lower() in ['true', '1', 'yes', 'vrai', 'oui']:
                    dossiers = dossiers.filter(est_archive=True)
                    filters_applied['est_archive'] = True
                elif est_archive.lower() in ['false', '0', 'no', 'faux', 'non']:
                    dossiers = dossiers.filter(est_archive=False)
                    filters_applied['est_archive'] = False
                else:
                    # Valeur invalide, on ignore le filtre
                    pass
            # ============ FIN DE L'AJOUT ============

            # Filtrage par client
            client_id = request.query_params.get('client_id')
            if client_id:
                dossiers = dossiers.filter(client_id=client_id)
                filters_applied['client_id'] = client_id
            
            # Recherche par titre ou référence
            search = request.query_params.get('search')
            if search:
                dossiers = dossiers.filter(
                    Q(titre__icontains=search) |
                    Q(reference_dossier__icontains=search) |
                    Q(description__icontains=search)
                )
                filters_applied['search'] = search
            
            # Calcul du nombre total (avant pagination éventuelle)
            total_count = dossiers.count()
            
            # Tri
            sort_by = request.query_params.get('sort_by', '-date_creation')
            allowed_sorts = ['date_creation', '-date_creation', 'date_ouverture', '-date_ouverture', 
                           'date_echeance', '-date_echeance', 'titre', '-titre', 'statut', '-statut']
            
            if sort_by in allowed_sorts:
                dossiers = dossiers.order_by(sort_by)
            else:
                dossiers = dossiers.order_by('-date_creation')
            
            # Pagination optionnelle
            page_size = request.query_params.get('page_size')
            page_number = request.query_params.get('page', 1)
            
            if page_size and page_size.isdigit():
                paginator = Paginator(dossiers, int(page_size))
                try:
                    dossiers_page = paginator.page(page_number)
                    dossiers_list = dossiers_page.object_list
                    pagination_info = {
                        'page_size': int(page_size),
                        'page_number': int(page_number),
                        'total_pages': paginator.num_pages,
                        'has_next': dossiers_page.has_next(),
                        'has_previous': dossiers_page.has_previous(),
                    }
                except EmptyPage:
                    dossiers_list = []
                    pagination_info = {
                        'page_size': int(page_size),
                        'page_number': int(page_number),
                        'total_pages': 0,
                        'has_next': False,
                        'has_previous': False,
                    }
            else:
                dossiers_list = dossiers
                pagination_info = None
            
            # Sérialisation
            serializer = DossierListSerializer(dossiers_list, many=True)
            
            # Statistiques supplémentaires
            stats = {
                'total': total_count,
                'par_statut': {
                    statut_code: dossiers.filter(statut=statut_code).count()
                    for statut_code, _ in Dossier.STATUT_CHOICES
                },
                'par_priorite': {
                    priorite_code: dossiers.filter(priorite=priorite_code).count()
                    for priorite_code, _ in Dossier.PRIORITE_CHOICES
                },
            }
            
            # Réponse structurée
            response_data = {
                'success': True,
                'message': f'{total_count} dossier(s) trouvé(s)',
                'data': {
                    'dossiers': serializer.data,
                    'metadata': {
                        'count': total_count,
                        'filters_applied': filters_applied,
                        'sort_applied': sort_by,
                        'stats': stats,
                    }
                }
            }
            
            # Ajouter les infos de pagination si applicable
            if pagination_info:
                response_data['data']['metadata']['pagination'] = pagination_info
            
            return Response(response_data)
            
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'error': 'Erreur lors de la récupération des dossiers',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DossierDetailAPIView(APIView):
    """
    Vue pour récupérer, mettre à jour et supprimer un dossier spécifique
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        """
        Récupère les détails d'un dossier spécifique
        """
        try: 
            dossier = get_object_or_404(Dossier, pk=pk)
            serializer = DossierSerializer(dossier)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la récupération du dossier: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk, format=None): 
        """
        Met à jour complètement un dossier
        """
        try:
            dossier = get_object_or_404(Dossier, pk=pk)
            serializer = DossierSerializer(dossier, data=request.data)
            
            if serializer.is_valid():
                with transaction.atomic():
                    updated_dossier = serializer.save()
                
                response_serializer = DossierSerializer(updated_dossier)
                return Response(response_serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la mise à jour: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk, format=None):
        """
        Met à jour partiellement un dossier
        """
        try:
            dossier = get_object_or_404(Dossier, pk=pk)
            serializer = DossierSerializer(dossier, data=request.data, partial=True)
            
            if serializer.is_valid():
                with transaction.atomic():
                    updated_dossier = serializer.save()

                    # 🚀 2. LOGIQUE DE NOTIFICATION - MISE À JOUR (PUT)
                    actor_user = request.user
                    try:
                        # Notifier tout le monde sauf l'acteur
                        recipients = Utilisateur.objects.filter(is_active=True).exclude(pk=actor_user.pk)
                        
                        notify_users(
                            recipients=list(recipients),
                            verb='DOSSIER_MISE_A_JOUR',
                            message=f"Le dossier '{updated_dossier.reference_dossier}' a été mis à jour par {actor_user.get_full_name()}.",
                            content_object=updated_dossier,
                            actor=actor_user
                        )
                    except Exception as e:
                        logger.error(f"Erreur lors de la création de la notification de mise à jour (PUT) pour le dossier {dossier.id}: {e}")
                    # FIN DE NOTIFICATION
                
                response_serializer = DossierSerializer(updated_dossier)
                return Response(response_serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la mise à jour partielle: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk, format=None):
        """
        Supprime un dossier
        """
        try:
            dossier = get_object_or_404(Dossier, pk=pk)
            
            actor_user = request.user
            try:
                recipients = Utilisateur.objects.filter(is_active=True).exclude(pk=actor_user.pk)
                notify_users(
                    recipients=list(recipients),
                    verb='DOSSIER_SUPPRIME',
                    message=f"Le dossier '{dossier.reference_dossier}' a été supprimé par {actor_user.get_full_name()}.",
                    content_object=dossier,
                    actor=actor_user
                )
            except Exception as e:
                logger.error(f"Erreur lors de la notification de suppression: {e}")
            
            with transaction.atomic():
                dossier.delete()
            
            return Response(
                {"message": "Dossier supprimé avec succès"},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la suppression: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DossierStatsAPIView(APIView):
    """
    Vue pour récupérer les statistiques des dossiers
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Récupère les statistiques globales des dossiers
        """
        try:
            total_dossiers = Dossier.objects.count()
            dossiers_actifs = Dossier.objects.filter(
                statut__in=['NOUVEAU', 'EN_COURS', 'EN_ATTENTE']
            ).count()
            dossiers_termines = Dossier.objects.filter(
                statut__in=['TERMINE', 'CLOTURE']
            ).count()
            dossiers_annules = Dossier.objects.filter(statut='ANNULE').count()
            dossiers_en_retard = Dossier.objects.filter(est_en_retard=True).count()
            
            # Statistiques par type
            types_stats = {}
            for type_dossier, label in Dossier.TYPE_DOSSIER_CHOICES:
                count = Dossier.objects.filter(type_dossier=type_dossier).count()
                types_stats[type_dossier] = {
                    'label': label,
                    'count': count
                }
            
            # Statistiques par statut
            statuts_stats = {}
            for statut, label in Dossier.STATUT_CHOICES:
                count = Dossier.objects.filter(statut=statut).count()
                statuts_stats[statut] = {
                    'label': label,
                    'count': count
                }
            
            stats = {
                'total_dossiers': total_dossiers,
                'dossiers_actifs': dossiers_actifs,
                'dossiers_termines': dossiers_termines,
                'dossiers_annules': dossiers_annules,
                'dossiers_en_retard': dossiers_en_retard,
                'par_type': types_stats,
                'par_statut': statuts_stats,
            }
            
            return Response(stats)
            
        except Exception as e:
            return Response(
                {"error": f"Erreur lors du calcul des statistiques: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DossierByClientAPIView(APIView):
    """
    Vue pour récupérer les dossiers d'un client spécifique
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, client_id, format=None):
        """
        Récupère tous les dossiers d'un client
        """
        try:
            dossiers = Dossier.objects.filter(client_id=client_id).order_by('-date_creation')
            serializer = DossierListSerializer(dossiers, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la récupération des dossiers du client: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )