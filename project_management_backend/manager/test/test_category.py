# test_category.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from manager.models import CategorieDocument# REMPLACER your_app_name par le nom réel de l'application
from django.db import IntegrityError, transaction

class CategorieDocumentModelTest(TestCase):
    """
    Tests pour le modèle CategorieDocument.
    """

    def setUp(self):
        """Configuration initiale pour les tests de CategorieDocument."""
        self.cat_parent = CategorieDocument.objects.create(
            nom="Documents Légaux",
            code="LEGAL",
            poids=50,
            est_obligatoire=True,
            delai_max=30
        )
        self.cat_enfant = CategorieDocument.objects.create(
            nom="Extrait de Naissance",
            code="NAISSANCE",
            parent=self.cat_parent,
            poids=20,
            ordre=2
        )

    ## Tests de base et hiérarchie

    def test_categorie_creation(self):
        """Vérifie que la création et les champs de base fonctionnent."""
        cat = CategorieDocument.objects.get(code="LEGAL")
        self.assertEqual(cat.nom, "Documents Légaux")
        self.assertEqual(cat.delai_max, 30)

    def test_categorie_enfant_str(self):
        """Vérifie la représentation __str__ pour une sous-catégorie."""
        cat = CategorieDocument.objects.get(code="NAISSANCE")
        self.assertEqual(str(cat), "Documents Légaux > Extrait de Naissance")
        self.assertEqual(cat.parent, self.cat_parent)
        self.assertEqual(self.cat_parent.sous_categories.count(), 1)


    def test_unique_constraint(self):
        """Vérifie l'unicité des champs 'nom' et 'code'."""
        
        # 1. Tester l'unicité du NOM
        # Exécuter dans un bloc atomique pour nettoyer la transaction en cas d'échec
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                CategorieDocument.objects.create(
                    nom="Documents Légaux",  # Nom existant
                    code="UNIQUE_1"
                )
                
        # 2. Tester l'unicité du CODE
        # Exécuter dans un bloc atomique séparé
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                CategorieDocument.objects.create(
                    nom="Nom Unique 2",
                    code="LEGAL"  # Code existant
                )
        
        # Vérifie qu'on peut toujours créer un objet valide après les erreurs
        CategorieDocument.objects.create(
            nom="Nouveau Nom Valide",
            code="CODE_V"
        )

    ## Tests des propriétés de Scoring

    def test_score_max_property(self):
        """Vérifie que la propriété score_max retourne la valeur du poids."""
        self.assertEqual(self.cat_parent.score_max, 50)

    def test_est_critique_property(self):
        """
        Vérifie que la propriété est_critique est VRAIE si est_obligatoire=VRAI
        ET poids >= 30.
        """
        # Cat Parent: obligatoire=True, poids=50 -> Critique
        self.assertTrue(self.cat_parent.est_critique) 
        
        # Cat Enfant: obligatoire=False (par défaut), poids=20 -> Non Critique
        self.assertFalse(self.cat_enfant.est_critique)

        # Cas obligatoire mais poids faible (Non Critique)
        cat_low_poids = CategorieDocument.objects.create(
            nom="Obligatoire Faible",
            code="OFAIBLE",
            poids=10,
            est_obligatoire=True
        )
        self.assertFalse(cat_low_poids.est_critique)
        
        # Cas obligatoire et pile au seuil (Critique)
        cat_seuil = CategorieDocument.objects.create(
            nom="Seuil Critique",
            code="SEUIL",
            poids=30,
            est_obligatoire=True
        )
        self.assertTrue(cat_seuil.est_critique)

    ## Tests des contraintes de validation (poids)

    def test_poids_validators(self):
        """Vérifie les contraintes MinValueValidator(1) et MaxValueValidator(100) pour 'poids'."""
        
        # Poids trop faible (0)
        cat_too_low = CategorieDocument(
            nom="Test Low", code="TLOW", poids=0
        )
        with self.assertRaises(ValidationError):
            # full_clean déclenche tous les validateurs de champs
            cat_too_low.full_clean()
            
        # Poids trop élevé (101)
        cat_too_high = CategorieDocument(
            nom="Test High", code="THIGH", poids=101
        )
        with self.assertRaises(ValidationError):
            cat_too_high.full_clean()