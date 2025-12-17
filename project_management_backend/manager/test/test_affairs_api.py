from django.test import TestCase
from rest_framework.test import APIClient

from account.models import Utilisateur
from manager.models import Client, Dossier


class AffairsListFilterTest(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.user = Utilisateur.objects.create_user(username='tester', password='pass')
        self.client_api.force_authenticate(user=self.user)

        self.client_obj = Client.objects.create(
            type_client='PERSONNE_PHYSIQUE', nom='Test', prenoms='User', telephone_1='+22501234567', charge_de_clientele=self.user
        )

        # Create dossiers: one archived, two not archived
        Dossier.objects.create(titre='Dossier 1', type_dossier='CONTRAT', client=self.client_obj, est_archive=False)
        Dossier.objects.create(titre='Dossier 2', type_dossier='CONTRAT', client=self.client_obj, est_archive=True)
        Dossier.objects.create(titre='Dossier 3', type_dossier='CONTRAT', client=self.client_obj, est_archive=False)

    def test_get_non_archived_affairs(self):
        # Call without est_archive parameter -> default should exclude archived
        resp = self.client_api.get('/manager/affairs')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        dossiers = data.get('data', {}).get('dossiers', [])
        # should return only the two non-archived
        titles = [d['titre'] for d in dossiers]
        self.assertIn('Dossier 1', titles)
        self.assertIn('Dossier 3', titles)
        self.assertNotIn('Dossier 2', titles)

    def test_get_non_archived_affairs_by_client(self):
        # Call by client without est_archive -> default exclude archived
        resp = self.client_api.get(f'/manager/affairs?client_id={self.client_obj.id}')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        dossiers = data.get('data', {}).get('dossiers', [])
        titles = [d['titre'] for d in dossiers]
        self.assertIn('Dossier 1', titles)
        self.assertIn('Dossier 3', titles)
        self.assertNotIn('Dossier 2', titles)
