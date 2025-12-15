from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ClientCreateAPIView,
    ClientBulkCreateAPIView,
    ClientWithDossierCreateAPIView,
    ClientListAPIView,
    ClientSearchAPIView
    , ClientMonthlyRegistrationStatsAPIView
)

from .view.affairs_views import (
    DossierCreateAPIView,
    DossierListCreateAPIView,
    DossierStatsAPIView,
    DossierDetailAPIView,
    # ============ AJOUT DES IMPORTS POUR COMMENTAIRES ============
    CommentaireListCreateAPIView,
    CommentaireDetailAPIView,
    ReponseListCreateAPIView,
    ReponseDetailAPIView,
    # =============================================================
)

from .view.documents_views import(
    DocumentsAPIView,
    DocumentDownloadAPIView,
    MultipleDocumentDownloadAPIView,
    DocumentPreviewAPIView,
    DocumentDirectDownloadAPIView,
)

from .view.categories_views import(CategoryView)

router = DefaultRouter()
router.register(r'dossiers', DossierCreateAPIView, basename='dossier')

urlpatterns = [
    # Listes des clients
    path('clients/', ClientListAPIView.as_view(), name="clients-list"),
    path('clients/search/', ClientSearchAPIView.as_view(), name='client-search'),

    # Ajouter des clients
    path('clients/ajouter/', ClientCreateAPIView.as_view(), name='client-create'),
    path('clients/ajouter-multiple/', ClientBulkCreateAPIView.as_view(), name='client-bulk-create'),
    path('clients/ajouter-avec-dossier/', ClientWithDossierCreateAPIView.as_view(), name='client-with-dossier-create'),
    # Statistiques clients
    path('clients/stats/monthly/', ClientMonthlyRegistrationStatsAPIView.as_view(), name='client-monthly-stats'),

    # View to manage affairs 
    path('dossier/create/', DossierCreateAPIView.as_view(), name="create-affairs"),
    path('affairs', DossierListCreateAPIView.as_view(), name="manage-affairs"),
    path('affairs/details/<int:pk>/', DossierDetailAPIView.as_view(), name='dossier-detail'),
    path('affairs/stats', DossierStatsAPIView.as_view(), name="affairs-stats"),

    # ============ ENDPOINTS POUR COMMENTAIRES ============
    
    # Commentaires d'un dossier
    path('affairs/<int:dossier_id>/commentaires/', 
         CommentaireListCreateAPIView.as_view(), 
         name='dossier-commentaires'),
    
    # Gestion d'un commentaire spécifique
    path('commentaires/<int:commentaire_id>/', 
         CommentaireDetailAPIView.as_view(), 
         name='commentaire-detail'),
    
    # Réponses d'un commentaire
    path('commentaires/<int:commentaire_id>/reponses/', 
         ReponseListCreateAPIView.as_view(), 
         name='commentaire-reponses'),
    
    # Gestion d'une réponse spécifique
    path('reponses/<int:reponse_id>/', 
         ReponseDetailAPIView.as_view(), 
         name='reponse-detail'),
    
    # =====================================================

    # View to manage documents
    path('documents/',DocumentsAPIView.as_view(), name="documents" ),
    path('documents/download/', DocumentDownloadAPIView.as_view(), name='documents-download-list'),
    path('documents/download/<int:document_id>/', DocumentDownloadAPIView.as_view(), name='document-download'),
    path('documents/<int:document_id>/download/', DocumentDirectDownloadAPIView.as_view(), name='document-direct-download'),
    path('documents/<int:pk>/', DocumentsAPIView.as_view(), name="document-detail"),
    # Téléchargement multiple
    path('documents/download-multiple/', MultipleDocumentDownloadAPIView.as_view(), name='documents-download-multiple'),
    
    # Prévisualisation
    path('documents/preview/<int:document_id>/', DocumentPreviewAPIView.as_view(), name='document-preview'),

    #Category
    path('category', CategoryView.as_view(), name="category-view"),
]