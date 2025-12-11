from django.test import TestCase, override_settings
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, MagicMock, PropertyMock
import os
import shutil 
from datetime import timedelta
from django.conf import settings
from datetime import timezone as dt_timezone
import unidecode
import re

# Assurez-vous d'importer les modèles nécessaires (même si certains ne sont que mockés)
from manager.models import Dossier, Client, CategorieDocument, Document
from account.models import Utilisateur

# ====================================================================
# Configuration de l'environnement de test et des constantes
# ====================================================================
TEST_MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'test_media')
TEST_FILE_CONTENT = b"Ceci est un fichier de test."

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class DocumentModelTest(TestCase):
    """
    Tests pour le modèle Document, y compris la logique de sauvegarde,
    les chemins de fichiers, les références, et les propriétés.
    """
    
    @classmethod
    def setUpTestData(cls):
        """Configuration des données de base nécessaires pour tous les tests."""
        
        # 1. Utilisateur
        cls.uploadeur = Utilisateur.objects.create_user(
            username='uploadeur', 
            email='up@test.com', 
            password='password'
        )
        cls.signataire_1 = Utilisateur.objects.create_user(
            username='sig1', 
            email='sig1@test.com', 
            password='password'
        )
        cls.signataire_2 = Utilisateur.objects.create_user(
            username='sig2', 
            email='sig2@test.com', 
            password='password'
        )
        cls.valideur = Utilisateur.objects.create_user(
            username='valid', 
            email='valid@test.com', 
            password='password'
        )

        # 2. Client (Mocking pour la création de dossier sécurisé)
        with patch.object(Client, 'creer_nom_dossier_securise', return_value='TEST_CLIENT_PP2025'):
            cls.client_test = Client.objects.create(
                type_client='PERSONNE_PHYSIQUE',
                nom="TEST",
                prenoms="Client",
                reference_client='PP2025'
            )
        
        # 3. Catégorie Document
        cls.cat_contrat = CategorieDocument.objects.create(
            nom="Contrat", code="CNTR", poids=20, est_obligatoire=True
        )
        cls.cat_annexe = CategorieDocument.objects.create(
            nom="Annexe", code="ANNX", poids=5, est_obligatoire=False
        )
        
        # 4. Dossier (Mocking pour éviter la complexité de save() complète)
        with patch.object(Dossier, '_generer_reference'), \
             patch('os.makedirs'):
            cls.dossier_test = Dossier.objects.create(
                titre="Dossier de Test",
                type_dossier='CONTRAT',
                client=cls.client_test,
                cree_par=cls.uploadeur,
                # Chemin nécessaire pour document_upload_path
                chemin_dossier=os.path.join(TEST_MEDIA_ROOT, 'dossiers_clients', 'TEST_CLIENT_PP2025')
            )
        
        # Créez le dossier physique réel pour les uploads de test
        os.makedirs(cls.dossier_test.chemin_dossier, exist_ok=True)


    def tearDown(self):
        """Nettoyage après chaque test : supprimer le répertoire MEDIA_ROOT de test."""
        if os.path.exists(TEST_MEDIA_ROOT):
            shutil.rmtree(TEST_MEDIA_ROOT)
        super().tearDown()
        
    def get_uploaded_file(self, filename='fichier_test.pdf'):
        """Utilitaire pour créer un fichier uploadé en mémoire."""
        return SimpleUploadedFile(filename, TEST_FILE_CONTENT, content_type='application/pdf')


    ## 1. Tests des fonctions utilitaires (hors modèle)
    
    @patch('manager.models.document.timezone.now')
    def creer_nom_fichier_securise(filename):
        name, ext = os.path.splitext(filename)

        # Enlever accents
        safe_name = unidecode(name)

        # Garder lettres, chiffres, espace, tiret, underscore
        safe_name = re.sub(r"[^A-Za-z0-9 _-]", "", safe_name)

        # Remplacer espaces et tirets multiples par underscore
        safe_name = re.sub(r"[ -]+", "_", safe_name)

        safe_name = safe_name.strip("_")

        timestamp = str(int(timezone.now().timestamp()))[-6:]

        return f"{safe_name}_{timestamp}{ext}"


    @patch('manager.models.document.timezone.now')
    def test_document_upload_path(self, mock_now):
        """Vérifie le chemin de destination de l'upload."""
        from manager.models.document import document_upload_path
        
        # Simuler un document SANS dossier associé
        mock_now.return_value = timezone.datetime(2025, 11, 15, tzinfo=dt_timezone.utc)
        document_sans_dossier = Document(dossier=None)
        
        path_sans = document_upload_path(document_sans_dossier, 'test.pdf')
        self.assertTrue(path_sans.startswith("documents/sans_dossier/2025/11/test_"))
        
        # Simuler un document AVEC dossier associé
        document_avec_dossier = Document(dossier=self.dossier_test)
        
        path_avec = document_upload_path(document_avec_dossier, 'contrat.pdf')
        # Le chemin doit être relatif à MEDIA_ROOT
        expected_start = os.path.join('dossiers_clients', 'TEST_CLIENT_PP2025', 'contrat_')
        self.assertTrue(path_avec.startswith(expected_start))


    ## 2. Tests de la logique de Sauvegarde (save)

    @patch.object(Dossier, 'mettre_a_jour_statut_par_score')
    def test_document_creation_and_save_logic(self, mock_update_score):
        """Vérifie la génération de référence, l'assignation client et la métadonnée."""
        uploaded_file = self.get_uploaded_file('mon_contrat.pdf')
        
        # Création du document
        document = Document.objects.create(
            titre="Contrat de prestation",
            categorie=self.cat_contrat,
            dossier=self.dossier_test,
            fichier=uploaded_file,
            uploade_par=self.uploadeur
        )
        
        document.refresh_from_db()
        
        # 1. Référence
        year = timezone.now().year
        self.assertTrue(document.reference.startswith(f"CNTR-{year}-"))
        
        # 2. Client auto-assigné
        self.assertEqual(document.client, self.client_test)
        
        # 3. Métadonnées du fichier
        self.assertEqual(document.extension, 'pdf')
        self.assertEqual(document.taille_fichier, len(TEST_FILE_CONTENT))
        
        # 4. Statut du dossier mis à jour
        mock_update_score.assert_called_once()
        
        # Vérifier que le fichier est bien enregistré au bon endroit (MEDIA_ROOT/dossier_client/...)
        self.assertTrue(os.path.exists(document.fichier.path))

    @patch.object(Dossier, 'mettre_a_jour_statut_par_score')
    def test_document_delete_updates_dossier_score(self, mock_update_score):
        """Vérifie que la suppression déclenche la mise à jour du score du dossier."""
        uploaded_file = self.get_uploaded_file()
        document = Document.objects.create(
            titre="À Supprimer",
            categorie=self.cat_annexe,
            dossier=self.dossier_test,
            fichier=uploaded_file,
            uploade_par=self.uploadeur
        )
        
        # Réinitialiser le mock après la création (save) pour tester le delete
        mock_update_score.reset_mock() 
        
        # Suppression
        document.delete()
        
        # Vérifier que la fonction de mise à jour du score a été appelée
        mock_update_score.assert_called_once()


    ## 3. Tests des Propriétés (@property)

    def test_est_valide_property(self):
        """Vérifie la propriété de validité basée sur date_validite."""
        
        # 1. Document sans date de validité (toujours True)
        doc_no_date = Document(date_validite=None)
        self.assertTrue(doc_no_date.est_valide)
        
        # 2. Document encore valide
        doc_valide = Document(date_validite=timezone.now().date() + timedelta(days=5))
        self.assertTrue(doc_valide.est_valide)
        
        # 3. Document périmé
        doc_perime = Document(date_validite=timezone.now().date() - timedelta(days=1))
        self.assertFalse(doc_perime.est_valide)
        
    def test_taille_lisible_property(self):
        """Vérifie que la taille du fichier est bien convertie en format lisible."""
        
        # 1. N/A (pas de taille)
        doc_na = Document(taille_fichier=None)
        self.assertEqual(doc_na.taille_lisible, "N/A")
        
        # 2. Octets
        doc_b = Document(taille_fichier=500)
        self.assertEqual(doc_b.taille_lisible, "500.0 o")
        
        # 3. Ko
        doc_ko = Document(taille_fichier=1024 * 5.5) # 5.5 Ko
        self.assertEqual(doc_ko.taille_lisible, "5.5 Ko")
        
        # 4. Mo
        doc_mo = Document(taille_fichier=1024**2 * 10.3) # 10.3 Mo
        self.assertEqual(doc_mo.taille_lisible, "10.3 Mo")
        
        # 5. Go (pour l'exemple)
        doc_go = Document(taille_fichier=1024**3 * 2.1) # 2.1 Go
        self.assertEqual(doc_go.taille_lisible, "2.1 Go")

    # Mocker le modèle SignatureDocument pour simuler les signatures
    @patch('manager.models.document.Document.signataires')
    @patch('manager.models.document.Document.signatures') 
    def test_est_signe_completement_property(self, mock_signatures, mock_signataires):
        """Vérifie l'état de la signature du document."""
        
        # 1. Ne nécessite pas de signature → None
        doc_no_sig = Document(necessite_signature=False)
        self.assertIsNone(doc_no_sig.est_signe_completement)
        
        # Configuration des mocks pour les tests suivants (necessite_signature=True)
        doc_sig_req = Document(necessite_signature=True)
        
        # 2. Nécessite signature, mais pas de signataires → False
        mock_signataires.count.return_value = 0
        self.assertFalse(doc_sig_req.est_signe_completement)
        
        # 3. Un signataire (total=1) / Zéro signature (faites=0) → False
        mock_signataires.count.return_value = 1
        mock_signatures.filter.return_value.count.return_value = 0
        self.assertFalse(doc_sig_req.est_signe_completement)
        
        # 4. Deux signataires (total=2) / Une signature (faites=1) → False
        mock_signataires.count.return_value = 2
        mock_signatures.filter.return_value.count.return_value = 1
        self.assertFalse(doc_sig_req.est_signe_completement)
        
        # 5. Deux signataires (total=2) / Deux signatures (faites=2) → True
        mock_signatures.filter.return_value.count.return_value = 2
        self.assertTrue(doc_sig_req.est_signe_completement)


    ## 4. Tests des Méthodes personnalisées

    @patch('manager.models.document.timezone.now')
    def test_enregistrer_consultation(self, mock_now):
        """Vérifie la mise à jour des compteurs de consultation."""
        now = timezone.datetime(2025, 12, 11, 10, 30, 0, tzinfo=dt_timezone.utc)
        mock_now.return_value = now
        
        document = Document.objects.create(
            titre="Consultable",
            categorie=self.cat_annexe,
            fichier=self.get_uploaded_file(),
            uploade_par=self.uploadeur
        )
        
        self.assertEqual(document.nombre_consultations, 0)
        self.assertIsNone(document.derniere_consultation)
        
        # 1ère consultation
        document.enregistrer_consultation()
        document.refresh_from_db()
        self.assertEqual(document.nombre_consultations, 1)
        self.assertEqual(document.derniere_consultation, now)
        
        # 2ème consultation (avec changement de temps)
        new_now = now + timedelta(hours=1)
        mock_now.return_value = new_now
        document.enregistrer_consultation()
        document.refresh_from_db()
        self.assertEqual(document.nombre_consultations, 2)
        self.assertEqual(document.derniere_consultation, new_now)

    @patch('manager.models.document.Document.save')
    @patch('manager.models.document.timezone.now')
    def creer_nouvelle_version(self, nouveau_fichier, user):
        """Crée une nouvelle version du document"""

        nouvelle_version = Document(
            titre=self.titre,
            description=self.description,
            categorie=self.categorie,  # IMPORTANT
            dossier=self.dossier,
            client=self.client,
            fichier=nouveau_fichier,
            numero_document=self.numero_document,
            date_document=timezone.now().date(),
            emetteur=self.emetteur,
            destinataire=self.destinataire,
            niveau_confidentialite=self.niveau_confidentialite,
            necessite_signature=self.necessite_signature,
            version=self.version + 1,
            document_parent=self,
            uploade_par=user,
            tags=self.tags
        )

        # ⚠ GENERER LA RÉFÉRENCE MÊME SI save() EST MOCKÉ
        nouvelle_version.generer_reference()

        # On force aussi extension/size
        if nouveau_fichier:
            nouvelle_version.extension = os.path.splitext(nouveau_fichier.name)[1].lower().lstrip('.')
            nouvelle_version.taille_fichier = getattr(nouveau_fichier, 'size', None)

        # save() sera mocké dans les tests → pas de problème
        nouvelle_version.save()

        return nouvelle_version
