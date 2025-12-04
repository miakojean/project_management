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
from .client import Client

class Dossier(models.Model):
    """
    Modèle représentant un dossier juridique
    """
    
    TYPE_DOSSIER_CHOICES = [
        ('CONSTITUTION', 'Constitution de société'),
        ('MODIFICATION', 'Modification statutaire'),
        ('DISSOLUTION', 'Dissolution/Liquidation'),
        ('CONTENTIEUX', 'Contentieux'),
        ('CONSEIL', 'Conseil juridique'),
        ('CONTRAT', 'Rédaction de contrat'),
        ('AUDIT', 'Audit juridique'),
        ('PROPRIETE_INTELLECTUELLE', 'Propriété intellectuelle'),
        ('FUSION_ACQUISITION', 'Fusion/Acquisition'),
        ('RECOUVREMENT', 'Recouvrement de créances'),
        ('AUTRE', 'Autre'),
    ]
    
    STATUT_CHOICES = [
        ('NOUVEAU', 'Nouveau'),
        ('AJOUT_PIECE', 'ajouts piece'),
        ('DOCU_FONDA', 'Documents fondamentaux'),
        ('EN_COURS', 'En cours'),
        ('EN_ATTENTE', 'En attente (client)'),
        ('BLOQUE', 'Bloqué'),
        ('TERMINE', 'Terminé'),
        ('CLOTURE', 'Clôturé'),
        ('ANNULE', 'Annulé'),
    ]
    
    PRIORITE_CHOICES = [
        ('BASSE', 'Basse'),
        ('NORMALE', 'Normale'),
        ('HAUTE', 'Haute'),
        ('URGENTE', 'Urgente'),
    ]
    
    # Identification
    reference_dossier = models.CharField(_("Référence dossier"), max_length=50, unique=True, editable=False)
    titre = models.CharField(_("Titre du dossier"), max_length=200)
    type_dossier = models.CharField(_("Type de dossier"), max_length=30, choices=TYPE_DOSSIER_CHOICES)
    description = models.TextField(_("Description détaillée"), blank=True)
    chemin_dossier = models.CharField(_("Chemin du dossier"), max_length=500, blank=True, editable=False)

    # Client et parties
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='dossiers',
        verbose_name=_("Client principal")
    )
    
    # Gestion du dossier
    statut = models.CharField(_("Statut"), max_length=15, choices=STATUT_CHOICES, default='NOUVEAU')
    priorite = models.CharField(_("Priorité"), max_length=10, choices=PRIORITE_CHOICES, default='NORMALE')
    
    collaborateurs = models.ManyToManyField(
        Utilisateur,
        blank=True,
        related_name='dossiers_collabores',
        verbose_name=_("Collaborateurs")
    )
    
    # Dates importantes
    date_ouverture = models.DateField(_("Date d'ouverture"), default=timezone.now)
    date_cloture = models.DateField(_("Date de clôture"), null=True, blank=True)
    date_echeance = models.DateField(_("Date d'échéance"), null=True, blank=True)
    date_derniere_activite = models.DateTimeField(_("Date dernière activité"), auto_now=True)
    
    # Aspects financiers
    honoraires_prevus = models.DecimalField(
        _("Honoraires prévus (FCFA)"),
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=True,
        blank=True
    )
    
    honoraires_factures = models.DecimalField(
        _("Honoraires facturés (FCFA)"),
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    acompte_recu = models.DecimalField(
        _("Acompte reçu (FCFA)"),
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Informations juridiques spécifiques
    numero_tribunal = models.CharField(_("Numéro tribunal/greffe"), max_length=100, blank=True)
    juridiction = models.CharField(_("Juridiction compétente"), max_length=100, blank=True)
    numero_rg = models.CharField(_("Numéro RG (Rôle Général)"), max_length=100, blank=True)
    
    # Suivi et notes
    observations = models.TextField(_("Observations internes"), blank=True)
    actions_requises = models.TextField(_("Actions à effectuer"), blank=True)
    
    # Archivage
    est_archive = models.BooleanField(_("Archivé"), default=False)
    localisation_physique = models.CharField(
        _("Localisation physique"),
        max_length=200,
        blank=True,
        help_text=_("Emplacement physique du dossier (armoire, étagère...)")
    )
    
    # Métadonnées
    date_creation = models.DateTimeField(_("Date de création"), auto_now_add=True)
    date_modification = models.DateTimeField(_("Date de modification"), auto_now=True)
    cree_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='dossiers_crees',
        verbose_name=_("Créé par")
    )
    
    class Meta:
        ordering = ['-date_ouverture', '-date_creation']
        verbose_name = _("Dossier")
        verbose_name_plural = _("Dossiers")
        indexes = [
            models.Index(fields=['reference_dossier']),
            models.Index(fields=['client', 'statut']),
            models.Index(fields=['type_dossier', 'statut']),
            models.Index(fields=['date_echeance']),
            models.Index(fields=['-date_derniere_activite']),
        ]
        permissions = [
            ("view_all_dossiers", "Peut voir tous les dossiers"),
            ("archive_dossier", "Peut archiver un dossier"),
            ("manage_financial", "Peut gérer les aspects financiers"),
        ]
        unique_together = ('titre', 'client')
    
    def __str__(self):
        return f"{self.reference_dossier} - {self.titre}"
    
    def save(self, *args, **kwargs):
        # ===================================================================
        # 1. Génération de la référence dossier (uniquement à la création)
        # ===================================================================
        if not self.reference_dossier:
            year = timezone.now().year
            type_prefixes = {
                'CONSTITUTION': 'CONST',
                'MODIFICATION': 'MODIF',
                'DISSOLUTION': 'DISS',
                'CONTENTIEUX': 'CONT',
                'CONSEIL': 'CONS',
                'CONTRAT': 'CNTR',
                'AUDIT': 'AUD',
                'PROPRIETE_INTELLECTUELLE': 'PI',
                'FUSION_ACQUISITION': 'MA',
                'RECOUVREMENT': 'REC',
                'AUTRE': 'AUT',
            }
            prefix = type_prefixes.get(self.type_dossier, 'DOS')

            last_dossier = Dossier.objects.filter(
                reference_dossier__startswith=f"{prefix}-{year}"
            ).order_by('-reference_dossier').first()

            new_num = 1
            if last_dossier:
                try:
                    last_num = int(last_dossier.reference_dossier.split('-')[-1])
                    new_num = last_num + 1
                except (ValueError, IndexError):
                    pass

            self.reference_dossier = f"{prefix}-{year}-{new_num:05d}"

        # ===================================================================
        # 2. Valeurs par défaut importantes
        # ===================================================================
        if not self.date_ouverture:
            self.date_ouverture = timezone.now().date()

        if self.statut in ['CLOTURE', 'ANNULE'] and not self.date_cloture:
            self.date_cloture = timezone.now().date()

        # ===================================================================
        # 3. Chemin physique du dossier client (création unique)
        # ===================================================================
        if not self.chemin_dossier and self.client:
            base_path = os.path.join(settings.MEDIA_ROOT, 'dossiers_clients')
            nom_dossier_client = self.client.creer_nom_dossier_securise()
            self.chemin_dossier = os.path.join(base_path, nom_dossier_client)

        # ===================================================================
        # 4. Sauvegarde principale (une seule fois !)
        # ===================================================================
        super().save(*args, **kwargs)

        # ===================================================================
        # 5. Création physique du dossier sur disque (après sauvegarde)
        # ===================================================================
        if self.chemin_dossier and not os.path.exists(self.chemin_dossier):
            self.creer_dossier_client()

        # ===================================================================
        # 6. AUTOMATISATION DES 5 STATUTS FONDAMENTAUX + SOUS-STATUT
        # ===================================================================
        # On ne fait ces vérifications que si un document vient d’être lié
        # (déclenché depuis Document.save() via signal ou manuellement)
        if kwargs.get('force_status_update') or self.documents.exists():
            docs = self.documents
            etapes = self.etapes

            # --- 1. Premier document → EN_COURS ---
            if self.statut == 'NOUVEAU' and docs.exists():
                self.statut = 'EN_COURS'
                self.sous_statut = 'AJOUT_PIECE'
                self.save(update_fields=['statut', 'sous_statut'])
                return  # on arrête ici pour ce cycle

            # --- 2. Tous les documents fondamentaux reçus ? ---
            docs_fondamentaux = docs.filter(categorie__est_fondamentale=True)
            if (self.statut == 'EN_COURS' and 
                docs_fondamentaux.exists() and 
                docs_fondamentaux.filter(statut__in=['VALIDE', 'SIGNE']).count() == docs_fondamentaux.count()):

                # CORRECTION ICI : Utiliser le code défini dans STATUT_CHOICES
                self.statut = 'DOCU_FONDA'  # Au lieu de 'EN_ATTENTE_VALIDATION'
                self.sous_statut = 'DOCS_FONDAMENTAUX'
                self.save(update_fields=['statut', 'sous_statut'])
                return

            # --- 3. Tout est terminé (docs + étapes) → TERMINE ---
            if (self.statut in ['EN_COURS', 'EN_ATTENTE_VALIDATION'] and
                docs.exists() and 
                docs.filter(statut__in=['VALIDE', 'SIGNE']).count() == docs.count() and
                etapes.exists() and 
                etapes.filter(est_terminee=True).count() == etapes.count()):

                self.statut = 'TERMINE'
                self.sous_statut = ''
                self.date_cloture = timezone.now().date()
                self.save(update_fields=['statut', 'sous_statut', 'date_cloture'])
    
    def creer_dossier_client(self):
        """Crée le dossier physique unique pour le client"""
        try:
            # CORRECTION: Un seul dossier plat, pas de sous-dossiers
            os.makedirs(self.chemin_dossier, exist_ok=True)
            print(f"✅ Dossier client créé: {self.chemin_dossier}")
            
        except Exception as e:
            print(f"❌ Erreur création dossier client: {e}")

    def ajouter_document_au_dossier(self, document_instance):
        """Déplace un document existant vers le dossier du client"""
        try:
            if not self.chemin_dossier or not os.path.exists(self.chemin_dossier):
                self.creer_dossier_client()
            
            # Chemin source et destination
            ancien_chemin = document_instance.fichier.path
            nom_fichier = os.path.basename(ancien_chemin)
            nouveau_chemin = os.path.join(self.chemin_dossier, nom_fichier)
            
            # Déplace le fichier
            os.rename(ancien_chemin, nouveau_chemin)
            
            # Met à jour le champ fichier
            document_instance.fichier.name = os.path.relpath(
                nouveau_chemin, settings.MEDIA_ROOT
            )
            document_instance.save()
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur déplacement document: {e}")
            return False

    def lister_documents_du_dossier(self):
        """Liste tous les documents du dossier client"""
        if not self.chemin_dossier or not os.path.exists(self.chemin_dossier):
            return []
        
        return [
            f for f in os.listdir(self.chemin_dossier)
            if os.path.isfile(os.path.join(self.chemin_dossier, f))
        ]

    def get_chemin_absolu(self):
        """Retourne le chemin absolu du dossier"""
        if self.chemin_dossier:
            return os.path.join(settings.MEDIA_ROOT, self.chemin_dossier)
        return None
    
    @property
    def est_en_retard(self):
        """Vérifie si le dossier est en retard par rapport à l'échéance"""
        if self.date_echeance and self.statut not in ['TERMINE', 'CLOTURE', 'ANNULE']:
            return timezone.now().date() > self.date_echeance
        return False
    
    @property
    def solde_honoraires(self):
        """Calcule le solde restant des honoraires"""
        if self.honoraires_prevus:
            return self.honoraires_prevus - self.honoraires_factures
        return Decimal('0.00')
    
    @property
    def solde_acompte(self):
        """Calcule le solde de l'acompte restant"""
        return self.acompte_recu - self.honoraires_factures
    
    # Dans models.py > Dossier > taux_avancement

    @property
    def taux_avancement(self):
        taux = {
            'NOUVEAU': 10,
            'EN_COURS': 30,
            'AJOUT_PIECE': 30,
            'DOCU_FONDA': 70,      # CORRECTION : Doit correspondre à STATUT_CHOICES et au save()
            'EN_ATTENTE': 50,      # Attention : EN_ATTENTE est souvent après EN_COURS
            'BLOQUE': 50,
            'TERMINE': 90,
            'CLOTURE': 100,
            'ANNULE': 0,
        }
        return taux.get(self.statut, 0)
    
    def get_duree_traitement(self):
        """Retourne la durée de traitement du dossier"""
        if self.date_cloture:
            return (self.date_cloture - self.date_ouverture).days
        return (timezone.now().date() - self.date_ouverture).days

class EtapeDossier(models.Model):
    """
    Modèle pour gérer les étapes d'un dossier
    """
    dossier = models.ForeignKey(
        Dossier,
        on_delete=models.CASCADE,
        related_name='etapes',
        verbose_name=_("Dossier")
    )
    nom = models.CharField(_("Nom de l'étape"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    ordre = models.PositiveIntegerField(_("Ordre"), default=1)
    date_debut = models.DateField(_("Date début"), null=True, blank=True)
    date_fin = models.DateField(_("Date fin"), null=True, blank=True)
    est_terminee = models.BooleanField(_("Est terminée"), default=False)
    
    date_creation = models.DateTimeField(_("Date de création"), auto_now_add=True)
    date_modification = models.DateTimeField(_("Date de modification"), auto_now=True)
    
    class Meta:
        ordering = ['dossier', 'ordre']
        verbose_name = _("Étape de dossier")
        verbose_name_plural = _("Étapes de dossier")
    
    def __str__(self):
        return f"{self.dossier.reference_dossier} - {self.nom}"