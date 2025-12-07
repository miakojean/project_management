from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Récupère le modèle utilisateur configuré (généralement auth.User)
User = get_user_model()

class Notification(models.Model):
    """
    Modèle pour stocker une notification dans l'application.
    """

    # --- Destinataire et Émetteur ---

    # L'utilisateur qui reçoit la notification
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="Destinataire"
    )

    # L'utilisateur qui a déclenché l'action (optionnel)
    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='actions_initiated',
        verbose_name="Acteur"
    )

    # --- Contenu et Type ---
    
    # Types d'événements (pour un rendu facile)
    EVENT_CHOICES = (
        ('DOSSIER_CREATION', 'Dossier créé'),
        ('DOSSIER_MISE_A_JOUR', 'Dossier mis à jour'),
        ('DOCUMENT_TELEVERSE', 'Document téléversé'),
        ('DOCUMENT_SUPPRIME', 'Document supprimé'),
        ('CLIENT_AJOUTE', 'Nouveau client ajouté'),
        # Ajoutez d'autres types d'événements ici
    )
    
    # Le type d'événement qui a déclenché la notification
    verb = models.CharField(
        max_length=50,
        choices=EVENT_CHOICES,
        verbose_name="Action"
    )

    # Le message affiché à l'utilisateur
    message = models.TextField(verbose_name="Message de notification")

    # --- Statut et Temps ---

    # Si la notification a été lue ou non
    is_read = models.BooleanField(default=False, verbose_name="Lue")

    # Date et heure de création
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créée le")
    
    # --- Lien vers l'objet source (Generic Foreign Key) ---

    # Contient le modèle de l'objet source (ex: 'Dossier' ou 'Document')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    
    # L'ID de l'objet source (ex: l'ID du Dossier ou du Document)
    object_id = models.PositiveIntegerField()
    
    # Champ calculé pour accéder directement à l'objet source (Dossier, Document...)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"[{'LU' if self.is_read else 'NON LU'}] {self.recipient.email} - {self.get_verb_display()}"