# test_client.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from datetime import date
from manager.models import Client
from account.models import Utilisateur # Utilisation du modèle Utilisateur fourni

class ClientModelTest(TestCase):
    """
    Tests pour le modèle Client, incluant l'utilisation de Utilisateur, la génération de référence,
    et la validation des coordonnées.
    """

    def setUp(self):
        """Configuration initiale pour les tests de Client."""
        # Création d'un Utilisateur réel pour la relation ForeignKey
        self.charge_clientele = Utilisateur.objects.create_user(
            username='c_client',
            email='charge@cabinet.com',
            password='Password123!',
            first_name='Mamadou',
            last_name='Kone',
            category_title=Utilisateur.Responsabilities.ASSISTANT
        )
        
        # Client Personne Physique (PP)
        self.client_pp = Client.objects.create(
            type_client='PERSONNE_PHYSIQUE',
            nom="DUPONT",
            prenoms="Jean-Michel",
            date_naissance=date(1985, 10, 20),
            telephone_1='+2250101010101',
            email='jean.dupont@example.com',
            statut='PROSPECT',
            charge_de_clientele=self.charge_clientele
        )
        
        # Client Personne Morale (PM)
        self.client_pm = Client.objects.create(
            type_client='PERSONNE_MORALE',
            raison_sociale="SOCIÉTÉ ANONYME TECH",
            numero_rccm="CI-ABC-12-34567",
            telephone_1='0707070707',
            capital_social=15000000.50,
            representant_legal_nom="Madame Boss",
            charge_de_clientele=self.charge_clientele
        )

    ## 1. Tests de création et de relations

    def test_client_pp_creation_and_relation(self):
        """Vérifie la création d'une PP et la relation ForeignKey."""
        self.assertEqual(self.client_pp.nom_complet, "DUPONT Jean-Michel")
        self.assertEqual(self.client_pp.charge_de_clientele, self.charge_clientele)
        self.assertEqual(self.client_pp.type_client, 'PERSONNE_PHYSIQUE')

    def test_client_pm_creation_and_fields(self):
        """Vérifie la création d'une PM et les champs spécifiques."""
        self.assertEqual(self.client_pm.nom_complet, "SOCIÉTÉ ANONYME TECH")
        self.assertEqual(self.client_pm.numero_rccm, "CI-ABC-12-34567")
        self.assertEqual(self.client_pm.capital_social, 15000000.50)

    def test_charge_de_clientele_on_delete(self):
        """Vérifie que la suppression de l'utilisateur met la FK à NULL (on_delete=models.SET_NULL)."""
        client_test = Client.objects.create(
            type_client='PERSONNE_PHYSIQUE',
            nom="TEST_DEL",
            prenoms="Test",
            telephone_1='0000000000',
            charge_de_clientele=self.charge_clientele
        )
        
        # Suppression de l'utilisateur
        self.charge_clientele.delete()
        
        # Recharge le client depuis la DB pour vérifier le champ
        client_test.refresh_from_db()
        self.assertIsNone(client_test.charge_de_clientele)

    ## 2. Tests de la méthode save() et référence client

    def test_reference_client_generation_pp(self):
        """Vérifie que la référence PP est générée correctement et incrémentée."""
        year = timezone.now().year
        
        # Vérifie la première référence PP
        ref_pp_1 = self.client_pp.reference_client
        self.assertTrue(ref_pp_1.startswith(f'PP{year}'))
        
        # Créer un second client PP
        client_pp_2 = Client.objects.create(
            type_client='PERSONNE_PHYSIQUE',
            nom="SMITH",
            prenoms="Jane",
            telephone_1='+2250101010102'
        )
        ref_pp_2 = client_pp_2.reference_client
        
        # Vérifie l'incrémentation (Ex: PP20250002)
        num_1 = int(ref_pp_1[-4:])
        num_2 = int(ref_pp_2[-4:])
        self.assertEqual(num_2, num_1 + 1)
        
    def test_reference_client_generation_pm(self):
        """Vérifie que la référence PM est générée correctement et incrémentée."""
        year = timezone.now().year
        
        # Vérifie la première référence PM
        ref_pm_1 = self.client_pm.reference_client
        self.assertTrue(ref_pm_1.startswith(f'PM{year}'))

        # Créer un second client PM
        client_pm_2 = Client.objects.create(
            type_client='PERSONNE_MORALE',
            raison_sociale="AUTRE SOCIETE",
            telephone_1='0707070708'
        )
        ref_pm_2 = client_pm_2.reference_client
        
        # Vérifie l'incrémentation (Ex: PM20250002)
        num_pm_1 = int(ref_pm_1[-4:])
        num_pm_2 = int(ref_pm_2[-4:])
        self.assertEqual(num_pm_2, num_pm_1 + 1)

    ## 3. Tests des propriétés et méthodes utilitaires

    def test_nom_complet_property(self):
        """Vérifie la propriété nom_complet pour les deux types."""
        self.assertEqual(self.client_pp.nom_complet, "DUPONT Jean-Michel")
        self.assertEqual(self.client_pm.nom_complet, "SOCIÉTÉ ANONYME TECH")

    def test_creer_nom_dossier_securise_pp(self):
        """Vérifie la création du nom de dossier pour une PP (nettoyage + référence)."""
        self.client_pp.nom = "DÜPONT"
        self.client_pp.prenoms = "Jean-François"
        self.client_pp.save()
        
        expected_name = f"DUPONT_JEAN_FRANCOIS_{self.client_pp.reference_client}"
        self.assertEqual(self.client_pp.creer_nom_dossier_securise(), expected_name)

    # test_client.py (Ligne 146 environ)

    def test_creer_nom_dossier_securise_pm(self):
        """Vérifie la création du nom de dossier pour une PM (nettoyage + référence)."""
        self.client_pm.raison_sociale = "Société d'Étude & Conseils S.A.R.L"
        self.client_pm.save()
        
        # CORRECTION ICI: Supprimer le '_' entre D et ETUDE
        expected_name = f"SOCIETE_DETUDE_CONSEILS_SARL_{self.client_pm.reference_client}"
        
        self.assertEqual(self.client_pm.creer_nom_dossier_securise(), expected_name)

    ## 4. Tests de validation (Téléphone)

    def test_telephone_validator_valid_formats(self):
        """Vérifie que les formats de numéro de téléphone valides sont acceptés."""
        
        valid_numbers = [
            '0707070707',       # 10 chiffres (local, courant en CI)
            '+2250707070707',   # Avec indicatif international
            '12345678',         # Min 8 chiffres
            '123456789012345'   # Max 15 chiffres
        ]
        
        for num in valid_numbers:
            self.client_pp.telephone_1 = num
            try:
                # full_clean déclenche les validateurs définis sur les champs
                self.client_pp.full_clean()
            except ValidationError:
                self.fail(f"La validation a échoué pour le numéro valide : {num}")
            
    def test_telephone_validator_invalid_formats(self):
        """Vérifie que les formats de numéro de téléphone invalides sont rejetés."""
        
        invalid_numbers = [
            '1234567',         # Trop court (moins de 8 chiffres)
            '07-07-07-07-07',  # Caractères non autorisés
            'ABCDEFGHIJ',      # Non numériques
            '+1234567890123456' # Trop long (plus de 17 caractères avec '+')
        ]
        
        for num in invalid_numbers:
            self.client_pp.telephone_1 = num
            with self.assertRaises(ValidationError, msg=f"Le numéro invalide {num} n'a pas levé d'erreur."):
                self.client_pp.full_clean()