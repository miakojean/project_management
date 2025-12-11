# test_dossier.py - VERSION CORRIGÉE
from django.test import TestCase, override_settings
from django.utils import timezone
from django.db import IntegrityError
from decimal import Decimal
from unittest.mock import patch, PropertyMock, MagicMock
import os
import shutil 
from datetime import timedelta 
from django.conf import settings

from manager.models import Dossier, EtapeDossier, Client, CategorieDocument 
from account.models import Utilisateur

# ====================================================================
# Configuration de l'environnement de test
# ====================================================================
TEST_MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'test_media')

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)  # ✅ CORRECTION
class DossierModelTest(TestCase):
    """
    Tests pour les modèles Dossier et EtapeDossier.
    """
    
    @classmethod
    def setUpTestData(cls):
        """Configuration des données de test avant l'exécution de toutes les méthodes."""
        
        # 1. Utilisateurs
        cls.collaborateur_1 = Utilisateur.objects.create_user(
            username='collab1', 
            email='c1@test.com', 
            password='password'
        )
        cls.cree_par_user = Utilisateur.objects.create_user(
            username='creator', 
            email='cr@test.com', 
            password='password'
        )

        # 2. Client
        with patch.object(Client, 'creer_nom_dossier_securise', return_value='DUPONT_JEAN_PP20250001'):
            cls.client_pp = Client.objects.create(
                type_client='PERSONNE_PHYSIQUE',
                nom="DUPONT",
                prenoms="Jean",
                telephone_1='0101010101',
                reference_client='PP20250001'
            )
        
        # 3. Catégories pour le scoring
        cls.cat_base = CategorieDocument.objects.create(
            nom="Base", code="BASE", poids=10, est_obligatoire=False
        )
        cls.cat_faible = CategorieDocument.objects.create(
            nom="Faible", code="FAIBLE", poids=20, est_obligatoire=False
        )
        cls.cat_critique = CategorieDocument.objects.create(
            nom="Critique", code="CRIT", poids=50, est_obligatoire=True
        )
        cls.cat_max = CategorieDocument.objects.create(
            nom="Max", code="MAX", poids=30, est_obligatoire=True
        )
        
    def setUp(self):
        """Configuration pour chaque test."""
        self.dossier_base = Dossier.objects.create(
            titre="Constitution SA Test",
            type_dossier='CONSTITUTION',
            client=self.client_pp,
            honoraires_prevus=Decimal('500000'),
            acompte_recu=Decimal('100000'),
            cree_par=self.cree_par_user
        )
        
        self.dossier_chemin_absolu = os.path.join(
            TEST_MEDIA_ROOT, 
            'dossiers_clients', 
            'DUPONT_JEAN_PP20250001'
        )
        
    def tearDown(self):
        """Nettoyage après chaque test."""
        if os.path.exists(TEST_MEDIA_ROOT):
            shutil.rmtree(TEST_MEDIA_ROOT)
        
    ## 1. Tests de la logique de save() et de la référence

    def test_dossier_creation_and_reference_generation(self):
        """Vérifie la création du dossier et la génération de la référence."""
        year = timezone.now().year
        self.assertTrue(self.dossier_base.reference_dossier.startswith(f"CONST-{year}-"))
        
        # ✅ CORRECTION : Vérifier avec TEST_MEDIA_ROOT
        expected_chemin = os.path.join(TEST_MEDIA_ROOT, 'dossiers_clients', 'DUPONT_JEAN_PP20250001')
        self.assertEqual(self.dossier_base.chemin_dossier, expected_chemin)
        self.assertTrue(os.path.exists(self.dossier_chemin_absolu))
        
    def test_reference_dossier_incrementation(self):
        """Vérifie que la référence est incrémentée pour le même type/année."""
        dossier_2 = Dossier.objects.create(
            titre="Deuxième Constitution SA",
            type_dossier='CONSTITUTION',
            client=self.client_pp,
            cree_par=self.cree_par_user
        )
        
        ref_num_1 = int(self.dossier_base.reference_dossier.split('-')[-1])
        ref_num_2 = int(dossier_2.reference_dossier.split('-')[-1])
        
        self.assertEqual(ref_num_2, ref_num_1 + 1)
        
    def test_reference_dossier_different_type(self):
        """Vérifie qu'un type différent utilise un préfixe différent."""
        dossier_contentieux = Dossier.objects.create(
            titre="Affaire Tribunal",
            type_dossier='CONTENTIEUX',
            client=self.client_pp,
            cree_par=self.cree_par_user
        )
        
        year = timezone.now().year
        self.assertTrue(dossier_contentieux.reference_dossier.startswith(f"CONT-{year}-"))

    def test_date_cloture_setting(self):
        """Vérifie que date_cloture est settée lors du changement de statut."""
        self.dossier_base.statut = 'CLOTURE'
        self.dossier_base.save()
        
        self.assertEqual(self.dossier_base.date_cloture, timezone.now().date())
        
        cloture_date = self.dossier_base.date_cloture
        self.dossier_base.statut = 'EN_COURS'
        self.dossier_base.save()
        self.assertEqual(self.dossier_base.date_cloture, cloture_date)

    def test_unique_together_constraint(self):
        """Vérifie l'unicité du couple (titre, client)."""
        with self.assertRaises(IntegrityError):
            Dossier.objects.create(
                titre="Constitution SA Test",
                type_dossier='MODIFICATION',
                client=self.client_pp,
                cree_par=self.cree_par_user
            )

    ## 2. Tests de la logique de Scoring et d'Avancement

    @patch('manager.models.dossier.Dossier.documents')
    def test_score_actuel_somme_poids(self, mock_documents):
        """✅ CORRECTION : Vérifie que score_actuel = SOMME des poids"""
        
        # Configuration des mocks pour simuler le comportement de .documents.filter(categorie=X).exists()
        def get_filter_side_effect(categories_presentes_ids):
            def filter_side_effect(categorie=None, **kwargs):
                mock_result = MagicMock()
                # exists() retourne True si la catégorie demandée fait partie des catégories présentes
                is_present = categorie.id in categories_presentes_ids
                mock_result.exists.return_value = is_present
                return mock_result
            return filter_side_effect
        
        # 1. Aucun document → score = 0
        mock_documents.filter.side_effect = get_filter_side_effect([])
        self.assertEqual(self.dossier_base.score_actuel, 0)
        
        # 2. Catégorie Base (10) uniquement
        mock_documents.filter.side_effect = get_filter_side_effect([self.cat_base.id])
        self.assertEqual(self.dossier_base.score_actuel, 10)
        
        # 3. Catégories Base (10) + Faible (20) = 30
        mock_documents.filter.side_effect = get_filter_side_effect([self.cat_base.id, self.cat_faible.id])
        self.assertEqual(self.dossier_base.score_actuel, 30)
        
        # 4. Toutes les catégories (10 + 20 + 50 + 30 = 110, cappé à 100)
        all_ids = [self.cat_base.id, self.cat_faible.id, self.cat_critique.id, self.cat_max.id]
        mock_documents.filter.side_effect = get_filter_side_effect(all_ids)
        self.assertEqual(self.dossier_base.score_actuel, 100)

    @patch('manager.models.dossier.Dossier.documents')
    def test_taux_avancement_pourcentage(self, mock_documents):
        """✅ CORRECTION : Vérifie le calcul du pourcentage"""
        
        # Score total = 10 + 20 + 50 + 30 = 110
        total_poids = 110.0
        
        # Configuration des mocks pour simuler le comportement de .documents.filter(categorie=X).exists()
        def get_filter_side_effect(categories_presentes_ids):
            def filter_side_effect(categorie=None, **kwargs):
                mock_result = MagicMock()
                mock_result.exists.return_value = (categorie.id in categories_presentes_ids)
                return mock_result
            return filter_side_effect

        # 1. Aucun document → 0%
        mock_documents.filter.side_effect = get_filter_side_effect([])
        self.assertEqual(self.dossier_base.taux_avancement, 0)
        
        # 2. Base (10) uniquement → 10/110 ≈ 9%
        mock_documents.filter.side_effect = get_filter_side_effect([self.cat_base.id])
        expected = int((10 / total_poids) * 100)
        self.assertEqual(self.dossier_base.taux_avancement, expected)
        
        # 3. Base (10) + Critique (50) = 60/110 ≈ 54%
        mock_documents.filter.side_effect = get_filter_side_effect([self.cat_base.id, self.cat_critique.id])
        expected = int((60 / total_poids) * 100)
        self.assertEqual(self.dossier_base.taux_avancement, expected)

    @patch.object(Dossier, 'taux_avancement', new_callable=PropertyMock)  # ✅ CORRECTION
    def test_mettre_a_jour_statut_par_score(self, mock_taux):
        """✅ CORRECTION : Vérifie la mise à jour du statut avec PropertyMock"""
        
        # 1. NOUVEAU (<= 10%)
        mock_taux.return_value = 5
        self.dossier_base.statut = 'NOUVEAU'
        self.dossier_base.mettre_a_jour_statut_par_score()
        self.assertEqual(self.dossier_base.statut, 'NOUVEAU')
        
        # 2. EN_COURS (11-40%)
        mock_taux.return_value = 30
        self.dossier_base.mettre_a_jour_statut_par_score()
        self.assertEqual(self.dossier_base.statut, 'EN_COURS')
        
        # 3. EN_ATTENTE (41-70%)
        mock_taux.return_value = 55
        self.dossier_base.mettre_a_jour_statut_par_score()
        self.assertEqual(self.dossier_base.statut, 'EN_ATTENTE')
        
        # 4. EN_COURS à nouveau (71-99%)
        mock_taux.return_value = 80
        self.dossier_base.mettre_a_jour_statut_par_score()
        self.assertEqual(self.dossier_base.statut, 'EN_COURS')
        
        # 5. TERMINE (100%)
        mock_taux.return_value = 100
        self.dossier_base.mettre_a_jour_statut_par_score()
        self.assertEqual(self.dossier_base.statut, 'TERMINE')

    ## 3. Tests des propriétés utilitaires

    def test_solde_honoraires_property(self):
        """Vérifie le calcul du solde restant dû."""
        self.assertEqual(self.dossier_base.solde_honoraires, Decimal('500000.00'))
        
        self.dossier_base.honoraires_factures = Decimal('200000.00')
        self.assertEqual(self.dossier_base.solde_honoraires, Decimal('300000.00'))
        
    def test_solde_acompte_property(self):
        """Vérifie le calcul du solde de l'acompte."""
        self.assertEqual(self.dossier_base.solde_acompte, Decimal('100000.00'))
        
        self.dossier_base.honoraires_factures = Decimal('150000.00')
        self.assertEqual(self.dossier_base.solde_acompte, Decimal('-50000.00'))
        
    def test_get_duree_traitement(self):
        """Vérifie le calcul de la durée de traitement en jours."""
        date_ouverture_past = timezone.now().date() - timedelta(days=5)
        self.dossier_base.date_ouverture = date_ouverture_past
        
        # Sans date de clôture
        self.assertEqual(self.dossier_base.get_duree_traitement(), 5)
        
        # Avec date de clôture
        self.dossier_base.date_cloture = date_ouverture_past + timedelta(days=10)
        self.assertEqual(self.dossier_base.get_duree_traitement(), 10)

    def test_est_en_retard_property(self):
        """Vérifie le retard basé sur la date d'échéance."""
        self.assertFalse(self.dossier_base.est_en_retard)
        
        self.dossier_base.date_echeance = timezone.now().date() - timedelta(days=1)
        self.dossier_base.statut = 'EN_COURS'
        self.assertTrue(self.dossier_base.est_en_retard)
        
        self.dossier_base.statut = 'TERMINE'
        self.assertFalse(self.dossier_base.est_en_retard)
        
    @patch.object(Dossier, 'score_actuel', new_callable=PropertyMock)  # ✅ CORRECTION
    def test_est_en_retard_score_property(self, mock_score_actuel):
        """✅ CORRECTION : Vérifie le retard basé sur le score"""
        
        # Simuler un dossier ouvert il y a 40 jours
        self.dossier_base.date_ouverture = timezone.now().date() - timedelta(days=40)
        self.dossier_base.save()
        
        # Durée > 30 jours ET Score < 50
        mock_score_actuel.return_value = 40
        self.assertTrue(self.dossier_base.est_en_retard_score)
        
        # Durée > 30 jours MAIS Score >= 50
        mock_score_actuel.return_value = 55
        self.assertFalse(self.dossier_base.est_en_retard_score)

    def test_etape_dossier_creation(self):
        """Vérifie la création et l'association d'une étape."""
        etape = EtapeDossier.objects.create(
            dossier=self.dossier_base,
            nom="Dépôt des statuts",
            ordre=1,
            date_debut=timezone.now().date(),
            est_terminee=True
        )
        
        self.assertEqual(etape.dossier, self.dossier_base)
        self.assertTrue(etape.est_terminee)
        self.assertEqual(str(etape), f"{self.dossier_base.reference_dossier} - Dépôt des statuts")

    def test_etape_ordering(self):
        """Vérifie que les étapes sont ordonnées correctement."""
        EtapeDossier.objects.create(dossier=self.dossier_base, nom="Etape 2", ordre=2)
        EtapeDossier.objects.create(dossier=self.dossier_base, nom="Etape 1", ordre=1)
        
        etapes = self.dossier_base.etapes.all()
        
        self.assertEqual(etapes[0].nom, "Etape 1")
        self.assertEqual(etapes[1].nom, "Etape 2")