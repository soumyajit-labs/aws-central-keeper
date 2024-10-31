from django.urls import path
from . import views

urlpatterns = [
    path('secrets/translate/raml/', views.TranslateRAML.as_view()),
    path('aws/secrets/fetch/', views.AWSSecrets.as_view()),
    path('aws/secrets/upsert/', views.AWSSecrets.as_view()),
    path('git/retrigger/', views.RetriggerGithubBuild.as_view()),
]