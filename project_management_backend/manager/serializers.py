# serializers.py

from .models import (
    Client, 
    Dossier, 
    CategorieDocument, 
    Document, 
    SignatureDocument,
    HistoriqueDocument, 
    EtapeDossier 
)
from rest_framework import serializers
from account.models import Utilisateur
from django.utils import timezone
from django.db import models



class ClientSerializer(serializers.ModelSerializer):
    # Champs calculés en lecture seule
    nom_complet = serializers.ReadOnlyField()
    
    # Relations
    charge_de_clientele = serializers.PrimaryKeyRelatedField(
        queryset=Utilisateur.objects.all(),
        required=False,
        allow_null=True
    )
    
    # CORRECTION: Gérer date_premier_contact correctement
    date_creation = serializers.DateTimeField(read_only=True)
    date_modification = serializers.DateTimeField(read_only=True)
    date_premier_contact = serializers.DateField(
        required=False,
        allow_null=True,
        default=timezone.now().date()  # Date par défaut (pas datetime)
    )
    
    class Meta:
        model = Client
        fields = [
            'id',
            # Informations générales
            'type_client', 'statut', 'reference_client',
            
            # Personne Physique
            'nom', 'prenoms', 'date_naissance', 'lieu_naissance',
            
            # Personne Morale
            'raison_sociale', 'forme_juridique', 'numero_rccm',
            'numero_cc', 'capital_social',
            
            # Coordonnées
            'adresse', 'ville', 'commune', 'telephone_1',
            'telephone_2', 'email',
            
            # Informations juridiques complémentaires 
            'representant_legal_nom', 'representant_legal_fonction',
            
            # Gestion administrative
            'date_creation', 'date_modification', 'date_premier_contact',
            'notes',
            
            # Relations
            'charge_de_clientele',
            
            # Champs calculés
            'nom_complet'
        ]
        read_only_fields = ['reference_client', 'date_creation', 'date_modification']

    def to_internal_value(self, data):
        """
        CORRECTION: Convertir les datetime en date avant validation
        """
        # Copier les données pour ne pas modifier l'original
        data = data.copy() if hasattr(data, 'copy') else dict(data)
        
        # Gérer date_premier_contact
        if 'date_premier_contact' in data and data['date_premier_contact']:
            date_str = str(data['date_premier_contact'])
            # Si c'est un datetime (contient 'T'), extraire seulement la date
            if 'T' in date_str:
                data['date_premier_contact'] = date_str.split('T')[0]
        
        # Gérer date_naissance
        if 'date_naissance' in data and data['date_naissance']:
            date_str = str(data['date_naissance'])
            if 'T' in date_str:
                data['date_naissance'] = date_str.split('T')[0]
        
        return super().to_internal_value(data)
    
    def validate(self, data):
        """
        Renforce la validation :
        1. Champs obligatoires selon le type_client.
        2. Unicité des identifiants (Email, Téléphone 1).
        3. Unicité du client (combinaison PP ou Raison Sociale/RCCM PM).
        """
        # 1. Validation conditionnelle des champs obligatoires (cohérence)
        type_client = data.get('type_client', self.instance.type_client if self.instance else None)

        if type_client == 'PERSONNE_PHYSIQUE':
            if not data.get('nom'):
                raise serializers.ValidationError({'nom': 'Le nom est obligatoire pour une personne physique.'})
            if not data.get('prenoms'):
                raise serializers.ValidationError({'prenoms': 'Le ou les prénoms sont obligatoires pour une personne physique.'})
        
        elif type_client == 'PERSONNE_MORALE':
            if not data.get('raison_sociale'):
                raise serializers.ValidationError({'raison_sociale': 'La raison sociale est obligatoire pour une personne morale.'})

        # 2. Vérification d'unicité pour l'email et le téléphone
        q_filters = models.Q()
        instance_pk = self.instance.pk if self.instance else None

        if data.get('email') and data['email']:
            q_filters |= models.Q(email=data['email'])

        if data.get('telephone_1') and data['telephone_1']:
            q_filters |= models.Q(telephone_1=data['telephone_1'])

        if q_filters:
            if instance_pk:
                if Client.objects.filter(q_filters).exclude(pk=instance_pk).exists():
                    raise serializers.ValidationError("Un client avec cet email ou ce téléphone 1 existe déjà.")
            else:
                if Client.objects.filter(q_filters).exists():
                    raise serializers.ValidationError("Un client avec cet email ou ce téléphone 1 existe déjà.")

        # 3. Vérification d'unicité par type de client (Anti-duplication)
        if type_client == 'PERSONNE_PHYSIQUE':
            nom = data.get('nom', self.instance.nom if self.instance else None)
            prenoms = data.get('prenoms', self.instance.prenoms if self.instance else None)
            date_naissance = data.get('date_naissance', self.instance.date_naissance if self.instance else None)
            
            # Vérifie la combinaison nom/prenoms/date_naissance si ces champs sont définis
            if nom and prenoms and date_naissance:
                dupe_check = Client.objects.filter(
                    type_client='PERSONNE_PHYSIQUE',
                    nom=nom,
                    prenoms=prenoms,
                    date_naissance=date_naissance
                )
                if instance_pk:
                    dupe_check = dupe_check.exclude(pk=instance_pk)
                
                if dupe_check.exists():
                    raise serializers.ValidationError({
                        'non_field_errors': "Un client Personne Physique avec ce Nom, Prénom(s) et Date de naissance existe déjà."
                    })
            
        elif type_client == 'PERSONNE_MORALE':
            raison_sociale = data.get('raison_sociale', self.instance.raison_sociale if self.instance else None)
            numero_rccm = data.get('numero_rccm', self.instance.numero_rccm if self.instance else None)
            numero_cc = data.get('numero_cc', self.instance.numero_cc if self.instance else None)
            
            dupe_check = Client.objects.filter(type_client='PERSONNE_MORALE')
            
            # Utilise au moins un identifiant unique PM
            pm_q_filters = models.Q()
            if raison_sociale:
                pm_q_filters |= models.Q(raison_sociale__iexact=raison_sociale) # Case-insensitive
            if numero_rccm:
                pm_q_filters |= models.Q(numero_rccm__iexact=numero_rccm)
            if numero_cc:
                pm_q_filters |= models.Q(numero_cc__iexact=numero_cc)
            
            if pm_q_filters:
                dupe_check = dupe_check.filter(pm_q_filters)
                if instance_pk:
                    dupe_check = dupe_check.exclude(pk=instance_pk)

                if dupe_check.exists():
                    raise serializers.ValidationError({
                        'non_field_errors': "Un client Personne Morale avec cette Raison Sociale, ce Numéro RCCM ou ce Numéro CC existe déjà."
                    })

        return super().validate(data)


# Serializer pour la création rapide de client
class ClientCreateSerializer(serializers.ModelSerializer):
    # CORRECTION: Définir explicitement date_premier_contact
    date_premier_contact = serializers.DateField(
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Client
        fields = [
            'type_client', 'nom', 'prenoms', 'raison_sociale',
            'telephone_1', 'email', 'charge_de_clientele', 'date_premier_contact'
        ]
    
    def to_internal_value(self, data):
        """
        CORRECTION: Convertir les datetime en date avant validation
        """
        data = data.copy() if hasattr(data, 'copy') else dict(data)
        
        # Gérer date_premier_contact
        if 'date_premier_contact' in data and data['date_premier_contact']:
            date_str = str(data['date_premier_contact'])
            if 'T' in date_str:
                data['date_premier_contact'] = date_str.split('T')[0]
        
        return super().to_internal_value(data)
        
    def validate(self, data):
        type_client = data.get('type_client')
        
        if type_client == 'PERSONNE_PHYSIQUE' and not data.get('nom'):
            raise serializers.ValidationError({
                'nom': 'Le nom est obligatoire pour une personne physique.'
            })
        elif type_client == 'PERSONNE_MORALE' and not data.get('raison_sociale'):
            raise serializers.ValidationError({
                'raison_sociale': 'La raison sociale est obligatoire pour une personne morale.'
            })
        
        # Définir date_premier_contact si non fournie
        if 'date_premier_contact' not in data or not data['date_premier_contact']:
            data['date_premier_contact'] = timezone.now().date()
            
        return data


# Serializer léger pour les listes
class ClientListSerializer(serializers.ModelSerializer):
    nom_complet = serializers.ReadOnlyField()
    charge_de_clientele_nom = serializers.CharField(
        source='charge_de_clientele.get_full_name', 
        read_only=True
    )
    nombre_dossiers = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = [
            'id', 'reference_client', 'type_client', 'statut',
            'nom_complet', 'telephone_1', 'email', 'ville',
            'charge_de_clientele_nom', 'date_creation', 'nombre_dossiers'
        ]
    
    def get_nombre_dossiers(self, obj):
        return obj.dossiers.count()


# Serializer pour les statistiques client
class ClientStatsSerializer(serializers.ModelSerializer):
    nom_complet = serializers.ReadOnlyField()
    total_dossiers = serializers.SerializerMethodField()
    dossiers_actifs = serializers.SerializerMethodField()
    dossiers_termines = serializers.SerializerMethodField()
    dernier_dossier = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = [
            'id', 'reference_client', 'nom_complet', 'type_client', 'statut',
            'total_dossiers', 'dossiers_actifs', 'dossiers_termines', 'dernier_dossier'
        ]
    
    def get_total_dossiers(self, obj):
        return obj.dossiers.count()
    
    def get_dossiers_actifs(self, obj):
        return obj.dossiers.filter(statut__in=['NOUVEAU', 'EN_COURS', 'EN_ATTENTE']).count()
    
    def get_dossiers_termines(self, obj):
        return obj.dossiers.filter(statut__in=['TERMINE', 'CLOTURE']).count()
    
    def get_dernier_dossier(self, obj):
        dernier = obj.dossiers.order_by('-date_creation').first()
        if dernier:
            return {
                'reference': dernier.reference_dossier,
                'titre': dernier.titre,
                'statut': dernier.statut,
                'date_ouverture': dernier.date_ouverture.strftime('%Y-%m-%d') if dernier.date_ouverture else None
            }
        return None


class DossierSerializer(serializers.ModelSerializer):
    # On utilise le serializer client existant pour l'affichage (lecture seule)
    client_details = ClientListSerializer(source='client', read_only=True)
    
    # Pour l'assignation (écriture), on garde l'ID standard
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    
    # Champs calculés du modèle
    solde_honoraires = serializers.ReadOnlyField()
    est_en_retard = serializers.ReadOnlyField()
    taux_avancement = serializers.ReadOnlyField()
    
    # Gestion des collaborateurs (Many-to-Many)
    collaborateurs = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Utilisateur.objects.all(),
        required=False
    )

    # CORRECTION COMPLÈTE: Définir explicitement tous les champs de date
    date_ouverture = serializers.DateField(required=False, format='%Y-%m-%d')
    date_echeance = serializers.DateField(required=False, allow_null=True, format='%Y-%m-%d')
    date_cloture = serializers.DateField(read_only=True, format='%Y-%m-%d')

    class Meta:
        model = Dossier
        fields = [
            'id', 'reference_dossier', 'titre', 'type_dossier', 
            'description', 'client', 'client_details',
            'statut', 'priorite', 'collaborateurs',
            'date_ouverture', 'date_echeance', 'date_cloture',
            'honoraires_prevus', 'honoraires_factures', 'solde_honoraires',
            'numero_tribunal', 'juridiction', 'numero_rg',
            'observations', 'est_en_retard', 'taux_avancement',
            'cree_par', 'date_creation'
        ]
        read_only_fields =[
            'reference_dossier', 'chemin_dossier', 
            'solde_honoraires', 'est_en_retard', 'taux_avancement',
            'cree_par', 'date_creation', 'date_derniere_activite',
            'date_cloture'
        ]

    def to_internal_value(self, data):
        """
        CORRECTION ROBUSTE: Nettoyer les données de date avant validation
        """
        data = data.copy() if hasattr(data, 'copy') else dict(data)
        
        # Gérer les champs de date de manière robuste
        date_fields = ['date_ouverture', 'date_echeance']
        
        for field in date_fields:
            if field in data and data[field]:
                field_value = data[field]
                
                # Si c'est un string avec 'T' (format datetime ISO)
                if isinstance(field_value, str) and 'T' in field_value:
                    data[field] = field_value.split('T')[0]
                
                # Si c'est un datetime Python, convertir en date
                elif hasattr(field_value, 'strftime'):
                    # Si c'est un datetime, extraire la date
                    if hasattr(field_value, 'date'):
                        data[field] = field_value.date()
                    # Si c'est déjà une date, laisser tel quel
                    elif hasattr(field_value, 'year'):
                        data[field] = field_value
                
                # Si c'est None ou vide string, le supprimer pour utiliser les valeurs par défaut
                elif not field_value:
                    data.pop(field, None)

        return super().to_internal_value(data)

    def create(self, validated_data):
        """
        Surcharge de create pour gérer les valeurs par défaut
        """
        # Si date_ouverture n'est pas fournie, utiliser la valeur par défaut du modèle
        if 'date_ouverture' not in validated_data:
            validated_data['date_ouverture'] = timezone.now().date()
        
        # Gérer les collaborateurs si présents
        collaborateurs = validated_data.pop('collaborateurs', [])
        
        # Créer le dossier
        dossier = Dossier.objects.create(**validated_data)
        
        # Ajouter les collaborateurs
        if collaborateurs:
            dossier.collaborateurs.set(collaborateurs)
        
        return dossier

    def validate(self, data):
        """Validation personnalisée"""
        # Vérifier que la date d'échéance n'est pas antérieure à l'ouverture
        date_ouverture = data.get('date_ouverture')
        date_echeance = data.get('date_echeance')
        
        if date_echeance and date_ouverture:
            if date_echeance < date_ouverture:
                raise serializers.ValidationError({
                    "date_echeance": "La date d'échéance ne peut pas être antérieure à la date d'ouverture."
                })
            
        client = data.get('client') or getattr(self.instance, 'client', None)
        titre = data.get('titre') or getattr(self.instance, 'titre', None)

        if client and titre:
            qs = Dossier.objects.filter(client=client, titre__iexact=titre)
            # Exclure le dossier en cours de modification (update)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({
                    "titre": "Un dossier avec ce titre existe déjà pour ce client."
                })    

        return data

class DossierListSerializer(serializers.ModelSerializer):
    """Serializer allégé pour les listes (Tableaux de bord)"""
    client_nom = serializers.ReadOnlyField(source='client.nom_complet')
    date_creation_formatee = serializers.SerializerMethodField()
    date_echeance_formatee = serializers.SerializerMethodField()
    
    class Meta:
        model = Dossier
        fields = [
            'id', 'reference_dossier', 'titre', 'type_dossier', 
            'statut', 'priorite', 'client_nom', 'date_echeance', 
            'est_en_retard', 'taux_avancement', 'date_creation',
            'date_creation_formatee', 'date_echeance_formatee'  # Ajout des champs formatés
        ]

    def get_date_creation_formatee(self, obj):
        """Formate la date de création"""
        if obj.date_creation:
            # Format: "15 déc. 2023" ou selon votre préférence
            return obj.date_creation.strftime('%d %b %Y')
        return None

    def get_date_echeance_formatee(self, obj):
        """Formate la date d'échéance"""
        if obj.date_echeance:
            return obj.date_echeance.strftime('%d %b %Y')
        return None

# Serializer pour CategorieDocument
class CategorieDocumentSerializer(serializers.ModelSerializer):
    parent_nom = serializers.CharField(source='parent.nom', read_only=True)
    nombre_documents = serializers.SerializerMethodField()
    chemin_complet = serializers.SerializerMethodField()
    
    class Meta:
        model = CategorieDocument
        fields = [
            'id', 'nom', 'description', 'code', 'couleur', 'icone',
            'parent', 'parent_nom', 'ordre', 'est_actif',
            'date_creation', 'date_modification',
            'nombre_documents', 'chemin_complet'
        ]
        read_only_fields = ['date_creation', 'date_modification']
    
    def get_nombre_documents(self, obj):
        return obj.documents.count()
    
    def get_chemin_complet(self, obj):
        if obj.parent:
            return f"{obj.parent.nom} > {obj.nom}"
        return obj.nom

# Serializer pour la création de catégorie
class CategorieDocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieDocument
        fields = ['nom', 'description', 'code', 'couleur', 'icone', 'parent', 'ordre', 'est_actif']

# Serializer pour SignatureDocument
class SignatureDocumentSerializer(serializers.ModelSerializer):
    signataire_nom = serializers.CharField(source='signataire.get_full_name', read_only=True)
    signataire_email = serializers.CharField(source='signataire.email', read_only=True)
    document_titre = serializers.CharField(source='document.titre', read_only=True)
    document_reference = serializers.CharField(source='document.reference', read_only=True)
    
    class Meta:
        model = SignatureDocument
        fields = [
            'id', 'document', 'document_titre', 'document_reference',
            'signataire', 'signataire_nom', 'signataire_email',
            'ordre_signature', 'a_signe', 'date_signature',
            'commentaire', 'adresse_ip', 'empreinte_numerique',
            'date_creation'
        ]
        read_only_fields = ['date_creation', 'date_signature', 'adresse_ip', 'empreinte_numerique']

# Serializer pour la signature
class SignatureCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignatureDocument
        fields = ['document', 'signataire', 'ordre_signature', 'commentaire']

# Serializer pour HistoriqueDocument
class HistoriqueDocumentSerializer(serializers.ModelSerializer):
    utilisateur_nom = serializers.CharField(source='utilisateur.get_full_name', read_only=True)
    document_titre = serializers.CharField(source='document.titre', read_only=True)
    document_reference = serializers.CharField(source='document.reference', read_only=True)
    
    class Meta:
        model = HistoriqueDocument
        fields = [
            'id', 'document', 'document_titre', 'document_reference',
            'action', 'utilisateur', 'utilisateur_nom',
            'date_action', 'details', 'adresse_ip'
        ]
        read_only_fields = ['date_action']

# Serializer pour EtapeDossier
class EtapeDossierSerializer(serializers.ModelSerializer):
    dossier_reference = serializers.CharField(source='dossier.reference_dossier', read_only=True)
    dossier_titre = serializers.CharField(source='dossier.titre', read_only=True)
    duree_etape = serializers.SerializerMethodField()
    est_en_retard = serializers.SerializerMethodField()
    
    class Meta:
        model = EtapeDossier
        fields = [
            'id', 'dossier', 'dossier_reference', 'dossier_titre',
            'nom', 'description', 'ordre', 'date_debut', 'date_fin',
            'est_terminee', 'date_creation', 'date_modification',
            'duree_etape', 'est_en_retard'
        ]
        read_only_fields = ['date_creation', 'date_modification']
    
    def get_duree_etape(self, obj):
        if obj.date_debut and obj.date_fin:
            return (obj.date_fin - obj.date_debut).days
        return None
    
    def get_est_en_retard(self, obj):
        if obj.date_fin and not obj.est_terminee:
            from django.utils import timezone
            return timezone.now().date() > obj.date_fin
        return False

# Serializer pour la création d'étape
class EtapeDossierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtapeDossier
        fields = ['dossier', 'nom', 'description', 'ordre', 'date_debut', 'date_fin', 'est_terminee']

# Serializers pour Document
class DocumentListSerializer(serializers.ModelSerializer):
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    client_nom = serializers.CharField(source='client.nom_complet', read_only=True)
    dossier_reference = serializers.CharField(source='dossier.reference_dossier', read_only=True)
    dossier_titre = serializers.CharField(source='dossier.titre', read_only=True)
    uploade_par_nom = serializers.CharField(source='uploade_par.get_full_name', read_only=True)
    taille_lisible = serializers.ReadOnlyField()
    est_valide = serializers.ReadOnlyField()
    est_signe_completement = serializers.ReadOnlyField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'reference', 'titre', 'type_document',
            'categorie', 'categorie_nom', 'client', 'client_nom',
            'dossier', 'dossier_reference', 'dossier_titre',
            'statut', 'niveau_confidentialite', 'taille_lisible',
            'date_document', 'date_validite', 'est_valide',
            'est_original', 'est_certifie_conforme',
            'necessite_signature', 'est_signe_completement',
            'version', 'uploade_par', 'uploade_par_nom',
            'date_upload', 'est_archive'
        ]

class DocumentDetailSerializer(serializers.ModelSerializer):
    # Relations
    categorie_detail = CategorieDocumentSerializer(source='categorie', read_only=True)
    client_detail = serializers.SerializerMethodField()
    dossier_detail = serializers.SerializerMethodField()
    uploade_par_detail = serializers.SerializerMethodField()
    valide_par_detail = serializers.SerializerMethodField()
    
    # Champs calculés
    taille_lisible = serializers.ReadOnlyField()
    est_valide = serializers.ReadOnlyField()
    est_signe_completement = serializers.ReadOnlyField()
    
    # Signatures
    signatures = SignatureDocumentSerializer(many=True, read_only=True)
    signataires_list = serializers.SerializerMethodField()
    
    # Historique
    historique_recent = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'reference', 'titre', 'description', 'type_document',
            'categorie', 'categorie_detail', 'client', 'client_detail',
            'dossier', 'dossier_detail', 'fichier', 'taille_fichier', 
            'taille_lisible', 'extension', 'numero_document',
            'date_document', 'date_validite', 'est_valide',
            'emetteur', 'destinataire', 'statut', 
            'niveau_confidentialite', 'est_original', 
            'est_certifie_conforme', 'necessite_signature',
            'valide_par', 'valide_par_detail', 'date_validation',
            'version', 'document_parent', 'tags', 'mots_cles',
            'uploade_par', 'uploade_par_detail', 'date_upload',
            'date_modification', 'derniere_consultation',
            'nombre_consultations', 'notes_internes', 'est_archive',
            'date_archivage', 'est_signe_completement',
            'signatures', 'signataires_list', 'historique_recent'
        ]
        read_only_fields = [
            'reference', 'taille_fichier', 'extension', 'date_upload',
            'date_modification', 'nombre_consultations'
        ]
    
    def get_client_detail(self, obj):
        if obj.client:
            return {
                'id': obj.client.id,
                'reference': obj.client.reference_client,
                'nom_complet': obj.client.nom_complet,
                'type_client': obj.client.type_client
            }
        return None
    
    def get_dossier_detail(self, obj):
        if obj.dossier:
            return {
                'id': obj.dossier.id,
                'reference': obj.dossier.reference_dossier,
                'titre': obj.dossier.titre,
                'statut': obj.dossier.statut
            }
        return None
    
    def get_uploade_par_detail(self, obj):
        if obj.uploade_par:
            return {
                'id': obj.uploade_par.id,
                'nom_complet': obj.uploade_par.get_full_name(),
                'email': obj.uploade_par.email
            }
        return None
    
    def get_valide_par_detail(self, obj):
        if obj.valide_par:
            return {
                'id': obj.valide_par.id,
                'nom_complet': obj.valide_par.get_full_name(),
                'email': obj.valide_par.email
            }
        return None
    
    def get_signataires_list(self, obj):
        return list(obj.signataires.values('id', 'first_name', 'last_name', 'email'))
    
    def get_historique_recent(self, obj):
        historique = obj.historique.order_by('-date_action')[:5]
        return HistoriqueDocumentSerializer(historique, many=True).data

class DocumentCreateSerializer(serializers.ModelSerializer):
    files = serializers.ListField(               # ← NOUVEAU champ
        child=serializers.FileField(), 
        write_only=True, 
        required=True
    )

    class Meta:
        model = Document
        fields = [
            'titre', 'description', 'type_document', 'categorie',
            'dossier', 'client', 'files', 'numero_document',   # ← 'files' au lieu de 'fichier'
            'date_document', 'date_validite', 'emetteur', 'destinataire',
            'niveau_confidentialite', 'est_original', 
            'est_certifie_conforme', 'necessite_signature',
            'tags', 'mots_cles', 'notes_internes'
        ]
        extra_kwargs = {
            'fichier': {'required': False, 'read_only': True}  # ← on l'ignore en écriture
        }

    def create(self, validated_data):
        files = validated_data.pop('files')  # On extrait la liste des fichiers
        documents = []
        
        for file in files:
            data = validated_data.copy()
            data['fichier'] = file  # On remet un fichier à la fois
            data['uploade_par'] = self.context['request'].user
            
            document = super().create(data)  # Crée un Document par fichier
            
            # Historique (une fois par doc)
            HistoriqueDocument.objects.create(
                document=document,
                action='CREATION',
                utilisateur=self.context['request'].user,
                details=f"Création du document {document.titre}"
            )
            
            # Déplacement physique si dossier
            if document.dossier:
                document.dossier.ajouter_document_au_dossier(document)
            
            documents.append(document)
        
        return documents  # Retourne la liste (ou le premier si tu veux)

class DocumentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'titre', 'description', 'categorie', 'numero_document',
            'date_document', 'date_validite', 'emetteur', 'destinataire',
            'statut', 'niveau_confidentialite', 'est_original',
            'est_certifie_conforme', 'necessite_signature',
            'tags', 'mots_cles', 'notes_internes', 'est_archive'
        ]
    
    def update(self, instance, validated_data):
        # Créer une entrée d'historique avant modification
        HistoriqueDocument.objects.create(
            document=instance,
            action='MODIFICATION',
            utilisateur=self.context['request'].user,
            details=f"Modification du document {instance.titre}"
        )
        
        return super().update(instance, validated_data)

# Serializer pour le téléchargement de nouvelle version
class DocumentVersionCreateSerializer(serializers.ModelSerializer):
    document_parent = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all(), 
        required=True
    )
    
    class Meta:
        model = Document
        fields = ['titre', 'description', 'fichier', 'document_parent', 'notes_internes']
    
    def create(self, validated_data):
        document_parent = validated_data.pop('document_parent')
        
        # Créer la nouvelle version
        nouvelle_version = document_parent.creer_nouvelle_version(
            nouveau_fichier=validated_data['fichier'],
            user=self.context['request'].user
        )
        
        # Mettre à jour les autres champs
        nouvelle_version.titre = validated_data.get('titre', document_parent.titre)
        nouvelle_version.description = validated_data.get('description', document_parent.description)
        nouvelle_version.notes_internes = validated_data.get('notes_internes', '')
        nouvelle_version.save()
        
        return nouvelle_version

# Serializer pour les statistiques de documents
class DocumentStatsSerializer(serializers.Serializer):
    total_documents = serializers.IntegerField()
    documents_par_type = serializers.DictField()
    documents_par_statut = serializers.DictField()
    documents_signes = serializers.IntegerField()
    documents_expires = serializers.IntegerField()
    espace_utilise = serializers.CharField()
    evolution_mensuelle = serializers.DictField()