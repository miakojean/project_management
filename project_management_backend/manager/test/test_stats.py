from django.test import TestCase
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import datetime

from account.models import Utilisateur
from manager.models import Client


class ClientMonthlyStatsAPITest(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.user = Utilisateur.objects.create_user(username='testuser', password='pass')
        self.client_api.force_authenticate(user=self.user)

        # Create clients across multiple months
        dates = [
            datetime(2025, 1, 15, 10, 0),
            datetime(2025, 2, 1, 9, 0),
            datetime(2025, 2, 5, 12, 0),
            datetime(2025, 2, 20, 18, 0),
            datetime(2025, 3, 3, 14, 0),
        ]

        for d in dates:
            c = Client.objects.create(
                type_client='PERSONNE_PHYSIQUE',
                nom='Test',
                prenoms='User',
                telephone_1='+22501234567',
                charge_de_clientele=self.user
            )
            # override date_creation
            Client.objects.filter(pk=c.pk).update(date_creation=timezone.make_aware(d))

    def test_monthly_stats(self):
        resp = self.client_api.get('/manager/clients/stats/monthly/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data.get('success'))
        labels = data.get('labels')
        counts = data.get('data')

        # Expect months: 2025-01 (1), 2025-02 (3), 2025-03 (1)
        self.assertIn('2025-01', labels)
        self.assertIn('2025-02', labels)
        self.assertIn('2025-03', labels)

        # Map labels to counts
        label_counts = dict(zip(labels, counts))
        self.assertEqual(label_counts.get('2025-01'), 1)
        self.assertEqual(label_counts.get('2025-02'), 3)
        self.assertEqual(label_counts.get('2025-03'), 1)
