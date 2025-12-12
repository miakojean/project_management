from django.db import models
from .models import Notification, NotificationRecipient # Import de la table pivot
from account.models import Utilisateur # Votre modèle utilisateur
from django.contrib.contenttypes.models import ContentType
from typing import List, Optional, Union 

def notify_users(
    recipients: Union[Utilisateur, List[Utilisateur]], 
    verb: str, 
    message: str, 
    content_object: models.Model, 
    actor: Optional[Utilisateur] = None, # L'acteur est facultatif et sert de déclencheur/excluant
) -> List[NotificationRecipient]:
    """
    Crée une notification unique et les relations NotificationRecipient pour les destinataires.
    
    Si 'recipients' est une liste vide, il tente de notifier TOUS les utilisateurs SAUF l'acteur.
    """
    
    # --- Étape 1 : Préparation de la liste des destinataires ---
    
    if not isinstance(recipients, list):
        recipients = [recipients]
        
    # LOGIQUE CLÉ : Si la liste des destinataires est vide, notifier TOUS sauf l'acteur
    if not recipients:
        # Récupère tous les utilisateurs actifs (à adapter selon votre modèle et logique)
        all_users = Utilisateur.objects.filter(is_active=True).exclude(pk=actor.pk)
        recipients = list(all_users)
        
    if not recipients:
        return []

    # --- Étape 2 : Création de l'enregistrement Notification Unique ---

    content_type_instance = ContentType.objects.get_for_model(content_object)
    
    # Créer l'objet Notification unique
    notification_instance = Notification.objects.create(
        actor=actor,
        verb=verb,
        message=message,
        content_type=content_type_instance,
        object_id=content_object.pk,
    )
    
    # --- Étape 3 : Création des enregistrements NotificationRecipient en masse ---

    recipients_to_create = []
    
    for recipient in recipients:
        recipients_to_create.append(
            NotificationRecipient(
                notification=notification_instance,
                recipient=recipient,
                is_read=False,
            )
        )
    
    # Insertion en masse des relations de destinataires
    created_recipients = NotificationRecipient.objects.bulk_create(recipients_to_create)
    
    return created_recipients