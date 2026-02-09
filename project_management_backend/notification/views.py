from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Notification, NotificationRecipient 
from .serializers import (
    NotificationRecipientSerializer,
    NotificationSerializer
)

class NotificationListAPIView(APIView):
    """
    API pour récupérer la liste des notifications de l'utilisateur connecté.
    """
    permission_classes = [IsAuthenticated]
    
    def get_notification_queryset(self):
        return Notification.objects.filter(
            notificationrecipient__recipient=self.request.user
        ).prefetch_related(
            'notificationrecipient_set' # Charge TOUS les recipients
        ).distinct().order_by('-created_at')
    
    def get_notificationrecipient_queryset(self):
        """
        Retourne le queryset de base des NotificationRecipient pour l'utilisateur connecté.
        """
        return NotificationRecipient.objects.filter(
            recipient=self.request.user
        )
    
    def get(self, request):
        """
        Récupère les notifications de l'utilisateur.
        """
        unread_only = request.query_params.get('unread', '').lower() == 'true'
        limit = request.query_params.get('limit')
        
        # Base queryset pour les notifications
        base_notification_queryset = self.get_notification_queryset()
        
        # Filtre pour les non lues si nécessaire
        if unread_only:
            # Filtrer les notifications non lues pour l'utilisateur courant
            notifications = base_notification_queryset.filter(
                notificationrecipient__recipient=request.user,
                notificationrecipient__is_read=False
            ).distinct()
        else:
            notifications = base_notification_queryset
        
        # Calcul des totaux à partir de NotificationRecipient
        notificationrecipient_queryset = self.get_notificationrecipient_queryset()
        unread_count = notificationrecipient_queryset.filter(is_read=False).count()
        total_count = notificationrecipient_queryset.count()
        
        # Limitation du nombre de résultats
        if limit and limit.isdigit():
            notifications = notifications[:int(limit)]
        
        # Sérialisation
        serializer = NotificationSerializer(
            notifications, 
            many=True,
            context={'request': request}
        )
        
        return Response({
            'notifications': serializer.data,
            'metadata': {
                'total_count': total_count,
                'unread_count': unread_count,
                'read_count': total_count - unread_count
            }
        })
    
    def post(self, request):
        """
        Marque TOUTES les notifications non lues de l'utilisateur comme lues.
        """
        # Mise à jour sur la table pivot NotificationRecipient
        notificationrecipient_queryset = self.get_notificationrecipient_queryset()
        updated_count = notificationrecipient_queryset.filter(is_read=False).update(is_read=True)
        
        return Response({
            'status': 'success',
            'message': f'{updated_count} notifications marquées comme lues',
            'marked_read': updated_count,
            'unread_count': notificationrecipient_queryset.filter(is_read=False).count()
        }, status=status.HTTP_200_OK)


class NotificationDetailAPIView(APIView):
    """
    API pour gérer une notification spécifique. Le PK est l'ID de la ligne NotificationRecipient.
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retourne le queryset de base pour l'utilisateur connecté (table pivot)."""
        return NotificationRecipient.objects.filter(recipient=self.request.user)
    
    def get(self, request, pk):
        """
        Récupère une entrée NotificationRecipient spécifique par son PK et la marque comme lue.
        """
        # Le PK doit être l'ID de l'enregistrement NotificationRecipient
        notification_recipient = get_object_or_404(self.get_queryset(), pk=pk)
        
        # Marquer comme lue
        if not notification_recipient.is_read:
            # Utilisez la méthode mark_as_read si vous l'avez ajoutée, sinon faites le save
            from django.utils import timezone
            notification_recipient.is_read = True
            notification_recipient.read_at = timezone.now()
            notification_recipient.save()
        
        # Sérialisation de l'objet pivot
        serializer = NotificationRecipientSerializer(notification_recipient)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """
        Met à jour l'état is_read d'une entrée NotificationRecipient spécifique.
        """
        notification_recipient = get_object_or_404(self.get_queryset(), pk=pk)
        
        is_read = request.data.get('is_read')
        
        if is_read is not None:
            new_is_read_state = bool(is_read)
            
            if notification_recipient.is_read != new_is_read_state:
                notification_recipient.is_read = new_is_read_state
                
                # Gestion du champ read_at
                from django.utils import timezone
                notification_recipient.read_at = timezone.now() if new_is_read_state else None
                    
                notification_recipient.save()
            
            serializer = NotificationRecipientSerializer(notification_recipient)
            return Response({
                'status': 'success',
                'message': f'Notification marquée comme {"lue" if notification_recipient.is_read else "non lue"}',
                'data': serializer.data
            })
        
        return Response({
            'status': 'error',-
            'message': 'Requête invalide. Seul le champ "is_read" peut être mis à jour.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Supprime l'entrée NotificationRecipient spécifique (supprime la notification de la vue de l'utilisateur).
        """
        notification_recipient = get_object_or_404(self.get_queryset(), pk=pk)
        notification_recipient.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)