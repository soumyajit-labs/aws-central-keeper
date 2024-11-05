from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .jwtAuthClass import IsAuthenticatedUser

from .serializers import SecretsSerializer, TransalationRequestSerializer, GithubRetriggerAction
from .services import yamlparser, aws, github
from .jwtAuthValidator import userNameSetter

# Create your views here.
class TranslateRAML(generics.ListCreateAPIView):
    serializer_class = TransalationRequestSerializer
    permission_classes = [IsAuthenticatedUser]
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
    permission_classes = [IsAuthenticatedUser]
    def get(self, request, *args, **kwargs):
        search = self.request.GET.get('name')
        return Response(aws.fetch(key=search))
    
    def create(self, request, *args, **kwargs):
        user = userNameSetter(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resp = self.perform_create(serializer,user)
        return Response(resp)
    
    def perform_create(self, serializer, *args):
        request = serializer.data
        response = aws.upsert(key=request.get('name'), val=request.get('value'), user=args[0])
        return response
    
class RetriggerGithubBuild(generics.ListCreateAPIView):
    serializer_class = GithubRetriggerAction
    permission_classes = [IsAuthenticatedUser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resp = self.perform_create(serializer)
        return Response(resp)
    
    def perform_create(self, serializer):
        request = serializer.data
        response = github.workflow_retrigger(buildArg=request.get('event'), repository=request.get('repository'))
        return response