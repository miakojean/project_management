from django.db import models
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _ 
import uuid
from django.utils import timezone
# Create your models here. 

class Utilisateur(AbstractUser):
    
    # Vu qu'il hérite de AbstractUser il a:
    # firstname, lastname, username, email, password

    class Responsabilities(models.TextChoices):
        DIRECTEUR = 'DR', _('Directeur')
        ASSISTANT = 'AS', _('Assistant')
        AUTRE = 'AU', _('Autre')
        # On va le terminer une fois avoir pris des informations

    phone_number = models.CharField(max_length=20, blank=True, null = True)
    category_title = models.CharField(max_length=3, choices=Responsabilities.choices, default=Responsabilities.DIRECTEUR, verbose_name=_("Catégorie")) # Pour la base de donnée relationnelle.

    def __str__(self):
        return f'Profile de {self.username}'

class PasswordResetToken(models.Model):
    user = models.ForeignKey(to=Utilisateur, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @classmethod
    def create_token(cls, user, expiration_hours=24):
        """" Méthode utilitaire pour créer un token avec expiration """
        token = cls(
            user = user, 
            expires_at = timezone.now() + timedelta(hours=expiration_hours))
        
        token.save()
        return token
    
    def is_valid(self):
        return self.expires_at > timezone.now()
    
    def __str__(self):
        return f'Token for {self.user.username}'