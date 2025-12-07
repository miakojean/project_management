# Exemple d'APIView pour les documents
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from ..models import Document
from manager.serializer.documentSerializer import (
    DocumentDownloadSerializer,
    DocumentDownloadRequestSerializer,
    MultipleDocumentDownloadSerializer,
)
from manager.serializers import (
    DocumentListSerializer,
    DocumentCreateSerializer
)
import os
import zipfile
import io
import json
from tempfile import NamedTemporaryFile
from django.http import FileResponse, HttpResponse
from django.utils import timezone

class DocumentsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        documents = Document.objects.all()
        serializer = DocumentListSerializer(documents, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DocumentCreateSerializer( 
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            documents = serializer.save()  # Liste de 1 ou N documents
            return Response({
                'message': f'{len(documents)} document(s) créé(s) avec succès',
                'documents': DocumentListSerializer(documents, many=True).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# documents_views.py - AJOUTEZ CETTE CLASSE
class DocumentDirectDownloadAPIView(APIView):
    """Vue pour téléchargement DIRECT du fichier avec GET"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, document_id):
        try:
            document = Document.objects.get(id=document_id)
            
            # Vérifier les permissions
            if not self._can_download(request.user, document):
                return Response(
                    {'error': 'Permission insuffisante'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Vérifier si le fichier existe
            if not document.fichier:
                return Response(
                    {'error': 'Fichier non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Enregistrer la consultation
            document.enregistrer_consultation()
            
            # Télécharger le fichier
            response = FileResponse(
                document.fichier.open('rb'),
                as_attachment=True,
                filename=self._get_download_filename(document)
            )
            
            # Définir le Content-Type
            response['Content-Type'] = self._get_content_type(document.extension)
            
            return response
            
        except Document.DoesNotExist:
            return Response(
                {'error': 'Document non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def _can_download(self, user, document):
        """Vérifie si l'utilisateur peut télécharger le document"""
        if document.niveau_confidentialite == 'PUBLIC':
            return True
        elif document.niveau_confidentialite == 'INTERNE':
            return user.is_authenticated
        elif document.niveau_confidentialite == 'CONFIDENTIEL':
            return user.has_perm('documents.view_confidential_documents')
        elif document.niveau_confidentialite == 'TRES_CONFIDENTIEL':
            return user.has_perm('documents.view_confidential_documents') and user.is_staff
        return False
    
    def _get_download_filename(self, document):
        """Génère un nom de fichier pour le téléchargement"""
        # Utiliser le titre ou la référence
        base_name = document.titre or document.reference
        # Nettoyer le nom
        safe_name = "".join(c for c in base_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        return f"{safe_name}.{document.extension}"
    
    def _get_content_type(self, extension):
        """Retourne le Content-Type approprié"""
        content_types = {
            'pdf': 'application/pdf',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'zip': 'application/zip',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'xls': 'application/vnd.ms-excel',
        }
        return content_types.get(extension.lower(), 'application/octet-stream')
    
class DocumentDownloadAPIView(APIView):
    """API pour télécharger un document"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, document_id=None):
        """Obtenir les informations de téléchargement"""
        if document_id:
            try:
                document = Document.objects.get(id=document_id)
                serializer = DocumentDownloadSerializer(
                    document,
                    context={'request': request}
                )
                return Response(serializer.data)
            except Document.DoesNotExist:
                return Response(
                    {'error': 'Document non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Lister les documents téléchargeables
            documents = Document.objects.filter(
                niveau_confidentialite__in=self._get_allowed_confidentiality(request.user)
            ).exclude(statut='BROUILLON')
            
            serializer = DocumentDownloadSerializer(
                documents,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data)
    
    def post(self, request):
        """Télécharger un document avec options"""
        serializer = DocumentDownloadRequestSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            document = serializer.validated_data.get('document')
            format_type = serializer.validated_data.get('format', 'original')
            inclure_metadata = serializer.validated_data.get('inclure_metadata', False)
            
            # Enregistrer dans l'historique
            self._enregistrer_telechargement(request, document, format_type)
            
            # Mettre à jour le compteur de consultations
            document.enregistrer_consultation()
            
            # Préparer la réponse
            if format_type == 'original':
                return self._telecharger_original(document, inclure_metadata)
            elif format_type == 'pdf':
                return self._telecharger_pdf(document, inclure_metadata)
            elif format_type == 'zip':
                return self._telecharger_zip([document], inclure_metadata)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_allowed_confidentiality(self, user):
        """Détermine les niveaux de confidentialité autorisés"""
        if user.has_perm('documents.view_confidential_documents') and user.is_staff:
            return ['PUBLIC', 'INTERNE', 'CONFIDENTIEL', 'TRES_CONFIDENTIEL']
        elif user.has_perm('documents.view_confidential_documents'):
            return ['PUBLIC', 'INTERNE', 'CONFIDENTIEL']
        elif user.is_authenticated:
            return ['PUBLIC', 'INTERNE']
        else:
            return ['PUBLIC']
    
    def _telecharger_original(self, document, inclure_metadata=False):
        """Télécharger le fichier original"""
        if inclure_metadata:
            # Créer une archive ZIP avec le fichier et les métadonnées
            return self._creer_archive_avec_metadata([document])
        
        response = FileResponse(
            document.fichier.open('rb'),
            as_attachment=True,
            filename=os.path.basename(document.fichier.name)
        )
        return response
    
    def _telecharger_pdf(self, document, inclure_metadata=False):
        """Télécharger en PDF (conversion si nécessaire)"""
        # TODO: Implémenter la conversion en PDF si possible
        # Pour l'instant, on retourne l'original
        return self._telecharger_original(document, inclure_metadata)
    
    def _telecharger_zip(self, documents, inclure_metadata=False):
        """Télécharger une archive ZIP"""
        return self._creer_archive_avec_metadata(documents)
    
    def _creer_archive_avec_metadata(self, documents):
        """Crée une archive ZIP avec les fichiers et métadonnées"""
        # Créer un fichier ZIP en mémoire
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for document in documents:
                # Ajouter le fichier principal
                file_name = os.path.basename(document.fichier.name)
                with document.fichier.open('rb') as f:
                    zip_file.writestr(file_name, f.read())
                
                # Ajouter les métadonnées comme fichier JSON
                metadata = {
                    'reference': document.reference,
                    'titre': document.titre,
                    'description': document.description,
                    'categorie': str(document.categorie),
                    'statut': document.statut,
                    'date_document': str(document.date_document),
                    'date_validite': str(document.date_validite),
                    'emetteur': document.emetteur,
                    'destinataire': document.destinataire,
                    'date_upload': str(document.date_upload),
                    'taille': document.taille_lisible,
                }
                
                metadata_filename = f"{document.reference}_metadata.json"
                zip_file.writestr(
                    metadata_filename,
                    json.dumps(metadata, indent=2, ensure_ascii=False)
                )
        
        zip_buffer.seek(0)
        
        # Nom de l'archive
        if len(documents) == 1:
            archive_name = f"{documents[0].reference}.zip"
        else:
            archive_name = f"documents_{timezone.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{archive_name}"'
        response['Content-Length'] = zip_buffer.getbuffer().nbytes
        
        return response
    
    def _enregistrer_telechargement(self, request, document, format_type):
        """Enregistre le téléchargement dans l'historique"""
        # TODO: Implémenter un modèle d'historique si nécessaire
        # Pour l'instant, on pourrait utiliser les logs Django
        pass


class MultipleDocumentDownloadAPIView(APIView):
    """API pour télécharger plusieurs documents"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = MultipleDocumentDownloadSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            documents = serializer.validated_data['documents']
            format_type = serializer.validated_data.get('format', 'zip')
            
            # Enregistrer chaque téléchargement
            for document in documents:
                document.enregistrer_consultation()
            
            if format_type == 'zip':
                # Créer une archive ZIP
                return self._creer_archive_zip(documents)
            elif format_type == 'separate':
                # Retourner une réponse multipart
                return self._creer_reponse_multipart(documents)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _creer_archive_zip(self, documents):
        """Crée une archive ZIP avec plusieurs documents"""
        view = DocumentDownloadAPIView()
        return view._creer_archive_avec_metadata(documents)
    
    def _creer_reponse_multipart(self, documents):
        """Crée une réponse multipart (plusieurs fichiers)"""
        # Cette méthode est plus complexe et nécessite
        # une gestion spécifique des boundary multipart
        # Pour simplifier, on utilise ZIP pour l'instant
        return self._creer_archive_zip(documents)


class DocumentPreviewAPIView(APIView):
    """API pour prévisualiser un document (sans téléchargement)"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, document_id):
        """Prévisualiser le document dans le navigateur"""
        try:
            document = Document.objects.get(id=document_id)
            
            # Vérifier les permissions
            user = request.user
            if document.niveau_confidentialite == 'CONFIDENTIEL':
                if not user.has_perm('documents.view_confidential_documents'):
                    return Response(
                        {'error': 'Permission insuffisante'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            elif document.niveau_confidentialite == 'TRES_CONFIDENTIEL':
                if not (user.has_perm('documents.view_confidential_documents') and user.is_staff):
                    return Response(
                        {'error': 'Permission insuffisante'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            
            # Vérifier si le format est prévisualisable
            previewable_formats = ['pdf', 'jpg', 'jpeg', 'png']
            if document.extension.lower() not in previewable_formats:
                return Response({
                    'message': 'Prévisualisation non disponible pour ce format',
                    'download_url': f'/api/documents/{document_id}/download/'
                })
            
            # Enregistrer la consultation
            document.enregistrer_consultation()
            
            # Retourner le fichier pour prévisualisation
            response = FileResponse(
                document.fichier.open('rb'),
                content_type=self._get_content_type(document.extension)
            )
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(document.fichier.name)}"'
            return response
            
        except Document.DoesNotExist:
            return Response(
                {'error': 'Document non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def _get_content_type(self, extension):
        """Retourne le Content-Type approprié"""
        content_types = {
            'pdf': 'application/pdf',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
        }
        return content_types.get(extension.lower(), 'application/octet-stream')