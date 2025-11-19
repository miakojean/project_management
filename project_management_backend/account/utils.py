from django.core.mail import EmailMessage
from django.conf import settings
import uuid
from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string

def generate_password_reset_token(user):
    
    """Génère un token sécurisé et le sauvegarde en base"""

    token = uuid.uuid4()
    expires_at = timezone.now() + timedelta(hours=1)

    from .models import PasswordResetToken

    # Supprime les anciens token et crée le nouveau

    PasswordResetToken.objects.filter(user=user).delete()
    PasswordResetToken.objects.create(
        user=user,
        token=token,
        expires_at=expires_at
    )
    return token

def send_password_reset_email(user, reset_link):
    """Envoie un email avec token visile et boutton cliquable"""

    subject = "Réinitialisation de votre mot de passe"

    context = {
        'user': user,
        'reset_link': reset_link,
        'token': reset_link.split('/')[-1],
        'frontend_url': settings.FRONTEND_URL,
    }

    html_content = render_to_string('account/password_reset.html', context)

    email = EmailMessage(
        subject,
        html_content,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.content_subtype = "html"
    email.send()