from .models import (
    Client, 
    Dossier, 
    CategorieDocument, 
    Document, 
    SignatureDocument,
    HistoriqueDocument, 
    EtapeDossier
)
from rest_framework import serializers
from account.models import Utilisateur

class ClientSerializer(serializers.ModelSerializer):

    utilisateur = serializers.PrimaryKeyRelatedField(
        queryset = Utilisateur.object.all(),
        required = True
    )

    class Meta:
        model = Client
        fields = [
            'type_client', 'statut', 'reference_client',
            # Personne Physique
            'nom', 'prenoms', 'date_naissance', 'lieu_naissance',
            # Personne Morale
            'raison_sociale', 'forme_juridique', 'numero_rccm',
            'numero_cc', 'capital_social',
            #Coordonnées
            'adresse', 'ville', 'commune', 'telephone_1',
            'telephone_2', 'email',
            # Informations juridiques complémentaires 
            'representant_legal_nom', 'representant_legal_fonction',
            #Gestionnaire administrative
            'date_de_creation','date_de_modification',
        ]