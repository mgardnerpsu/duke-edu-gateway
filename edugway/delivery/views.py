from django.shortcuts import render
from edugway import settings
from rest_framework import mixins, viewsets, serializers, status 
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from edugway.content.models import Course, PubCourse
from edugway.delivery.serializers import CourseSerializer

class CourseViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, 
            viewsets.GenericViewSet):
    '''
    Course resourse actions.
    '''
    queryset = Course.objects.filter(pub_courses__is_current_version=True)
    serializer_class = CourseSerializer
