from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinValueValidator, FileExtensionValidator
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
    statut = models.CharField(_("Statut"), max_length=10, choices=STATUT_CHOICES, default='PROSPECT')
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
    
    def __str__(self):
        return f"{self.reference_dossier} - {self.titre}"
    
    def save(self, *args, **kwargs):
        # Génération de la référence dossier
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
            
            if last_dossier:
                last_num = int(last_dossier.reference_dossier.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.reference_dossier = f"{prefix}-{year}-{new_num:05d}"
        
        # Gestion de la date de clôture
        if self.statut in ['CLOTURE', 'ANNULE'] and not self.date_cloture:
            self.date_cloture = timezone.now().date()

        # CORRECTION: Génération cohérente du chemin AVANT sauvegarde
        if not self.chemin_dossier and self.client:
            base_path = os.path.join(settings.MEDIA_ROOT, 'dossiers_clients')
            nom_dossier_client = self.client.creer_nom_dossier_securise()
            self.chemin_dossier = os.path.join(base_path, nom_dossier_client)

        # Sauvegarde d'abord
        super().save(*args, **kwargs)
        
        # CORRECTION: Création physique APRÈS sauvegarde
        if self.chemin_dossier and not os.path.exists(self.chemin_dossier):
            self.creer_dossier_client()

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
    
    @property
    def taux_avancement(self):
        """Calcule un taux d'avancement basé sur le statut"""
        taux = {
            'NOUVEAU': 0,
            'EN_COURS': 50,
            'EN_ATTENTE': 50,
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


class CategorieDocument(models.Model):
    """
    Modèle pour catégoriser les documents
    """
    nom = models.CharField(_("Nom"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True)
    code = models.CharField(_("Code"), max_length=20, unique=True, help_text=_("Code court pour référencement"))
    
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


def creer_nom_fichier_securise(filename):
    """Crée un nom de fichier sécurisé"""
    name, ext = os.path.splitext(filename)
    safe_name = unidecode(name)
    safe_name = re.sub(r'[^\w\s-]', '', safe_name)
    safe_name = re.sub(r'[-\s]+', '_', safe_name)
    safe_name = safe_name.strip('_')
    
    # Ajoute un timestamp pour éviter les doublons
    timestamp = str(int(timezone.now().timestamp()))[-6:]
    return f"{safe_name}_{timestamp}{ext}"


def document_upload_path(instance, filename):
    """
    CORRECTION: Génère le chemin cohérent avec la structure des dossiers clients
    """
    # Si le document est lié à un dossier, utilise son chemin
    if instance.dossier and instance.dossier.chemin_dossier:
        # Chemin relatif depuis MEDIA_ROOT
        chemin_relatif = os.path.relpath(instance.dossier.chemin_dossier, settings.MEDIA_ROOT)
        nom_fichier_securise = creer_nom_fichier_securise(filename)
        return os.path.join(chemin_relatif, nom_fichier_securise)
    
    # Fallback: structure par défaut pour les documents sans dossier
    date = timezone.now()
    nom_fichier_securise = creer_nom_fichier_securise(filename)
    return f"documents/sans_dossier/{date.year}/{date.month:02d}/{nom_fichier_securise}"


class Document(models.Model):
    """
    Modèle pour la gestion des documents juridiques
    """
    
    TYPE_DOCUMENT_CHOICES = [
        ('PIECE_IDENTITE', 'Pièce d\'identité'),
        ('STATUT', 'Statuts'),
        ('PROCES_VERBAL', 'Procès-verbal'),
        ('CONTRAT', 'Contrat'),
        ('COURRIER', 'Courrier'),
        ('ATTESTATION', 'Attestation'),
        ('CERTIFICAT', 'Certificat'),
        ('FACTURE', 'Facture'),
        ('RECU', 'Reçu'),
        ('ACTE', 'Acte juridique'),
        ('JUGEMENT', 'Jugement'),
        ('ORDONNANCE', 'Ordonnance'),
        ('ASSIGNATION', 'Assignation'),
        ('CONCLUSIONS', 'Conclusions'),
        ('MEMOIRE', 'Mémoire'),
        ('RAPPORT', 'Rapport'),
        ('NOTE', 'Note juridique'),
        ('CORRESPONDANCE', 'Correspondance'),
        ('FORMULAIRE', 'Formulaire administratif'),
        ('JUSTIFICATIF', 'Justificatif'),
        ('AUTRE', 'Autre'),
    ]
    
    STATUT_DOCUMENT_CHOICES = [
        ('BROUILLON', 'Brouillon'),
        ('EN_ATTENTE_VALIDATION', 'En attente de validation'),
        ('VALIDE', 'Validé'),
        ('SIGNE', 'Signé'),
        ('ENVOYE', 'Envoyé'),
        ('ARCHIVE', 'Archivé'),
        ('PERIME', 'Périmé'),
        ('REJETE', 'Rejeté'),
    ]
    
    NIVEAU_CONFIDENTIALITE_CHOICES = [
        ('PUBLIC', 'Public'),
        ('INTERNE', 'Interne'),
        ('CONFIDENTIEL', 'Confidentiel'),
        ('TRES_CONFIDENTIEL', 'Très confidentiel'),
    ]
    
    # Identification
    reference = models.CharField(
        _("Référence du document"),
        max_length=100,
        unique=True,
        editable=False
    )
    titre = models.CharField(_("Titre du document"), max_length=300)
    description = models.TextField(_("Description"), blank=True)
    
    # Classification
    type_document = models.CharField(
        _("Type de document"),
        max_length=30,
        choices=TYPE_DOCUMENT_CHOICES
    )
    categorie = models.ForeignKey(
        CategorieDocument,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents',
        verbose_name=_("Catégorie")
    )
    
    # Relations
    dossier = models.ForeignKey(
        Dossier,
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True,
        verbose_name=_("Dossier associé")
    )
    
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True,
        verbose_name=_("Client associé")
    )
    
    # Fichier
    fichier = models.FileField(
        _("Fichier"),
        upload_to=document_upload_path,
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx', 'odt', 'jpg', 'jpeg', 'png', 'xlsx', 'xls', 'zip']
        )]
    )
    
    taille_fichier = models.BigIntegerField(
        _("Taille du fichier (octets)"),
        editable=False,
        null=True
    )
    
    extension = models.CharField(_("Extension"), max_length=10, editable=False, blank=True)
    
    # Métadonnées du document
    numero_document = models.CharField(
        _("Numéro document"),
        max_length=100,
        blank=True,
        help_text=_("Numéro officiel du document (ex: numéro de jugement, numéro RCCM, etc.)")
    )
    
    date_document = models.DateField(
        _("Date du document"),
        null=True,
        blank=True,
        help_text=_("Date de création/signature du document original")
    )
    
    date_validite = models.DateField(
        _("Date de validité"),
        null=True,
        blank=True,
        help_text=_("Date jusqu'à laquelle le document est valide")
    )
    
    emetteur = models.CharField(
        _("Émetteur/Auteur"),
        max_length=200,
        blank=True,
        help_text=_("Personne ou organisme émetteur du document")
    )
    
    destinataire = models.CharField(_("Destinataire"), max_length=200, blank=True)
    
    # Statut et sécurité
    statut = models.CharField(
        _("Statut"),
        max_length=25,
        choices=STATUT_DOCUMENT_CHOICES,
        default='BROUILLON'
    )
    
    niveau_confidentialite = models.CharField(
        _("Niveau de confidentialité"),
        max_length=20,
        choices=NIVEAU_CONFIDENTIALITE_CHOICES,
        default='INTERNE'
    )
    
    est_original = models.BooleanField(
        _("Document original"),
        default=False,
        help_text=_("Cocher si c'est l'original physique ou numérique")
    )
    
    est_certifie_conforme = models.BooleanField(_("Certifié conforme"), default=False)
    
    # Signature et validation
    necessite_signature = models.BooleanField(_("Nécessite signature"), default=False)
    
    signataires = models.ManyToManyField(
        Utilisateur,
        through='SignatureDocument',
        related_name='documents_a_signer',
        verbose_name=_("Signataires")
    )
    
    valide_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents_valides',
        verbose_name=_("Validé par")
    )
    
    date_validation = models.DateTimeField(_("Date validation"), null=True, blank=True)
    
    # Versioning
    version = models.PositiveIntegerField(_("Version"), default=1)
    document_parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='versions',
        verbose_name=_("Document parent (version précédente)")
    )
    
    # Tags et recherche
    tags = models.CharField(
        _("Tags"),
        max_length=500,
        blank=True,
        help_text=_("Tags séparés par des virgules pour faciliter la recherche")
    )
    
    mots_cles = models.TextField(
        _("Mots-clés"),
        blank=True,
        help_text=_("Mots-clés pour la recherche full-text")
    )
    
    # Traçabilité
    uploade_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='documents_uploades',
        verbose_name=_("Uploadé par")
    )
    
    date_upload = models.DateTimeField(_("Date d'upload"), auto_now_add=True)
    date_modification = models.DateTimeField(_("Date de modification"), auto_now=True)
    
    derniere_consultation = models.DateTimeField(_("Dernière consultation"), null=True, blank=True)
    nombre_consultations = models.PositiveIntegerField(_("Nombre de consultations"), default=0)
    
    # Notes
    notes_internes = models.TextField(
        _("Notes internes"),
        blank=True,
        help_text=_("Notes visibles uniquement par l'équipe")
    )
    
    # Archivage
    est_archive = models.BooleanField(_("Est archivé"), default=False)
    date_archivage = models.DateTimeField(_("Date d'archivage"), null=True, blank=True)
    
    class Meta:
        ordering = ['-date_upload']
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['dossier', 'statut']),
            models.Index(fields=['client', 'type_document']),
            models.Index(fields=['type_document', 'statut']),
            models.Index(fields=['date_document']),
            models.Index(fields=['date_validite']),
            models.Index(fields=['-date_upload']),
        ]
        permissions = [
            ("view_confidential_documents", "Peut voir les documents confidentiels"),
            ("validate_document", "Peut valider un document"),
            ("sign_document", "Peut signer un document"),
            ("archive_document", "Peut archiver un document"),
        ]
    
    def __str__(self):
        return f"{self.reference} - {self.titre}"
    
    def save(self, *args, **kwargs):
        # Génération de la référence
        if not self.reference:
            year = timezone.now().year
            type_prefix = self.type_document[:4].upper()
            
            last_doc = Document.objects.filter(
                reference__startswith=f"DOC-{type_prefix}-{year}"
            ).order_by('-reference').first()
            
            if last_doc:
                last_num = int(last_doc.reference.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.reference = f"DOC-{type_prefix}-{year}-{new_num:06d}"
        
        # CORRECTION: S'assurer que le client est cohérent avec le dossier
        if self.dossier and not self.client:
            self.client = self.dossier.client
        
        # Métadonnées du fichier
        if self.fichier:
            self.extension = os.path.splitext(self.fichier.name)[1].lower().replace('.', '')
            if hasattr(self.fichier, 'size'):
                self.taille_fichier = self.fichier.size
        
        super().save(*args, **kwargs)
    
    @property
    def est_valide(self):
        """Vérifie si le document est encore valide"""
        if self.date_validite:
            return timezone.now().date() <= self.date_validite
        return True
    
    @property
    def taille_lisible(self):
        """Retourne la taille du fichier dans un format lisible"""
        if not self.taille_fichier:
            return "N/A"
        
        taille = self.taille_fichier
        for unit in ['o', 'Ko', 'Mo', 'Go']:
            if taille < 1024.0:
                return f"{taille:.1f} {unit}"
            taille /= 1024.0
        return f"{taille:.1f} To"
    
    @property
    def est_signe_completement(self):
        """Vérifie si tous les signataires ont signé"""
        if not self.necessite_signature:
            return None
        
        total_signataires = self.signataires.count()
        if total_signataires == 0:
            return False
        
        signatures_faites = self.signatures.filter(a_signe=True).count()
        return signatures_faites == total_signataires
    
    def enregistrer_consultation(self):
        """Enregistre une consultation du document"""
        self.derniere_consultation = timezone.now()
        self.nombre_consultations += 1
        self.save(update_fields=['derniere_consultation', 'nombre_consultations'])
    
    def creer_nouvelle_version(self, nouveau_fichier, user):
        """Crée une nouvelle version du document"""
        nouvelle_version = Document.objects.create(
            titre=self.titre,
            description=self.description,
            type_document=self.type_document,
            categorie=self.categorie,
            dossier=self.dossier,
            client=self.client,
            fichier=nouveau_fichier,
            numero_document=self.numero_document,
            date_document=timezone.now().date(),
            emetteur=self.emetteur,
            destinataire=self.destinataire,
            niveau_confidentialite=self.niveau_confidentialite,
            necessite_signature=self.necessite_signature,
            version=self.version + 1,
            document_parent=self,
            uploade_par=user,
            tags=self.tags
        )
        return nouvelle_version


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