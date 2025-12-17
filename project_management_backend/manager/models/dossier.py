# models/dossier.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from .client import Client
from .category import CategorieDocument

Utilisateur = get_user_model()


class Dossier(models.Model):
    """
    Modèle représentant un dossier juridique avec système de scoring
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

        # ==================================================================
        # 2. Valeurs par défaut importantes                                 
        # ==================================================================
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

    def creer_dossier_client(self):
        """Crée le dossier physique unique pour le client"""
        try:
            os.makedirs(self.chemin_dossier, exist_ok=True)
        except Exception as e:
            print(f"❌ Erreur création dossier client: {e}")

    # ===================================================================
    # PROPRIÉTÉS DE SCORING (NOUVEAU)
    # ===================================================================
    
    @property
    def score_total(self):
        """Score maximum possible pour ce dossier (90 points max)"""
        from django.db.models import Sum
        total = CategorieDocument.objects.filter(
            est_actif=True
        ).aggregate(Sum('poids'))['poids__sum'] or 0
        return min(total, 90)  # Maximum 90 points
    
    @property
    def score_actuel(self):
        """Score actuel - DOIT UTILISER LA MÊME LOGIQUE QUE taux_avancement"""
        return self.taux_avancement  # ← À CHANGER!
    
    @property
    def taux_avancement(self):
        """Prend le poids maximum parmi les catégories avec documents"""
        max_poids = 10  # Base minimum de 10%
        
        for categorie in CategorieDocument.objects.filter(est_actif=True):
            # Vérifier si cette catégorie a au moins un document dans ce dossier
            if self.documents.filter(categorie=categorie).exists():
                # Si le poids de cette catégorie est supérieur au maximum actuel
                if categorie.poids > max_poids:
                    max_poids = categorie.poids
        
        # Limiter à 100% maximum
        return min(max_poids, 100)
    
    @property
    def avancement_detaille(self):
        """Retourne un dict détaillé de l'avancement par catégorie"""
        details = {
            'score_total': 100,
            'score_actuel': self.taux_avancement,
            'pourcentage': self.taux_avancement,
            'categories': []
        }
        
        for categorie in CategorieDocument.objects.filter(est_actif=True):
            has_document = self.documents.filter(categorie=categorie).exists()
            has_valid_document = self.documents.filter(
                categorie=categorie, statut__in=['VALIDE', 'SIGNE']
            ).exists()
            
            details['categories'].append({
                'categorie_id': categorie.id,
                'categorie_nom': categorie.nom,
                'poids': categorie.poids,
                'est_obligatoire': categorie.est_obligatoire,
                'est_fondamentale': categorie.est_fondamentale,
                'a_document': has_document,
                'a_document_valide': has_valid_document,
                'contribution': categorie.poids if has_document else 0
            })
        
        return details
    
    @property
    def prochaine_etape(self):
        """Suggère la prochaine étape basée sur le scoring"""
        details = self.avancement_detaille
        
        for cat in details['categories']:
            if cat['est_obligatoire'] and not cat['a_document']:
                return {
                    'action': f"Obtenir un document : {cat['categorie_nom']}",
                    'priorite': 'HAUTE' if cat['poids'] >= 20 else 'MOYENNE',
                    'categorie_id': cat['categorie_id']
                }
        
        return {
            'action': "Finaliser les documents optionnels",
            'priorite': 'BASSE',
            'categorie_id': None
        }
    
    @property
    def est_en_retard(self):
        """Vérifie si le dossier est en retard par rapport à l'échéance"""
        if self.date_echeance and self.statut not in ['TERMINE', 'CLOTURE', 'ANNULE']:
            return timezone.now().date() > self.date_echeance
        return False
    
    @property
    def est_en_retard_score(self):
        """Vérifie si le dossier est en retard basé sur le scoring"""
        if self.get_duree_traitement() > 30 and self.score_actuel < 50:
            return True
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
    
    # ===================================================================
    # MÉTHODES UTILITAIRES
    # ===================================================================
    
    def get_duree_traitement(self):
        """Retourne la durée de traitement du dossier en jours"""
        if self.date_cloture:
            return (self.date_cloture - self.date_ouverture).days
        return (timezone.now().date() - self.date_ouverture).days
    
    def mettre_a_jour_statut_par_score(self):
        if self.statut in ['ANNULE', 'CLOTURE', 'TERMINE']:
            return
        
        pourcentage = self.taux_avancement
        nouveau_statut = self.statut
        
        # Seuils fixes basés sur vos catégories (corrigés)
        if pourcentage <= 10:
            nouveau_statut = 'NOUVEAU'
        elif pourcentage <= 45:  # Identification
            nouveau_statut = 'EN_COURS'
        elif pourcentage <= 60:  # Constitutifs
            nouveau_statut = 'EN_COURS'
        elif pourcentage <= 75:  # Procédures
            nouveau_statut = 'EN_ATTENTE'
        elif pourcentage <= 95:  # Opérationnels
            nouveau_statut = 'EN_ATTENTE_VALIDATION'
        else:  # 96-100% = Livrables
            nouveau_statut = 'TERMINE'
        
        if nouveau_statut != self.statut:
            self.statut = nouveau_statut
            self.save(update_fields=['statut'])
    
    def ajouter_document_au_dossier(self, document_instance):
        """Déplace un document existant vers le dossier du client"""
        try:
            if not self.chemin_dossier or not os.path.exists(self.chemin_dossier):
                self.creer_dossier_client()
            
            ancien_chemin = document_instance.fichier.path
            nom_fichier = os.path.basename(ancien_chemin)
            nouveau_chemin = os.path.join(self.chemin_dossier, nom_fichier)
            
            os.rename(ancien_chemin, nouveau_chemin)
            
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
    
class Commentaire(models.Model):
    """
    Modèle simple pour les commentaires sur les dossiers
    """
    dossier = models.ForeignKey(
        Dossier,
        on_delete=models.CASCADE,
        related_name='commentaires',
        verbose_name=_("Dossier")
    )
    auteur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='commentaires',
        verbose_name=_("Auteur")
    )
    message = models.TextField(_("Message"))
    
    date_creation = models.DateTimeField(_("Date de création"), auto_now_add=True)
    date_modification = models.DateTimeField(_("Date de modification"), auto_now=True)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = _("Commentaire")
        verbose_name_plural = _("Commentaires")
    
    def __str__(self):
        return f"Commentaire sur {self.dossier.reference_dossier} par {self.auteur}"


class Reponse(models.Model):
    """
    Modèle simple pour les réponses aux commentaires
    """
    commentaire = models.ForeignKey(
        Commentaire,
        on_delete=models.CASCADE,
        related_name='reponses',
        verbose_name=_("Commentaire")
    )
    auteur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='reponses',
        verbose_name=_("Auteur")
    )
    message = models.TextField(_("Message"))
    
    date_creation = models.DateTimeField(_("Date de création"), auto_now_add=True)
    
    class Meta:
        ordering = ['date_creation']
        verbose_name = _("Réponse")
        verbose_name_plural = _("Réponses")
    
    def __str__(self):
        return f"Réponse à {self.commentaire}"