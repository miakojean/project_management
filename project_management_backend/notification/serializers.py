from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification, NotificationRecipient

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
    """Sérialiseur complet pour les notifications."""
    
    # Sérialiser les relations
    actor = SimpleUserSerializer(read_only=True)
    recipients_info = NotificationRecipientSerializer(
        source='notificationrecipient_set',
        many=True,
        read_only=True
    )
    
    # Champ pour la liste des destinataires (pour la création)
    recipients = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    
    # Champ pour le statut de lecture de l'utilisateur courant
    is_read_for_current_user = serializers.SerializerMethodField()
    
    # Champ pour le nom du type d'objet
    content_type_name = serializers.SerializerMethodField()
    
    # Champ pour le verb en format lisible
    verb_display = serializers.CharField(source='get_verb_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = (
            'id',
            'actor',
            'verb',
            'verb_display',
            'message',
            'recipients_info',
            'recipients',
            'is_read_for_current_user',
            'created_at',
            'content_type',
            'object_id',
            'content_type_name',
        )
        read_only_fields = ('id', 'created_at', 'recipients_info', 'is_read_for_current_user')
    
    def get_content_type_name(self, obj):
        """Retourne le nom du modèle de l'objet lié."""
        if obj.content_type:
            return obj.content_type.model
        return None
    
    def get_is_read_for_current_user(self, obj):
        """Retourne si la notification est lue pour l'utilisateur courant."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                recipient_status = obj.notificationrecipient_set.get(recipient=request.user)
                return recipient_status.is_read
            except NotificationRecipient.DoesNotExist:
                return False
        return False
    
    def create(self, validated_data):
        """Crée une notification avec plusieurs destinataires."""
        recipients = validated_data.pop('recipients', [])
        
        # Créer la notification
        notification = Notification.objects.create(**validated_data)
        
        # Ajouter les destinataires
        if recipients:
            notification.recipients.add(*recipients)
        
        return notification