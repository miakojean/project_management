# models/historique.py
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
from .document import Document

Utilisateur = get_user_model()

class HistoriqueDocument(models.Model):
    """
    Modèle pour tracer l'historique des actions sur un document
    """
    ACTION_CHOICES = [
        ('CREATION', 'Création'),
        ('MODIFICATION', 'Modification'),
        ('CONSULTATION', 'Consultation'),
        ('TELECHARGEMENT', 'Téléchargement'),
        ('VALIDATION', 'Validation'),
        ('SIGNATURE', 'Signature'),
        ('ENVOI', 'Envoi'),
        ('ARCHIVAGE', 'Archivage'),
        ('SUPPRESSION', 'Suppression'),
        ('PARTAGE', 'Partage'),
    ]
    
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='historique'
    )
    
    action = models.CharField(_("Action"), max_length=20, choices=ACTION_CHOICES)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, verbose_name=_("Utilisateur"))
    date_action = models.DateTimeField(_("Date action"), auto_now_add=True)
    
    details = models.TextField(
        _("Détails"),
        blank=True,
        help_text=_("Détails supplémentaires sur l'action")
    )
    
    adresse_ip = models.GenericIPAddressField(_("Adresse IP"), null=True, blank=True)
    
    class Meta:
        ordering = ['-date_action']
        verbose_name = _("Historique de document")
        verbose_name_plural = _("Historiques de documents")
    
    def __str__(self):
        return f"{self.document.reference} - {self.get_action_display()} par {self.utilisateur} le {self.date_action}"