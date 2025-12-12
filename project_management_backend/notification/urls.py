from django.urls import path
from .views import (
    NotificationListAPIView, 
    NotificationDetailAPIView, 
)
urlpatterns = [
    path('notif-index', view=NotificationListAPIView.as_view(), name="notifications-list"),
    # CORRECTION : Ajout de <int:pk> pour l'ID de l'entrée pivot
    path('notification-details/<int:pk>/', view=NotificationDetailAPIView.as_view(), name="notification-details"),
]