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
from .document import Document

class SignatureDocument(models.Model):
    """
    Modèle intermédiaire pour gérer les signatures de documents
    """
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='signatures'
    )
    
    signataire = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='signatures'
    )
    
    ordre_signature = models.PositiveIntegerField(
        _("Ordre signature"),
        default=1,
        help_text=_("Ordre dans lequel le signataire doit signer")
    )
    
    a_signe = models.BooleanField(_("A signé"), default=False)
    date_signature = models.DateTimeField(_("Date signature"), null=True, blank=True)
    commentaire = models.TextField(_("Commentaire"), blank=True)
    
    # Traçabilité technique
    adresse_ip = models.GenericIPAddressField(_("Adresse IP"), null=True, blank=True)
    empreinte_numerique = models.CharField(
        _("Empreinte numérique"),
        max_length=64,
        blank=True,
        help_text=_("Hash SHA-256 du document au moment de la signature")
    )
    
    date_creation = models.DateTimeField(_("Date de création"), auto_now_add=True)
    
    class Meta:
        ordering = ['document', 'ordre_signature']
        verbose_name = _("Signature de document")
        verbose_name_plural = _("Signatures de documents")
        unique_together = ['document', 'signataire']
    
    def __str__(self):
        statut = "✓ Signé" if self.a_signe else "En attente"
        return f"{self.document.reference} - {self.signataire.get_full_name()} ({statut})"
    
    def signer(self, ip_address=None):
        """Enregistre la signature"""
        self.a_signe = True
        self.date_signature = timezone.now()
        self.adresse_ip = ip_address
        
        import hashlib
        if self.document.fichier:
            hash_sha256 = hashlib.sha256()
            for chunk in self.document.fichier.chunks():
                hash_sha256.update(chunk)
            self.empreinte_numerique = hash_sha256.hexdigest()
        
        self.save()
        
        if self.document.est_signe_completement:
            self.document.statut = 'SIGNE'
            self.document.save()