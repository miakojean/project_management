from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification, NotificationRecipient, Insight

User = get_user_model()

class SimpleUserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les champs d'utilisateur essentiels."""
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name')
        read_only_fields = fields


class NotificationRecipientSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le statut de lecture par utilisateur."""
    recipient = SimpleUserSerializer(read_only=True)
    
    class Meta:
        model = NotificationRecipient
        fields = ('id', 'recipient', 'is_read', 'read_at')
        read_only_fields = fields


class NotificationSerializer(serializers.ModelSerializer):
    actor = SimpleUserSerializer(read_only=True)
    
    # On supprime recipients_info complet pour la confidentialité
    # On garde recipients pour la création (write_only)
    recipients = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    
    verb_display = serializers.CharField(source='get_verb_display', read_only=True)
    
    # NOUVEAUX CHAMPS CALCULÉS
    is_read = serializers.SerializerMethodField()
    tracking_id = serializers.SerializerMethodField() # L'ID à utiliser pour DELETE/UPDATE
    content_type_str = serializers.SerializerMethodField()  # AJOUTEZ CETTE LIGNE
    
    class Meta:
        model = Notification
        fields = (
            'id', # ID de la notification (contenu)
            'tracking_id', # ID de la relation (pour marquer lu/supprimer)
            'actor',
            'verb',
            'verb_display',
            'recipients',
            'message',
            'is_read', # Remplaçant de is_read_for_current_user
            'created_at',
            'content_type_str', # Renommé pour clarté
            'object_id',
        )
        read_only_fields = ('id', 'created_at')

    def get_content_type_str(self, obj):
        """Méthode pour obtenir la représentation en string du content_type"""
        if obj.content_type:
            return f"{obj.content_type.app_label}.{obj.content_type.model}"
        return None

    def _get_recipient_data(self, obj):
        """
        Helper pour récupérer l'objet pivot sans refaire de requête SQL
        si prefetch_related est utilisé dans la vue.
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            return None
            
        # Astuce : On regarde dans le cache de préchargement si disponible
        # Sinon on fait la requête (couteux, mais fallback)
        if hasattr(obj, '_prefetched_objects_cache') and 'notificationrecipient_set' in obj._prefetched_objects_cache:
            for recipient_obj in obj.notificationrecipient_set.all():
                if recipient_obj.recipient_id == user.id:
                    return recipient_obj
        else:
            # Fallback (non performant mais fonctionnel)
            try:
                return obj.notificationrecipient_set.get(recipient=user)
            except NotificationRecipient.DoesNotExist:
                return None
        return None

    def get_is_read(self, obj):
        recipient_data = self._get_recipient_data(obj)
        return recipient_data.is_read if recipient_data else False

    def get_tracking_id(self, obj):
        recipient_data = self._get_recipient_data(obj)
        return recipient_data.id if recipient_data else None

    def create(self, validated_data):
        recipients = validated_data.pop('recipients', [])
        notification = Notification.objects.create(**validated_data)
        
        # Création en masse via through_defaults (Django 2.2+) ou boucle
        # Ici on utilise la méthode simple
        if recipients:
            notification.recipients.add(*recipients)
            
        return notification
    
class InsightSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Insight
        fields = [
            'title',
            'slug',
            'excerpt',
            'content',
            'author',
            'category',
            'confidentiality_level',
            'status',
            'creation_date',
            'last_modified',
            'publication_date',
            'expiration_date',
            'attachment',
            'thumbnail',
            'views_count',
            'is_featured',
            'allow_comments',  # AJOUTEZ LA VIRGULE MANQUANTE ICI
            'related_insights'
        ]