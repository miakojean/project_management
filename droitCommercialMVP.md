# MVP - Application Web de Suivi de Dossiers Juridiques **Commercialux**

## 🎯 Objectif du MVP Spécialisé
Application dédiée au suivi des dossiers **commerciaux** avec focus sur les spécificités du droit des affaires.

## ⚡ Fonctionnalités Core Adaptées au Commercial

### 1. **Types d'Affaires Commerciales Prédéfinis**
```python
AFFAIRE_TYPES = [
    ('contrat_commercial', 'Contrat Commercial'),
    ('litige_fournisseur', 'Litige Fournisseur'),
    ('droit_societes', 'Droit des Sociétés'),
    ('concurrence', 'Droit de la Concurrence'),
    ('distribution', 'Droit de la Distribution'),
    ('faillite', 'Procédure Collective'),
    ('fusion_acquisition', 'Fusion & Acquisition'),
]
```

### 2. **Workflow Commercial Typique**
```
Nouveau → Négociation → Signature → Exécution → Litige → Clôture
```

### 3. **Champs Spécifiques aux Dossiers Commerciaux**
- **Parties concernées** : Société A vs Société B
- **Montant du contrat** 
- **Secteur d'activité**
- **Juridiction compétente** (Tribunal de Commerce, etc.)
- **Type de contrat** (distribution, partenariat, sous-traitance)

## 🔧 Modèles Django Adaptés

### Modèle Dossier Commercial
```python
class DossierCommercial(models.Model):
    TYPE_AFFAIRE_CHOICES = [
        ('contrat_commercial', 'Contrat Commercial'),
        ('litige_fournisseur', 'Litige Fournisseur'),
        ('droit_societes', 'Droit des Sociétés'),
        ('concurrence', 'Droit de la Concurrence'),
        ('distribution', 'Droit de la Distribution'),
        ('faillite', 'Procédure Collective'),
        ('fusion_acquisition', 'Fusion & Acquisition'),
    ]
    
    STATUT_CHOICES = [
        ('nouveau', 'Nouveau'),
        ('negociation', 'En Négociation'),
        ('signature', 'En cours de Signature'),
        ('execution', 'En Exécution'),
        ('litige', 'En Litige'),
        ('cloture', 'Clôturé'),
    ]

    reference = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey('Client', on_delete=models.PROTECT)
    avocat_responsable = models.ForeignKey(User, on_delete=models.PROTECT)
    
    # Spécificités commerciales
    type_affaire = models.CharField(max_length=50, choices=TYPE_AFFAIRE_CHOICES)
    partie_adverse = models.CharField(max_length=200, blank=True)
    avocat_adverse = models.CharField(max_length=200, blank=True)
    montant_contrat = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    juridiction = models.CharField(max_length=100, blank=True)
    
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='nouveau')
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
```

### Modèle Client Commercial
```python
class ClientCommercial(models.Model):
    FORME_JURIDIQUE_CHOICES = [
        ('sas', 'SAS'),
        ('sarl', 'SARL'),
        ('sa', 'SA'),
        ('ei', 'Entreprise Individuelle'),
        ('sci', 'SCI'),
    ]
    
    nom = models.CharField(max_length=200)
    forme_juridique = models.CharField(max_length=50, choices=FORME_JURIDIQUE_CHOICES)
    siret = models.CharField(max_length=14, blank=True)
    adresse = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    representant_legal = models.CharField(max_length=100, blank=True)
```

## 📊 Échéancier Commercial Critique

### Étapes Spécifiques aux Affaires Commerciales
```python
ETAPES_COMMERCIALES = {
    'contrat_commercial': [
        'Négociation initiale',
        'Rédaction contrat',
        'Revue juridique',
        'Signature',
        'Exécution',
        'Renouvellement'
    ],
    'litige_fournisseur': [
        'Mise en demeure',
        'Négociation amiable',
        'Assignation',
        'Audience',
        'Jugement',
        'Exécution jugement'
    ],
    'droit_societes': [
        'Audit juridique',
        'Rédaction statuts',
        'Assemblée générale',
        'Dépôt formalités',
        'Immatriculation'
    ]
}
```

## 🎨 Interface Utilisateur Commerciale

### Tableau de Bord Spécialisé
- **Widgets métier** : 
  - Contrats en négociation
  - Litiges actifs
  - Échéances de signature
  - Honoraires en attente

### Fiche Dossier Commercial
```
Dossier COMM-2024-001 - Société Client vs Société Adverse
───────────────────────────────────────────────────────
Type: Contrat Commercial    | Montant: 150 000 €
Statut: ⚖️ En Négociation   | Juridiction: Tribunal de Commerce

PARTIES:
├── Client: Société Client SAS (SIRET: 123456789)
├── Représentant: M. Dupont Jean
├── Adverse: Société Adverse SARL
└── Avocat Adverse: Maître Martin

ÉTAPES:
□ [En cours] Négociation contrat (échéance: 25/01/2024)
□ Rédaction contrat
□ Signature
□ Exécution

[+ Ajouter une action] [Modifier le statut]
```

## ⏱️ Planning MVP Commercial - 3 Semaines

### **Semaine 1** - Foundation Commerciale
- [ ] Setup projet avec modèles commerciaux
- [ ] CRUD Clients entreprises (SAS/SARL/SA)
- [ ] Types d'affaires commerciales prédéfinis
- [ ] Authentification équipe commerciale

### **Semaine 2** - Dossiers Commerciaux
- [ ] Formulaire création avec parties adverses
- [ ] Gestion montants contrats
- [ ] Workflows par type d'affaire
- [ ] Dashboard métier commercial

### **Semaine 3** - Finalisation
- [ ] Échéancier commercial
- [ ] Recherche par entreprise/montant
- [ ] Tests scénarios commerciaux
- [ ] Déploiement pilote

## ✅ Métriques de Suivi Commercial
- **Taux de conversion** négociation → signature
- **Délai moyen** de traitement par type d'affaire
- **Portefeuille** de contrats en cours
- **Litiges actifs** par secteur

---

**Focus MVP Commercial** : 
- ✅ Gestion des **sociétés clientes** 
- ✅ Suivi des **contrats et montants**
- ✅ Workflows **droit des affaires**
- ✅ Interface **spécialisée commerce**

Ce MVP répond directement aux besoins d'un cabinet spécialisé en droit commercial avec une terminologie et des processus adaptés.