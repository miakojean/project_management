# models/document.py - VERSION CORRIGÉE
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os
from django.conf import settings
import re
from unidecode import unidecode

from django.contrib.auth import get_user_model 
from .client import Client  
from .dossier import Dossier
from .category import CategorieDocument

# Obtenez le modèle Utilisateur
Utilisateur = get_user_model()


def creer_nom_fichier_securise(filename):
    """Crée un nom de fichier sécurisé"""
    name, ext = os.path.splitext(filename)
    safe_name = unidecode(name)
    safe_name = re.sub(r'[^\w\s-]', '', safe_name)
    safe_name = re.sub(r'[-\s]+', '_', safe_name)
    safe_name = safe_name.strip('_')
    
    timestamp = str(int(timezone.now().timestamp()))[-6:]
    return f"{safe_name}_{timestamp}{ext}"


def document_upload_path(instance, filename):
    """
    Génère le chemin cohérent avec la structure des dossiers clients
    """
    if instance.dossier and instance.dossier.chemin_dossier:
        chemin_relatif = os.path.relpath(instance.dossier.chemin_dossier, settings.MEDIA_ROOT)
        nom_fichier_securise = creer_nom_fichier_securise(filename)
        return os.path.join(chemin_relatif, nom_fichier_securise)
    
    date = timezone.now()
    nom_fichier_securise = creer_nom_fichier_securise(filename)
    return f"documents/sans_dossier/{date.year}/{date.month:02d}/{nom_fichier_securise}"


class Document(models.Model):
    """
    Modèle pour la gestion des documents juridiques
    """
    
    STATUT_DOCUMENT_CHOICES = [
        ('BROUILLON', 'Brouillon'),
        ('EN_ATTENTE_VALIDATION', 'En attente de validation'),
        ('VALIDE', 'Validé'),
        ('SIGNE', 'Signé'),
        ('ENVOYE', 'Envoyé'),
        ('ARCHIVE', 'Archivé'),
        ('PERIME', 'Périmé'),
        ('REJETE', 'Rejeté'),
    ]
    
    NIVEAU_CONFIDENTIALITE_CHOICES = [
        ('PUBLIC', 'Public'),
        ('INTERNE', 'Interne'),
        ('CONFIDENTIEL', 'Confidentiel'),
        ('TRES_CONFIDENTIEL', 'Très confidentiel'),
    ]
    
    # Identification
    reference = models.CharField(
        _("Référence du document"),
        max_length=100,
        unique=True,
        editable=False
    )
    titre = models.CharField(_("Titre du document"), max_length=300)
    description = models.TextField(_("Description"), blank=True)
    
    # Classification
    categorie = models.ForeignKey(
        CategorieDocument,
        on_delete=models.PROTECT,
        related_name='documents',
        verbose_name=_("Catégorie")
    )
    
    # Relations
    dossier = models.ForeignKey(
        Dossier,
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True,
        verbose_name=_("Dossier associé")
    )
    
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True,
        verbose_name=_("Client associé")
    )
    
    # Fichier
    fichier = models.FileField(
        _("Fichier"),
        upload_to=document_upload_path,
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx', 'odt', 'jpg', 'jpeg', 
                               'png', 'xlsx', 'xls', 'zip']
        )]
    )
    
    taille_fichier = models.BigIntegerField(
        _("Taille du fichier (octets)"),
        editable=False,
        null=True 
    )
    
    extension = models.CharField(_("Extension"), max_length=10, editable=False, blank=True)
    
    # Métadonnées du document
    numero_document = models.CharField(
        _("Numéro document"),
        max_length=100,
        blank=True,
        help_text=_("Numéro officiel du document")
    )
    
    date_document = models.DateField(
        _("Date du document"),
        null=True,
        blank=True,
        help_text=_("Date de création/signature du document original")
    )
    
    date_validite = models.DateField(
        _("Date de validité"),
        null=True,
        blank=True,
        help_text=_("Date jusqu'à laquelle le document est valide")
    )
    
    emetteur = models.CharField(
        _("Émetteur/Auteur"),
        max_length=200,
        blank=True,
        help_text=_("Personne ou organisme émetteur du document")
    )
    
    destinataire = models.CharField(_("Destinataire"), max_length=200, blank=True)
    
    # Statut et sécurité
    statut = models.CharField(
        _("Statut"),
        max_length=25,
        choices=STATUT_DOCUMENT_CHOICES,
        default='BROUILLON'
    )
    
    niveau_confidentialite = models.CharField(
        _("Niveau de confidentialité"),
        max_length=20,
        choices=NIVEAU_CONFIDENTIALITE_CHOICES,
        default='INTERNE'
    )
    
    est_original = models.BooleanField(
        _("Document original"),
        default=False,
        help_text=_("Cocher si c'est l'original physique ou numérique")
    )
    
    est_certifie_conforme = models.BooleanField(_("Certifié conforme"), default=False)
    
    # Signature et validation
    necessite_signature = models.BooleanField(_("Nécessite signature"), default=False)
    
    signataires = models.ManyToManyField(
        Utilisateur,
        through='SignatureDocument',
        related_name='documents_a_signer',
        verbose_name=_("Signataires")
    )
    
    valide_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents_valides',
        verbose_name=_("Validé par")
    )
    
    date_validation = models.DateTimeField(_("Date validation"), null=True, blank=True)
    
    # Versioning
    version = models.PositiveIntegerField(_("Version"), default=1)
    document_parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='versions',
        verbose_name=_("Document parent (version précédente)")
    )
    
    # Tags et recherche
    tags = models.CharField(
        _("Tags"),
        max_length=500,
        blank=True,
        help_text=_("Tags séparés par des virgules pour faciliter la recherche")
    )
    
    mots_cles = models.TextField(
        _("Mots-clés"),
        blank=True,
        help_text=_("Mots-clés pour la recherche full-text")
    )
    
    # Traçabilité
    uploade_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='documents_uploades',
        verbose_name=_("Uploadé par")
    )
    
    date_upload = models.DateTimeField(_("Date d'upload"), auto_now_add=True)
    date_modification = models.DateTimeField(_("Date de modification"), auto_now=True)
    
    derniere_consultation = models.DateTimeField(_("Dernière consultation"), null=True, blank=True)
    nombre_consultations = models.PositiveIntegerField(_("Nombre de consultations"), default=0)
    
    # Notes
    notes_internes = models.TextField(
        _("Notes internes"),
        blank=True,
        help_text=_("Notes visibles uniquement par l'équipe")
    )
    
    # Archivage
    est_archive = models.BooleanField(_("Est archivé"), default=False)
    date_archivage = models.DateTimeField(_("Date d'archivage"), null=True, blank=True)
    
    class Meta:
        ordering = ['-date_upload']
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['dossier', 'statut']),
            models.Index(fields=['client', 'categorie']),
            models.Index(fields=['categorie', 'statut']),
            models.Index(fields=['date_document']),
            models.Index(fields=['date_validite']),
            models.Index(fields=['-date_upload']),
        ]
        permissions = [
            ("view_confidential_documents", "Peut voir les documents confidentiels"),
            ("validate_document", "Peut valider un document"),
            ("sign_document", "Peut signer un document"),
            ("archive_document", "Peut archiver un document"),
        ]
    
    def __str__(self):
        return f"{self.reference} - {self.titre}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        if not self.reference:
            self.generer_reference()
        
        if self.dossier and not self.client:
            self.client = self.dossier.client
        
        if self.fichier:
            self.extension = os.path.splitext(self.fichier.name)[1].lower().lstrip('.')
            if hasattr(self.fichier, 'size'):
                self.taille_fichier = self.fichier.size
        
        super().save(*args, **kwargs)
        
        # =============================================================
        # MISE À JOUR DU STATUT DU DOSSIER
        # =============================================================
        if self.dossier:
            # 1. Mettre à jour le statut basé sur le scoring
            self.dossier.mettre_a_jour_statut_par_score()
            
            # 2. Ancienne logique (gardée pour compatibilité)
            if is_new and self.dossier.statut == 'NOUVEAU':
                self.dossier.statut = 'EN_COURS'
                self.dossier.save(update_fields=['statut'])
        
        # =============================================================
        # POUR LES MODIFICATIONS DE DOCUMENTS EXISTANTS
        # =============================================================
        elif not is_new and self.dossier:
            # Si un document existant est modifié, recalculer aussi
            self.dossier.mettre_a_jour_statut_par_score()
    
    def generer_reference(self):
        """Génère la référence unique du document"""
        year = timezone.now().year
        categorie_prefix = self.categorie.code[:4].upper() if self.categorie else "DOC"
        
        last_doc = Document.objects.filter(
            reference__startswith=f"{categorie_prefix}-{year}"
        ).order_by('-reference').first()
        
        new_num = 1
        if last_doc:
            try:
                last_num = int(last_doc.reference.split('-')[-1])
                new_num = last_num + 1
            except (ValueError, IndexError):
                pass
        
        self.reference = f"{categorie_prefix}-{year}-{new_num:06d}"
    
    def delete(self, *args, **kwargs):
        """Surcharger la suppression pour mettre à jour le dossier"""
        dossier = self.dossier  # Sauvegarder la référence avant suppression
        
        # Appeler la suppression parente
        result = super().delete(*args, **kwargs)
        
        # Mettre à jour le dossier après suppression
        if dossier:
            dossier.mettre_a_jour_statut_par_score()
        
        return result

    @property
    def est_valide(self):
        """Vérifie si le document est encore valide"""
        if self.date_validite:
            return timezone.now().date() <= self.date_validite
        return True
    
    @property
    def taille_lisible(self):
        """Retourne la taille du fichier dans un format lisible"""
        if not self.taille_fichier:
            return "N/A"
        
        taille = self.taille_fichier
        for unit in ['o', 'Ko', 'Mo', 'Go']:
            if taille < 1024.0:
                return f"{taille:.1f} {unit}"
            taille /= 1024.0 
        return f"{taille:.1f} To"
    
    @property
    def est_signe_completement(self):
        """Vérifie si tous les signataires ont signé"""
        if not self.necessite_signature:
            return None
        
        total_signataires = self.signataires.count()
        if total_signataires == 0:
            return False
        
        signatures_faites = self.signatures.filter(a_signe=True).count()
        return signatures_faites == total_signataires
    
    def enregistrer_consultation(self):
        """Enregistre une consultation du document"""
        self.derniere_consultation = timezone.now()
        self.nombre_consultations += 1
        self.save(update_fields=['derniere_consultation', 'nombre_consultations'])
    
    def creer_nouvelle_version(self, nouveau_fichier, user):
        """Crée une nouvelle version du document"""
        nouvelle_version = Document.objects.create(
            titre=self.titre,
            description=self.description,
            categorie=self.categorie,
            dossier=self.dossier,
            client=self.client,
            fichier=nouveau_fichier,
            numero_document=self.numero_document,
            date_document=timezone.now().date(),
            emetteur=self.emetteur,
            destinataire=self.destinataire,
            niveau_confidentialite=self.niveau_confidentialite,
            necessite_signature=self.necessite_signature,
            version=self.version + 1,
            document_parent=self,
            uploade_par=user,
            tags=self.tags
        )
        return nouvelle_version
