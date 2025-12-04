from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinValueValidator, FileExtensionValidator, MaxValueValidator
from django.utils import timezone
from account.models import Utilisateur
from decimal import Decimal
import os
from django.conf import settings
import re
from unidecode import unidecode 

class CategorieDocument(models.Model):
    """
    Modèle pour catégoriser les documents avec système de scoring
    """
    nom = models.CharField(_("Nom"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True)
    code = models.CharField(_("Code"), max_length=20, unique=True, help_text=_("Code court pour référencement"))
    est_fondamentale = models.BooleanField(default=False, verbose_name="Document fondamental")
    
    # NOUVEAU: Système de scoring
    poids = models.IntegerField(
        _("Poids dans l'avancement"),
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text=_("Importance de cette catégorie dans l'avancement global (1-100)")
    )
    
    est_obligatoire = models.BooleanField(
        _("Obligatoire"),
        default=False,
        help_text=_("Cette catégorie est-elle obligatoire pour terminer le dossier ?")
    )
    
    # Paramètres d'évaluation
    delai_max = models.IntegerField(
        _("Délai maximum (jours)"),
        null=True,
        blank=True,
        help_text=_("Délai maximum pour obtenir ce type de document")
    )
    
    # Paramètres
    couleur = models.CharField(
        _("Couleur"),
        max_length=7,
        default='#3498db',
        help_text=_("Couleur hex pour l'interface (#RRGGBB)")
    )
    icone = models.CharField(
        _("Icône"),
        max_length=50,
        blank=True,
        help_text=_("Nom de l'icône (ex: file-text, certificate, etc.)")
    )
    
    # Organisation
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sous_categories',
        verbose_name=_("Catégorie parente")
    )
    
    ordre = models.PositiveIntegerField(_("Ordre"), default=1)
    est_actif = models.BooleanField(_("Est actif"), default=True)
    
    date_creation = models.DateTimeField(_("Date de création"), auto_now_add=True)
    date_modification = models.DateTimeField(_("Date de modification"), auto_now=True)
    
    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = _("Catégorie de document")
        verbose_name_plural = _("Catégories de documents")
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.nom} > {self.nom}"
        return self.nom
    
    # NOUVEAU: Méthodes pour le scoring
    @property
    def score_max(self):
        """Retourne le score maximum pour cette catégorie"""
        return self.poids
    
    @property
    def est_critique(self):
        """Détermine si la catégorie est critique"""
        return self.est_obligatoire and self.poids >= 30
