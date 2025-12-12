from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    """
    Modèle pour stocker une notification dans l'application.
    Supporte plusieurs destinataires via une relation ManyToMany.
    """

    # --- Émetteur ---
    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='actions_initiated',
        verbose_name="Acteur"
    )

    # --- Contenu et Type ---
    EVENT_CHOICES = (
        ('DOSSIER_CREATION', 'Dossier créé'),
        ('DOSSIER_MISE_A_JOUR', 'Dossier mis à jour'),
        ('DOCUMENT_TELEVERSE', 'Document téléversé'),
        ('DOCUMENT_SUPPRIME', 'Document supprimé'),
        ('CLIENT_AJOUTE', 'Nouveau client ajouté'),
    )
    
    verb = models.CharField(
        max_length=50,
        choices=EVENT_CHOICES,
        verbose_name="Action"
    )

    message = models.TextField(verbose_name="Message de notification")

    # --- Destinataires (plusieurs) ---
    recipients = models.ManyToManyField(
        User,
        through='NotificationRecipient',
        related_name='notifications',
        verbose_name="Destinataires"
    )

    # --- Statut et Temps ---
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créée le")
    
    # --- Lien vers l'objet source ---
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"{self.get_verb_display()} - {self.recipients.count()} destinataire(s)"


class NotificationRecipient(models.Model):
    """
    Table intermédiaire pour gérer le statut de lecture par utilisateur.
    """
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False, verbose_name="Lue")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="Lue le")

    class Meta:
        unique_together = ['notification', 'recipient']
        verbose_name = "Destinataire de notification"
        verbose_name_plural = "Destinataires de notifications"

    def mark_as_read(self):
        if self.is_read:
            return False # Déjà lu, rien à faire
        
        self.is_read = True
        self.read_at = timezone.now() # Assurez-vous d'utiliser django.utils.timezone
        self.save()
        return True # Marqué comme lu