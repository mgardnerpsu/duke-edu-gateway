from django.shortcuts import render
from rest_framework import mixins, viewsets, serializers, status 
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from edugway.authors.models import Author
from edugway.authors.serializers import AuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
	'''
	Authors resourse actions.
	'''
	queryset = Author.objects.all()
	serializer_class = AuthorSerializer
