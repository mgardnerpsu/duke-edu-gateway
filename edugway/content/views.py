from django.shortcuts import render
from edugway import settings
from rest_framework import mixins, viewsets, serializers, status 
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from edugway.content.models import Category, Credit
from edugway.content.serializers import CategorySerializer, CreditSerializer

class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, 
			viewsets.GenericViewSet):
    '''
    Category resourse actions.
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CreditViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, 
			viewsets.GenericViewSet):
    '''
    Credit resourse actions.
    '''
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer
