# test_account_models.py
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from account.models import Utilisateur, PasswordResetToken # REMPLACER account par le nom réel de l'application si différent
from unittest.mock import patch

class UtilisateurModelTest(TestCase):
    """
    Tests pour le modèle Utilisateur (hérite d'AbstractUser).
    """

    def setUp(self):
        """Crée un utilisateur de base pour les tests."""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '0700000001',
            'category_title': Utilisateur.Responsabilities.ASSISTANT,
        }
        self.user = Utilisateur.objects.create_user(**self.user_data)
        
    def test_utilisateur_creation(self):
        """Vérifie que l'utilisateur est créé correctement avec les champs de AbstractUser et personnalisés."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.phone_number, '0700000001')
        self.assertEqual(self.user.category_title, 'AS') # Code en DB
        self.assertIsInstance(self.user, Utilisateur)

    def test_default_category(self):
        """Vérifie que la catégorie par défaut est DIRECTEUR (DR)."""
        default_user = Utilisateur.objects.create_user(username='defaultuser', password='password')
        self.assertEqual(default_user.category_title, 'DR')

    def test_str_representation(self):
        """Vérifie la représentation __str__."""
        expected_str = f'Profile de {self.user.username}'
        self.assertEqual(str(self.user), expected_str)
        
    def test_responsabilities_choices(self):
        """Vérifie que les choix de catégorie sont corrects."""
        self.assertEqual(Utilisateur.Responsabilities.DIRECTEUR, 'DR')
        self.assertEqual(Utilisateur.Responsabilities.ASSISTANT, 'AS')
        self.assertEqual(Utilisateur.Responsabilities.AUTRE, 'AU')


class PasswordResetTokenModelTest(TestCase):
    """
    Tests pour le modèle PasswordResetToken.
    """

    def setUp(self):
        """Crée un utilisateur et un token pour les tests."""
        self.user = Utilisateur.objects.create_user(
            username='tokenuser', 
            email='token@example.com',
            password='securepassword'
        )
        # Création manuelle d'un token valide pour les tests de base
        self.valid_token = PasswordResetToken.objects.create(
            user=self.user,
            expires_at=timezone.now() + timedelta(hours=1)
        )

    def test_token_creation(self):
        """Vérifie que le token est créé correctement."""
        self.assertIsNotNone(self.valid_token.token)
        self.assertGreater(self.valid_token.expires_at, timezone.now())
        self.assertEqual(self.valid_token.user, self.user)
        self.assertIsNotNone(self.valid_token.created_at)

    def test_str_representation(self):
        """Vérifie la représentation __str__."""
        expected_str = f'Token for {self.user.username}'
        self.assertEqual(str(self.valid_token), expected_str)

    # Test de la méthode de classe `create_token`
    def test_create_token_utility(self):
        """Vérifie la création du token via la méthode utilitaire."""
        
        # Cas 1: Utilisation des heures par défaut (24h)
        token_24h = PasswordResetToken.create_token(self.user)
        expected_expiration_24h = timezone.now() + timedelta(hours=24)
        # Vérifie que l'expiration est proche de 24h
        self.assertAlmostEqual(token_24h.expires_at, expected_expiration_24h, delta=timedelta(seconds=1))

        # Cas 2: Utilisation d'une expiration personnalisée (1 heure)
        token_1h = PasswordResetToken.create_token(self.user, expiration_hours=1)
        expected_expiration_1h = timezone.now() + timedelta(hours=1)
        # Vérifie que l'expiration est proche de 1h
        self.assertAlmostEqual(token_1h.expires_at, expected_expiration_1h, delta=timedelta(seconds=1))
        
        # Vérifie que les tokens sont uniques
        self.assertNotEqual(token_24h.token, token_1h.token)

    # Test de la méthode d'instance `is_valid`
    def test_is_valid_method_valid_token(self):
        """Vérifie que is_valid retourne True pour un token futur."""
        # Le token créé dans setUp est valide (expire dans 1 heure)
        self.assertTrue(self.valid_token.is_valid())

    @patch('django.utils.timezone.now')
    def test_is_valid_method_expired_token(self, mock_now):
        """Vérifie que is_valid retourne False pour un token expiré."""
        
        # Simuler que le temps actuel est après l'expiration du token
        # Le token expire à T+1h. Nous simulons que le temps est T+2h.
        expired_time = self.valid_token.expires_at + timedelta(hours=1)
        mock_now.return_value = expired_time
        
        self.assertFalse(self.valid_token.is_valid())

    @patch('django.utils.timezone.now')
    def test_is_valid_method_token_exactly_expired(self, mock_now):
        """Vérifie que is_valid retourne False si l'expiration est égale à l'heure actuelle."""
        
        # Simuler que le temps actuel est exactement l'heure d'expiration
        mock_now.return_value = self.valid_token.expires_at
        
        self.assertFalse(self.valid_token.is_valid()) # `expires_at > timezone.now()` doit être Faux ou Égal