from django.contrib import admin
from .models import (
    Client, 
    Dossier, 
    CategorieDocument, 
    Document, 
    SignatureDocument, 
    HistoriqueDocument, 
    EtapeDossier
)
# Register your models here.

admin.site.register(Client)
admin.site.register(CategorieDocument)
admin.site.register(Dossier)
admin.site.register(Document)
admin.site.register(SignatureDocument)
admin.site.register(HistoriqueDocument)
admin.site.register(EtapeDossier)
