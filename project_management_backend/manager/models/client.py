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


class Client(models.Model):
    """
    Modèle représentant un client du cabinet juridique
    """
    
    TYPE_CLIENT_CHOICES = [
        ('PERSONNE_PHYSIQUE', 'Personne Physique'),
        ('PERSONNE_MORALE', 'Personne Morale'),
    ]
    
    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('INACTIF', 'Inactif'),
        ('PROSPECT', 'Prospect'),
        ('ARCHIVE', 'Archivé'),
    ]
    
    # Informations générales
    type_client = models.CharField(_("Type de client"), max_length=20, choices=TYPE_CLIENT_CHOICES)
    statut = models.CharField(_("Statut"), max_length=10, choices=STATUT_CHOICES, default='ACTIF')
    reference_client = models.CharField(_("Référence client"), max_length=50, unique=True, editable=False)
    
    # Personne Physique
    nom = models.CharField(_("Nom"), max_length=100, blank=True)
    prenoms = models.CharField(_("Prénoms"), max_length=100, blank=True)
    date_naissance = models.DateField(_("Date de naissance"), null=True, blank=True)
    lieu_naissance = models.CharField(_("Lieu de naissance"), max_length=100, blank=True)
    
    # Personne Morale
    raison_sociale = models.CharField(_("Raison sociale"), max_length=200, blank=True)
    forme_juridique = models.CharField(_("Forme juridique"), max_length=50, blank=True)
    numero_rccm = models.CharField(_("Numéro RCCM"), max_length=50, blank=True)
    numero_cc = models.CharField(_("Numéro Compte Contribuable"), max_length=50, blank=True)
    capital_social = models.DecimalField(_("Capital social"), max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Coordonnées
    adresse = models.TextField(_("Adresse"), blank=True)
    ville = models.CharField(_("Ville"), max_length=100, blank=True)
    commune = models.CharField(_("Commune"), max_length=100, blank=True)
    
    telephone_validator = RegexValidator(
        regex=r'^\+?[0-9]{8,15}$',
        message=_("Format: '+225XXXXXXXXXX' ou 'XXXXXXXXXX'")
    )
    
    telephone_1 = models.CharField(_("Téléphone 1"), validators=[telephone_validator], max_length=17)
    telephone_2 = models.CharField(_("Téléphone 2"), validators=[telephone_validator], max_length=17, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    
    # Informations juridiques complémentaires
    representant_legal_nom = models.CharField(_("Nom du représentant légal"), max_length=100, blank=True)
    representant_legal_fonction = models.CharField(_("Fonction du représentant"), max_length=100, blank=True)
    
    # Gestion administrative
    date_creation = models.DateTimeField(_("Date de création"), auto_now_add=True)
    date_modification = models.DateTimeField(_("Date de modification"), auto_now=True)
    date_premier_contact = models.DateField(_("Date premier contact"), default=timezone.now)
    notes = models.TextField(_("Notes"), blank=True, help_text=_("Notes internes sur le client"))
    
    # Relations
    charge_de_clientele = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='clients_geres',
        verbose_name=_("Chargé de clientèle")
    )
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
        indexes = [
            models.Index(fields=['reference_client']),
            models.Index(fields=['type_client', 'statut']),
            models.Index(fields=['raison_sociale']),
            models.Index(fields=['nom', 'prenoms']),
        ]
    
    def __str__(self):
        if self.type_client == 'PERSONNE_MORALE':
            return f"{self.raison_sociale} ({self.reference_client})"
        return f"{self.nom} {self.prenoms} ({self.reference_client})"
    
    def save(self, *args, **kwargs):
        if not self.reference_client:
            prefix = 'PM' if self.type_client == 'PERSONNE_MORALE' else 'PP'
            year = timezone.now().year
            last_client = Client.objects.filter(
                reference_client__startswith=f"{prefix}{year}"
            ).order_by('-reference_client').first()
            
            if last_client:
                last_num = int(last_client.reference_client[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.reference_client = f"{prefix}{year}{new_num:04d}"
        
        super().save(*args, **kwargs)
    
    @property
    def nom_complet(self):
        """Retourne le nom complet du client selon son type"""
        if self.type_client == 'PERSONNE_MORALE':
            return self.raison_sociale
        return f"{self.nom} {self.prenoms}"
    
    def creer_nom_dossier_securise(self):
        """Crée un nom de dossier sécurisé pour le client"""
        if self.type_client == 'PERSONNE_MORALE':
            nom_base = self.raison_sociale
        else:
            nom_base = f"{self.nom} {self.prenoms}"
        
        # Nettoyage du nom
        nom_base = unidecode(nom_base)
        nom_base = re.sub(r'[^\w\s-]', '', nom_base)
        nom_base = re.sub(r'[-\s]+', '_', nom_base)
        nom_base = nom_base.strip('_').upper()
        
        # Ajoute la référence client pour éviter les doublons
        return f"{nom_base}_{self.reference_client}"