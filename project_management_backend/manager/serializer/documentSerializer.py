from manager.models import Document
from rest_framework import serializers
from django.utils import timezone
from django.db import models

# serializers/document_download_serializers.py
from rest_framework import serializers
from django.http import FileResponse
from django.utils.translation import gettext_lazy as _
from ..models import Document
import os


class DocumentDownloadSerializer(serializers.ModelSerializer):
    """Serializer pour le téléchargement de documents"""
    
    # URL de téléchargement direct
    download_url = serializers.SerializerMethodField()
    
    # Métadonnées pour le téléchargement
    fichier_info = serializers.SerializerMethodField()
    est_telechargeable = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id',
            'reference',
            'titre',
            'description',
            'download_url',
            'fichier_info',
            'est_telechargeable',
            'statut',
            'niveau_confidentialite',
            'extension',
            'taille_lisible',
            'date_document',
            'date_validite',
        ]
        read_only_fields = fields
    
    def get_download_url(self, obj):
        """Génère l'URL de téléchargement"""
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/documents/{obj.id}/download/')
        return None
    
    def get_fichier_info(self, obj):
        """Informations sur le fichier"""
        return {
            'nom_fichier': os.path.basename(obj.fichier.name) if obj.fichier else None,
            'extension': obj.extension,
            'taille': obj.taille_lisible,
            'chemin': obj.fichier.url if obj.fichier else None,
        }
    
    def get_est_telechargeable(self, obj):
        """Vérifie si le document peut être téléchargé"""
        # Vérifier l'existence du fichier physique
        if not obj.fichier or not obj.fichier.storage.exists(obj.fichier.name):
            return False
        
        # Vérifier les permissions de confidentialité
        request = self.context.get('request')
        user = request.user if request else None
        
        if not user:
            return False
        
        # Vérifier les permissions basées sur le niveau de confidentialité
        if obj.niveau_confidentialite == 'PUBLIC':
            return True
        elif obj.niveau_confidentialite == 'INTERNE' and user.is_authenticated:
            return True
        elif obj.niveau_confidentialite == 'CONFIDENTIEL':
            return user.has_perm('documents.view_confidential_documents')
        elif obj.niveau_confidentialite == 'TRES_CONFIDENTIEL':
            # Permission spéciale pour très confidentiel
            return user.has_perm('documents.view_confidential_documents') and user.is_staff
        
        return False


class DocumentDownloadRequestSerializer(serializers.Serializer):
    """Serializer pour les requêtes de téléchargement"""
    
    document_id = serializers.IntegerField(
        required=True,
        help_text=_("ID du document à télécharger")
    )
    
    format = serializers.ChoiceField(
        choices=[
            ('original', _("Format original")),
            ('pdf', _("PDF (si conversion possible)")),
            ('zip', _("Archive ZIP (pour plusieurs fichiers)")),
        ],
        default='original',
        required=False,
        help_text=_("Format de téléchargement")
    )
    
    inclure_metadata = serializers.BooleanField(
        default=False,
        required=False,
        help_text=_("Inclure un fichier JSON avec les métadonnées")
    )
    
    raisons = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        help_text=_("Raison du téléchargement (pour audit)")
    )
    
    def validate_document_id(self, value):
        """Valider que le document existe"""
        try:
            document = Document.objects.get(id=value)
            self.context['document'] = document
        except Document.DoesNotExist:
            raise serializers.ValidationError(_("Document non trouvé"))
        return value
    
    def validate(self, data):
        """Validation supplémentaire"""
        document = self.context.get('document')
        request = self.context.get('request')
        
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError(_("Authentification requise"))
        
        # Vérifier les permissions
        user = request.user
        
        # Vérifier la confidentialité
        if document.niveau_confidentialite == 'CONFIDENTIEL':
            if not user.has_perm('documents.view_confidential_documents'):
                raise serializers.ValidationError(_("Permission insuffisante pour ce document"))
        elif document.niveau_confidentialite == 'TRES_CONFIDENTIEL':
            if not (user.has_perm('documents.view_confidential_documents') and user.is_staff):
                raise serializers.ValidationError(_("Permission insuffisante pour ce document"))
        
        # Vérifier que le document n'est pas en brouillon
        if document.statut == 'BROUILLON':
            raise serializers.ValidationError(_("Le document est encore en brouillon"))
        
        # Vérifier la validité du document
        if not document.est_valide:
            raise serializers.ValidationError(_("Le document n'est plus valide"))
        
        # Vérifier l'existence du fichier
        if not document.fichier or not document.fichier.storage.exists(document.fichier.name):
            raise serializers.ValidationError(_("Le fichier n'existe pas sur le serveur"))
        
        return data


class MultipleDocumentDownloadSerializer(serializers.Serializer):
    """Serializer pour télécharger plusieurs documents"""
    
    document_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        min_length=1,
        max_length=50,  # Limite pour éviter les abus
        help_text=_("Liste des IDs des documents à télécharger")
    )
    
    format = serializers.ChoiceField(
        choices=[
            ('zip', _("Archive ZIP")),
            ('separate', _("Fichiers séparés (multi-part)")),
        ],
        default='zip',
        required=False
    )
    
    compress_level = serializers.IntegerField(
        min_value=0,
        max_value=9,
        default=6,
        required=False,
        help_text=_("Niveau de compression (0-9)")
    )
    
    def validate_document_ids(self, value):
        """Valider que tous les documents existent"""
        documents = Document.objects.filter(id__in=value)
        
        if len(documents) != len(value):
            found_ids = set(documents.values_list('id', flat=True))
            missing_ids = set(value) - found_ids
            raise serializers.ValidationError(
                _("Documents non trouvés: {ids}").format(ids=list(missing_ids))
            )
        
        self.context['documents'] = documents
        return value
    
    def validate(self, data):
        """Validation globale"""
        documents = self.context.get('documents', [])
        request = self.context.get('request')
        
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError(_("Authentification requise"))
        
        user = request.user
        
        # Vérifier les permissions pour chaque document
        for document in documents:
            # Vérifier la confidentialité
            if document.niveau_confidentialite == 'CONFIDENTIEL':
                if not user.has_perm('documents.view_confidential_documents'):
                    raise serializers.ValidationError(
                        _("Permission insuffisante pour le document: {ref}").format(
                            ref=document.reference
                        )
                    )
            elif document.niveau_confidentialite == 'TRES_CONFIDENTIEL':
                if not (user.has_perm('documents.view_confidential_documents') and user.is_staff):
                    raise serializers.ValidationError(
                        _("Permission insuffisante pour le document: {ref}").format(
                            ref=document.reference
                        )
                    )
        
        return data


class DocumentDownloadHistorySerializer(serializers.Serializer):
    """Serializer pour l'historique des téléchargements"""
    
    date = serializers.DateTimeField()
    utilisateur = serializers.CharField()
    document_reference = serializers.CharField()
    document_titre = serializers.CharField()
    format = serializers.CharField()
    taille = serializers.CharField()
    ip_address = serializers.IPAddressField(required=False)
    user_agent = serializers.CharField(required=False, allow_blank=True)

# serializers/document_serializers.py (suite)
class DocumentListSerializer(serializers.ModelSerializer):
    """Serializer pour lister les documents"""
    
    dossier = serializers.StringRelatedField()
    client = serializers.StringRelatedField()
    categorie = serializers.StringRelatedField()
    taille_lisible = serializers.SerializerMethodField()
    est_valide = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id',
            'reference',
            'titre',
            'description',
            'categorie',
            'dossier',
            'client',
            'fichier',
            'taille_lisible',
            'extension',
            'statut',
            'niveau_confidentialite',
            'date_document',
            'date_validite',
            'est_valide',
            'version',
            'date_upload',
            'uploade_par',
        ]
    
    def get_taille_lisible(self, obj):
        return obj.taille_lisible
    
    def get_est_valide(self, obj):
        return obj.est_valide