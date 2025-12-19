from django.db import models
from .models import Notification, NotificationRecipient # Import de la table pivot
from account.models import Utilisateur # Votre modèle utilisateur
from django.contrib.contenttypes.models import ContentType
from typing import List, Optional, Union, Iterable
from django.db.models.query import QuerySet

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
    
    # --- Normalisation & robustesse pour 'recipients' ---
    # Accepts: None, a single Utilisateur, a QuerySet, a list of Utilisateur or pks
    norm_recipients: List[Utilisateur] = []

    # If consumers explicitly passed None or empty iterable -> notify all active except actor
    if recipients is None:
        qs = Utilisateur.objects.filter(is_active=True)
        if actor is not None:
            qs = qs.exclude(pk=actor.pk)
        norm_recipients = list(qs)

    elif isinstance(recipients, QuerySet):
        norm_recipients = list(recipients)

    elif isinstance(recipients, Iterable) and not isinstance(recipients, (str, bytes)):
        # Iterable (list/tuple/set) of users or pks
        for r in recipients:
            if r is None:
                continue
            if isinstance(r, Utilisateur):
                norm_recipients.append(r)
            elif isinstance(r, int):
                try:
                    u = Utilisateur.objects.get(pk=r)
                    norm_recipients.append(u)
                except Utilisateur.DoesNotExist:
                    continue
            else:
                # ignore unknown types
                continue

        # If the passed iterable was empty, default to all active users except actor
        if len(norm_recipients) == 0:
            qs = Utilisateur.objects.filter(is_active=True)
            if actor is not None:
                qs = qs.exclude(pk=actor.pk)
            norm_recipients = list(qs)

    else:
        # single value (maybe a user instance or pk)
        if isinstance(recipients, Utilisateur):
            norm_recipients = [recipients]
        elif isinstance(recipients, int):
            try:
                norm_recipients = [Utilisateur.objects.get(pk=recipients)]
            except Utilisateur.DoesNotExist:
                norm_recipients = []
        else:
            # unknown type => nothing to notify
            norm_recipients = []

    # Ensure actor is excluded from recipients list if present
    if actor is not None:
        norm_recipients = [u for u in norm_recipients if u.pk != actor.pk]

    if not norm_recipients:
        return []

    recipients = norm_recipients

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