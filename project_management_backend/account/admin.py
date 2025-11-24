# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        # Si le mot de passe est en texte brut, le hacher
        if obj.password and not obj.password.startswith('pbkdf2_sha256$'):
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)