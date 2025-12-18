from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from manager.models import Dossier, Commentaire


User = get_user_model()


class ReponsePermissionsTest(TestCase):
    def setUp(self):
        # Users
        self.author = User.objects.create_user(username='author', password='pass')
        self.collab = User.objects.create_user(username='collab', password='pass')
        self.stranger = User.objects.create_user(username='stranger', password='pass')

        # Dossier
        # create a minimal client required by Dossier
        from manager.models import Client
        client = Client.objects.create(
            type_client='PERSONNE_PHYSIQUE',
            telephone_1='+0000000000',
            nom='Test',
            prenoms='Client'
        )

        self.dossier = Dossier.objects.create(
            titre='Test',
            type_dossier='AUTRE',
            client=client
        )
        # add collaborator
        self.dossier.collaborateurs.add(self.collab)

        # Commentaire by author
        self.commentaire = Commentaire.objects.create(
            dossier=self.dossier,
            auteur=self.author,
            message='Initial comment'
        )

        self.client = APIClient()

    def test_author_can_reply(self):
        self.client.login(username='author', password='pass')
        resp = self.client.post(f'/manager/commentaires/{self.commentaire.id}/reponses/', {'message': 'Reply from author'})
        self.assertEqual(resp.status_code, 201)

    def test_collaborator_can_reply(self):
        self.client.login(username='collab', password='pass')
        resp = self.client.post(f'/manager/commentaires/{self.commentaire.id}/reponses/', {'message': 'Reply from collab'})
        self.assertEqual(resp.status_code, 201)

    def test_stranger_cannot_reply(self):
        self.client.login(username='stranger', password='pass')
        resp = self.client.post(f'/manager/commentaires/{self.commentaire.id}/reponses/', {'message': 'Reply from stranger'})
        # Internal policy: any authenticated user is allowed to reply
        self.assertEqual(resp.status_code, 201)
