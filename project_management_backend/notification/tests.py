from django.test import TestCase
from account.models import Utilisateur
from .utils import notify_users
from manager.models.client import Client
from .models import Notification, NotificationRecipient


class NotifyUsersTests(TestCase):
	def setUp(self):
		# Create some users
		self.actor = Utilisateur.objects.create_user(username='actor', password='pass')
		self.u1 = Utilisateur.objects.create_user(username='u1', password='pass')
		self.u2 = Utilisateur.objects.create_user(username='u2', password='pass')

	def test_notify_with_none_recipients_notifies_all_except_actor(self):
		client = Client.objects.create(type_client='PERSONNE_PHYSIQUE', nom='Test', prenoms='User', telephone_1='+12345678')

		created = notify_users(None, 'CLIENT_AJOUTE', 'nouveau client', client, actor=self.actor)

		# Should create Notification + recipients for u1 and u2 (actor excluded)
		self.assertTrue(Notification.objects.exists())
		self.assertEqual(NotificationRecipient.objects.count(), 2)

	def test_notify_with_empty_list_uses_all_active(self):
		client = Client.objects.create(type_client='PERSONNE_PHYSIQUE', nom='Foo', prenoms='Bar', telephone_1='+12345678')

		created = notify_users([], 'CLIENT_AJOUTE', 'nouveau client', client, actor=self.actor)
		self.assertEqual(NotificationRecipient.objects.count(), 2)

	def test_notify_with_queryset_and_list_of_pks(self):
		client = Client.objects.create(type_client='PERSONNE_PHYSIQUE', nom='Q', prenoms='P', telephone_1='+12345678')

		qs = Utilisateur.objects.filter(username='u1')
		created = notify_users(qs, 'CLIENT_AJOUTE', 'msg', client, actor=None)
		self.assertEqual(NotificationRecipient.objects.count(), 1)

		Notification.objects.all().delete()
		NotificationRecipient.objects.all().delete()

		created = notify_users([self.u2.id], 'CLIENT_AJOUTE', 'msg', client, actor=None)
		self.assertEqual(NotificationRecipient.objects.count(), 1)

	def test_notify_excludes_actor_if_passed_in_list(self):
		client = Client.objects.create(type_client='PERSONNE_PHYSIQUE', nom='Ex', prenoms='Cl', telephone_1='+12345678')

		# pass list including actor and u1
		created = notify_users([self.actor, self.u1], 'CLIENT_AJOUTE', 'msg', client, actor=self.actor)
		# actor should be excluded -> only 1 recipient
		self.assertEqual(NotificationRecipient.objects.count(), 1)
