from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from .models import Utilisateur


class UtilisateurCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        validators=[validate_password],  # AJOUT: Validation Django du mot de passe
        error_messages={
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
        # Validation de la correspondance des mots de passe
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                "password2": _("Les mots de passe ne correspondent pas.")
            })
        
        # La validation de la longueur est maintenant gérée par validate_password

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
        # Extraire les mots de passe
        password = validated_data.pop('password')
        validated_data.pop('password2')  # On retire le champ de confirmation
        
        # Création de l'utilisateur avec create_user() qui hash automatiquement
        user = Utilisateur.objects.create_user(
            **validated_data,
            password=password  # Le password est passé séparément pour être hashé
        )
        return user


# Serializer pour la mise à jour (sans les champs de mot de passe)
class UtilisateurUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = [
            'first_name', 'last_name',
            'phone_number', 'category_title',
            'email'
        ]


# Serializer pour changer le mot de passe
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({
                "new_password2": _("Les nouveaux mots de passe ne correspondent pas.")
            })
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("L'ancien mot de passe est incorrect."))
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


# Serializer pour la liste (sans mot de passe)
class UtilisateurListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name',
            'phone_number', 'category_title',
            'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']


# Serializer pour le profil détaillé
class UtilisateurDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name',
            'phone_number', 'category_title',
            'date_joined', 'last_login', 'is_active',
            'is_staff', 'is_superuser'
        ]
        read_only_fields = [
            'id', 'date_joined', 'last_login', 
            'is_active', 'is_staff', 'is_superuser'
        ]