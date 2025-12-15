from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from ..models import Dossier, Reponse, Commentaire
from ..serializers import (
    DossierSerializer, 
    DossierListSerializer,
    CommentaireCreateSerializer,
    CommentaireMinimalSerializer,
    ReponseMinimalSerializer,
    ReponseCreateSerializer,
    ReponseSerializer
)
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
        
# =========================================================
# VUES POUR COMMENTAIRES ET REPONSES (MINIMALISTES)
# =========================================================

class CommentaireListCreateAPIView(APIView):
    """
    Vue pour lister et créer des commentaires sur un dossier
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, dossier_id, format=None):
        """
        Récupère tous les commentaires d'un dossier
        """
        try:
            # Vérifier que le dossier existe
            dossier = get_object_or_404(Dossier, pk=dossier_id)
            
            # Récupérer les commentaires du dossier
            commentaires = dossier.commentaires.all().order_by('-date_creation')
            # Debug: lister quelques infos pour faciliter le debug si la sérialisation plante
            try:
                logger.debug(f"Récupération commentaires pour dossier {dossier_id}: count={commentaires.count()}")
                # lister les ids et auteurs pour faciliter l'investigation
                sample = list(commentaires.values_list('id', 'auteur_id')[:20])
                logger.debug(f"Commentaires sample (id, auteur_id): {sample}")
            except Exception as e:
                logger.debug(f"Impossible d'inspecter les commentaires pour debug: {e}")
            
            # Sérialiser avec un serializer qui inclut les détails de l'auteur mais pas les réponses imbriquées
            try:
                serializer = CommentaireMinimalSerializer(commentaires, many=True)
            except Exception as e:
                # Enregistrer traceback complet côté serveur pour le debug
                logger.exception(f"Erreur lors de la sérialisation des commentaires pour dossier {dossier_id}: {e}")
                return Response(
                    {
                        'success': False,
                        'error': 'Erreur lors de la sérialisation des commentaires',
                        'details': str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            return Response({
                'success': True,
                'dossier_id': dossier_id,
                'dossier_reference': dossier.reference_dossier,
                'dossier_titre': dossier.titre,
                'count': commentaires.count(),
                'commentaires': serializer.data
            })
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des commentaires: {e}")
            return Response(
                {
                    'success': False,
                    'error': 'Erreur lors de la récupération des commentaires',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, dossier_id, format=None):
        """
        Crée un nouveau commentaire sur un dossier
        """
        try:
            # Vérifier que le dossier existe
            dossier = get_object_or_404(Dossier, pk=dossier_id)
            
            # Préparer les données
            data = request.data.copy()
            data['dossier'] = dossier_id
            
            # Utiliser le serializer de création avec auteur automatique
            serializer = CommentaireCreateSerializer(
                data=data,
                context={'request': request}
            )
            
            if serializer.is_valid():
                with transaction.atomic():
                    commentaire = serializer.save()
                    
                    # 🚀 NOTIFICATION
                    actor_user = request.user
                    try:
                        # Notifier les collaborateurs du dossier
                        recipients = dossier.collaborateurs.all().exclude(pk=actor_user.pk)
                        
                        notify_users(
                            recipients=list(recipients),
                            verb='COMMENTAIRE_AJOUTE',
                            message=f"Un nouveau commentaire a été ajouté au dossier '{dossier.reference_dossier}' par {actor_user.get_full_name()}.",
                            content_object=commentaire,
                            actor=actor_user
                        )
                    except Exception as e:
                        logger.error(f"Erreur notification commentaire: {e}")
                    # FIN NOTIFICATION
                
                # Retourner le commentaire créé
                response_serializer = CommentaireMinimalSerializer(commentaire)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(
                {
                    'success': False,
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du commentaire: {e}")
            return Response(
                {
                    'success': False,
                    'error': 'Erreur lors de la création du commentaire',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CommentaireDetailAPIView(APIView):
    """
    Vue pour récupérer, modifier et supprimer un commentaire spécifique
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, commentaire_id, format=None):
        """
        Récupère un commentaire spécifique avec ses réponses
        """
        try:
            commentaire = get_object_or_404(Commentaire, pk=commentaire_id)
            
            # Vérifier que l'utilisateur a accès au dossier
            if not request.user.has_perm('view_all_dossiers') and \
               not commentaire.dossier.collaborateurs.filter(pk=request.user.pk).exists() and \
               commentaire.auteur != request.user:
                return Response(
                    {'error': 'Vous n\'avez pas accès à ce commentaire'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = CommentaireMinimalSerializer(commentaire)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du commentaire: {e}")
            return Response(
                {
                    'success': False,
                    'error': 'Erreur lors de la récupération du commentaire',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, commentaire_id, format=None):
        """
        Met à jour un commentaire (seul l'auteur peut modifier)
        """
        try:
            commentaire = get_object_or_404(Commentaire, pk=commentaire_id)
            
            # Vérifier que l'utilisateur est l'auteur
            if commentaire.auteur != request.user:
                return Response(
                    {'error': 'Vous ne pouvez modifier que vos propres commentaires'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Préparer les données (ne pas permettre de changer le dossier)
            data = request.data.copy()
            if 'dossier' in data:
                del data['dossier']
            
            serializer = CommentaireMinimalSerializer(
                commentaire, 
                data=data, 
                partial=True  # Permet la modification partielle
            )
            
            if serializer.is_valid():
                with transaction.atomic():
                    updated_commentaire = serializer.save()
                    
                    # 🚀 NOTIFICATION
                    actor_user = request.user
                    try:
                        # Notifier les collaborateurs du dossier
                        recipients = commentaire.dossier.collaborateurs.all().exclude(pk=actor_user.pk)
                        
                        notify_users(
                            recipients=list(recipients),
                            verb='COMMENTAIRE_MODIFIE',
                            message=f"Un commentaire sur le dossier '{commentaire.dossier.reference_dossier}' a été modifié par {actor_user.get_full_name()}.",
                            content_object=updated_commentaire,
                            actor=actor_user
                        )
                    except Exception as e:
                        logger.error(f"Erreur notification modification commentaire: {e}")
                    # FIN NOTIFICATION
                
                return Response(serializer.data)
            
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(f"Erreur lors de la modification du commentaire: {e}")
            return Response(
                {
                    'success': False,
                    'error': 'Erreur lors de la modification du commentaire',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, commentaire_id, format=None):
        """
        Supprime un commentaire (seul l'auteur ou admin peut supprimer)
        """
        try:
            commentaire = get_object_or_404(Commentaire, pk=commentaire_id)
            dossier = commentaire.dossier
            
            # Vérifier les permissions
            can_delete = (
                commentaire.auteur == request.user or
                request.user.has_perm('delete_commentaire') or
                request.user.is_superuser
            )
            
            if not can_delete:
                return Response(
                    {'error': 'Vous n\'avez pas la permission de supprimer ce commentaire'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # 🚀 NOTIFICATION avant suppression
            actor_user = request.user
            try:
                recipients = dossier.collaborateurs.all().exclude(pk=actor_user.pk)
                notify_users(
                    recipients=list(recipients),
                    verb='COMMENTAIRE_SUPPRIME',
                    message=f"Un commentaire sur le dossier '{dossier.reference_dossier}' a été supprimé par {actor_user.get_full_name()}.",
                    content_object=commentaire,
                    actor=actor_user
                )
            except Exception as e:
                logger.error(f"Erreur notification suppression commentaire: {e}")
            
            with transaction.atomic():
                commentaire.delete()
            
            return Response(
                {'message': 'Commentaire supprimé avec succès'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du commentaire: {e}")
            return Response(
                {
                    'success': False,
                    'error': 'Erreur lors de la suppression du commentaire',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReponseListCreateAPIView(APIView):
    """
    Vue pour lister et créer des réponses à un commentaire
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, commentaire_id, format=None):
        """
        Récupère toutes les réponses d'un commentaire
        """
        try:
            # Vérifier que le commentaire existe
            commentaire = get_object_or_404(Commentaire, pk=commentaire_id)
            
            # Récupérer les réponses
            reponses = commentaire.reponses.all().order_by('date_creation')
            serializer = ReponseSerializer(reponses, many=True)
            
            return Response({
                'success': True,
                'commentaire_id': commentaire_id,
                'count': reponses.count(),
                'reponses': serializer.data
            })
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des réponses: {e}")
            return Response(
                {
                    'success': False,
                    'error': 'Erreur lors de la récupération des réponses',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, commentaire_id, format=None):
        """
        Crée une nouvelle réponse à un commentaire
        """
        try:
            # Vérifier que le commentaire existe
            commentaire = get_object_or_404(Commentaire, pk=commentaire_id)
            
            # Vérifier l'accès au dossier
            if not request.user.has_perm('view_all_dossiers') and \
               not commentaire.dossier.collaborateurs.filter(pk=request.user.pk).exists():
                return Response(
                    {'error': 'Vous n\'avez pas accès à ce dossier'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Préparer les données
            data = request.data.copy()
            data['commentaire'] = commentaire_id
            
            # Utiliser le serializer de création avec auteur automatique
            serializer = ReponseCreateSerializer(
                data=data,
                context={'request': request}
            )
            
            if serializer.is_valid():
                with transaction.atomic():
                    reponse = serializer.save()
                    
                    # 🚀 NOTIFICATION
                    actor_user = request.user
                    try:
                        # Notifier l'auteur du commentaire original et les collaborateurs
                        recipients = set()
                        recipients.add(commentaire.auteur)  # Auteur du commentaire
                        
                        # Ajouter les collaborateurs du dossier
                        for collaborateur in commentaire.dossier.collaborateurs.all():
                            if collaborateur != actor_user:
                                recipients.add(collaborateur)
                        
                        notify_users(
                            recipients=list(recipients),
                            verb='REPONSE_AJOUTEE',
                            message=f"Une réponse a été ajoutée à un commentaire sur le dossier '{commentaire.dossier.reference_dossier}'.",
                            content_object=reponse,
                            actor=actor_user
                        )
                    except Exception as e:
                        logger.error(f"Erreur notification réponse: {e}")
                    # FIN NOTIFICATION
                
                # Retourner la réponse créée
                response_serializer = ReponseMinimalSerializer(reponse)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(
                {
                    'success': False,
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de la réponse: {e}")
            return Response(
                {
                    'success': False,
                    'error': 'Erreur lors de la création de la réponse',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReponseDetailAPIView(APIView):
    """
    Vue pour modifier et supprimer une réponse spécifique
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, reponse_id, format=None):
        """
        Met à jour une réponse (seul l'auteur peut modifier)
        """
        try:
            reponse = get_object_or_404(Reponse, pk=reponse_id)
            commentaire = reponse.commentaire
            
            # Vérifier que l'utilisateur est l'auteur
            if reponse.auteur != request.user:
                return Response(
                    {'error': 'Vous ne pouvez modifier que vos propres réponses'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Vérifier l'accès au dossier
            if not request.user.has_perm('view_all_dossiers') and \
               not commentaire.dossier.collaborateurs.filter(pk=request.user.pk).exists():
                return Response(
                    {'error': 'Vous n\'avez pas accès à ce dossier'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Préparer les données (ne pas permettre de changer le commentaire)
            data = request.data.copy()
            if 'commentaire' in data:
                del data['commentaire']
            
            serializer = ReponseMinimalSerializer(
                reponse, 
                data=data, 
                partial=True
            )
            
            if serializer.is_valid():
                with transaction.atomic():
                    updated_reponse = serializer.save()
                    
                    # 🚀 NOTIFICATION
                    actor_user = request.user
                    try:
                        # Notifier les personnes concernées
                        recipients = set()
                        recipients.add(commentaire.auteur)  # Auteur du commentaire original
                        
                        for collaborateur in commentaire.dossier.collaborateurs.all():
                            if collaborateur != actor_user:
                                recipients.add(collaborateur)
                        
                        notify_users(
                            recipients=list(recipients),
                            verb='REPONSE_MODIFIEE',
                            message=f"Une réponse a été modifiée sur le dossier '{commentaire.dossier.reference_dossier}'.",
                            content_object=updated_reponse,
                            actor=actor_user
                        )
                    except Exception as e:
                        logger.error(f"Erreur notification modification réponse: {e}")
                    # FIN NOTIFICATION
                
                return Response(serializer.data)
            
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(f"Erreur lors de la modification de la réponse: {e}")
            return Response(
                {
                    'success': False,
                    'error': 'Erreur lors de la modification de la réponse',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, reponse_id, format=None):
        """
        Supprime une réponse (seul l'auteur peut supprimer)
        """
        try:
            reponse = get_object_or_404(Reponse, pk=reponse_id)
            commentaire = reponse.commentaire
            
            # Vérifier que l'utilisateur est l'auteur
            if reponse.auteur != request.user:
                return Response(
                    {'error': 'Vous ne pouvez supprimer que vos propres réponses'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Vérifier l'accès au dossier
            if not request.user.has_perm('view_all_dossiers') and \
               not commentaire.dossier.collaborateurs.filter(pk=request.user.pk).exists():
                return Response(
                    {'error': 'Vous n\'avez pas accès à ce dossier'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # 🚀 NOTIFICATION avant suppression
            actor_user = request.user
            try:
                recipients = set()
                recipients.add(commentaire.auteur)  # Auteur du commentaire original
                
                for collaborateur in commentaire.dossier.collaborateurs.all():
                    if collaborateur != actor_user:
                        recipients.add(collaborateur)
                
                notify_users(
                    recipients=list(recipients),
                    verb='REPONSE_SUPPRIMEE',
                    message=f"Une réponse a été supprimée sur le dossier '{commentaire.dossier.reference_dossier}'.",
                    content_object=reponse,
                    actor=actor_user
                )
            except Exception as e:
                logger.error(f"Erreur notification suppression réponse: {e}")
            
            with transaction.atomic():
                reponse.delete()
            
            return Response(
                {'message': 'Réponse supprimée avec succès'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de la réponse: {e}")
            return Response(
                {
                    'success': False,
                    'error': 'Erreur lors de la suppression de la réponse',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )