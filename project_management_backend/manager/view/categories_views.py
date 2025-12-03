from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from ..models import CategorieDocument
from ..serializers import CategorieDocumentCreateSerializer

class CategoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        category = CategorieDocument.objects.all()
        serializer = CategorieDocumentCreateSerializer(category, many=True)
        return Response(serializer.data)