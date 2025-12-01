# Exemple d'APIView pour les documents
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from ..models import Document
from ..serializers import DocumentListSerializer, DocumentCreateSerializer

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
            documents = serializer.save()                    # ← documents = liste maintenant
            return Response({
                'message': f'{len(documents)} document(s) créé(s) avec succès',
                'documents': DocumentListSerializer(documents, many=True).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)