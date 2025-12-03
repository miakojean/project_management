from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ClientCreateAPIView,
    ClientBulkCreateAPIView,
    ClientWithDossierCreateAPIView,
    ClientListAPIView,
    ClientSearchAPIView
)

from .view.affairs_views import (
    DossierCreateAPIView,
    DossierListCreateAPIView,
    DossierStatsAPIView,
    DossierDetailAPIView,
)

from .view.documents_views import(
    DocumentsAPIView
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

    # View to manage affairs 
    path('dossier/create/', DossierCreateAPIView.as_view(), name="create-affairs"),
    path('affairs', DossierListCreateAPIView.as_view(), name="manage-affairs"),
    path('affairs/details/<int:pk>/', DossierDetailAPIView.as_view(), name='dossier-detail'),
    path('affairs/stats', DossierStatsAPIView.as_view(), name="affairs-stats"),

    # View to manage documents
    path('documents/',DocumentsAPIView.as_view(), name="documents" ),

    #Category
    path('category', CategoryView.as_view(), name="category-view")
]