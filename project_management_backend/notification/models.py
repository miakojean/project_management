from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.urls import reverse 

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

class Insight(models.Model):
    """
    Modèle pour les informations internes de l'organisation
    """
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Brouillon'
        PUBLISHED = 'published', 'Publié'
        ARCHIVED = 'archived', 'Archivé'
        RESTRICTED = 'restricted', 'Accès restreint'
    
    class Category(models.TextChoices):
        TECHNOLOGY = 'technology', 'Technologie'
        STRATEGY = 'strategy', 'Stratégie'
        MARKETING = 'marketing', 'Marketing'
        FINANCE = 'finance', 'Finances'
        HR = 'hr', 'Ressources Humaines'
        OPERATIONS = 'operations', 'Opérations'
        SALES = 'sales', 'Ventes'
        INNOVATION = 'innovation', 'Innovation'
        GENERAL = 'general', 'Général'
    
    class ConfidentialityLevel(models.IntegerChoices):
        PUBLIC = 1, 'Public (Tous les employés)'
        INTERNAL = 2, 'Interne (Employés confirmés)'
        CONFIDENTIAL = 3, 'Confidentiel (Managers+)'
        RESTRICTED = 4, 'Restreint (Direction)'
    
    # Informations principales
    title = models.CharField(
        max_length=200,
        verbose_name="Titre",
        help_text="Titre explicite de l'information"
    )
    
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publication_date',
        verbose_name="Slug",
        help_text="URL conviviale pour le référencement"
    )
    
    excerpt = models.TextField(
        max_length=500,
        verbose_name="Résumé",
        help_text="Court résumé (max 500 caractères)",
        blank=True
    )
    
    content = models.TextField(
        verbose_name="Contenu",
        help_text="Contenu détaillé de l'information"
    )
    
    # Métadonnées
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='insights',
        verbose_name="Auteur"
    )
    
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.GENERAL,
        verbose_name="Catégorie"
    )
    
    confidentiality_level = models.IntegerField(
        choices=ConfidentialityLevel.choices,
        default=ConfidentialityLevel.INTERNAL,
        verbose_name="Niveau de confidentialité"
    )
    
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Statut"
    )
    
    # Dates importantes
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    last_modified = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )
    
    publication_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date de publication",
        help_text="Date de publication planifiée"
    )
    
    expiration_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date d'expiration",
        help_text="Date à laquelle l'information n'est plus pertinente"
    )
    
    # Gestion des fichiers
    attachment = models.FileField(
        upload_to='insights/attachments/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Pièce jointe"
    )
    
    thumbnail = models.ImageField(
        upload_to='insights/thumbnails/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Image de couverture",
        help_text="Image représentative (format recommandé: 1200x630px)"
    )
    
    # Métriques et engagement
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de vues"
    )
    
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Mettre en avant",
        help_text="Afficher en première page"
    )
    
    allow_comments = models.BooleanField(
        default=True,
        verbose_name="Autoriser les commentaires"
    )
    
    # Relations
    related_insights = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        verbose_name="Informations connexes"
    )
    
    class Meta:
        verbose_name = "Information interne"
        verbose_name_plural = "Informations internes"
        ordering = ['-publication_date', '-creation_date']
        permissions = [
            ('view_confidential', 'Peut voir les informations confidentielles'),
            ('publish_insight', 'Peut publier des informations'),
            ('manage_insights', 'Peut gérer toutes les informations'),
        ]
        indexes = [
            models.Index(fields=['status', 'publication_date']),
            models.Index(fields=['category', 'confidentiality_level']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    def get_absolute_url(self):
        """Retourne l'URL détaillée de l'information"""
        return reverse('insight_detail', kwargs={
            'year': self.publication_date.year,
            'month': self.publication_date.month,
            'day': self.publication_date.day,
            'slug': self.slug
        })
    
    def is_published(self):
        """Vérifie si l'information est publiée et non expirée"""
        now = timezone.now()
        is_active = (
            self.status == self.Status.PUBLISHED and 
            self.publication_date <= now
        )
        
        if self.expiration_date:
            is_active = is_active and (self.expiration_date >= now)
        
        return is_active
    
    def can_be_viewed_by(self, user):
        """Vérifie si l'utilisateur peut voir cette information"""
        # Les superutilisateurs voient tout
        if user.is_superuser:
            return True
        
        # Vérification du statut
        if not self.is_published():
            return False
        
        # Vérification du niveau de confidentialité
        user_level = self.get_user_confidentiality_level(user)
        return user_level >= self.confidentiality_level
    
    @staticmethod
    def get_user_confidentiality_level(user):
        """Détermine le niveau de confidentialité d'un utilisateur"""
        # Logique à adapter selon votre structure d'organisation
        if user.groups.filter(name='Direction').exists():
            return Insight.ConfidentialityLevel.RESTRICTED
        elif user.groups.filter(name='Managers').exists():
            return Insight.ConfidentialityLevel.CONFIDENTIAL
        elif user.is_staff:
            return Insight.ConfidentialityLevel.INTERNAL
        else:
            return Insight.ConfidentialityLevel.PUBLIC
    
    def increment_views(self):
        """Incrémente le compteur de vues"""
        self.views_count += 1
        self.save(update_fields=['views_count'])