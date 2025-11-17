from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Utilisateur

class UtilisateurCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only = True,
        style = { 'input_type': 'password'},
        error_messages = {
            'blank': _('Le mot de passe est obligatoire.'),
            'required': _('Le mot de passe est obligatoire.')
        }
    )
    password2 = serializers.CharField(
        write_only=True, 
        style={'input_type': 'password'},
        error_messages={
            'blank': _('La confirmation du mot de passe est obligatoire.'),
            'required': _('La confirmation du mot de passe est obligatoire.')
        }
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            'blank': _("L'adresse email est obligatoire."),
            'required': _("L'adresse email est obligatoire.")
        }
    )

    class Meta:
        model = Utilisateur
        fields = [
            'username', 'email',
            'password', 'password2',
            'first_name', 'last_name',
            'phone_number', 'category_title',
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                "password2": _("Les mots de passe ne correspondent pas.")
            })
        
        # Validation de la force du mot de passe (optionnel)
        if len(data['password']) < 8:
            raise serializers.ValidationError({
                "password": _("Le mot de passe doit contenir au moins 8 caractères.")
            })

        # Vérifications d'unicité
        if Utilisateur.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({
                "username": _("Ce nom d'utilisateur est déjà pris.")
            })

        if Utilisateur.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                "email": _("Cette adresse email est déjà utilisée.")
            })

        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = Utilisateur(**validated_data)
        user.save()
        return user