from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class SimpleUserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les champs d'utilisateur essentiels (Actor/Recipient)."""
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        # Assurez-vous d'importer votre modèle utilisateur ou utilisez settings.AUTH_USER_MODEL
        model = User 
        fields = ('id', 'email', 'full_name')
        read_only_fields = fields