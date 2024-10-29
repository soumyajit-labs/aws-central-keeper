from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .serializers import UserSerializer, SecretsSerializer, TransalationRequestSerializer
from .services import yamlparser, aws

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class TranslateRAML(generics.ListCreateAPIView):
    serializer_class = TransalationRequestSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resp = self.perform_create(serializer)
        return Response(resp)
    
    def perform_create(self, serializer):
        request = serializer.data
        response = yamlparser.parser(key=request.get('key'), 
                                     ops=request.get('operation'), 
                                     text=request.get('text'))
        return response

class AWSSecrets(generics.ListCreateAPIView):
    serializer_class = SecretsSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        search = self.request.GET.get('name')
        return Response(aws.fetch(key=search))
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resp = self.perform_create(serializer)
        return Response(resp)
    
    def perform_create(self, serializer):
        request = serializer.data
        response = aws.upsert(key=request.get('name'), val=request.get('value'))
        return response