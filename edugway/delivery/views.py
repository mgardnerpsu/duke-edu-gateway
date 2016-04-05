from django.shortcuts import render
from edugway import settings
from rest_framework import mixins, viewsets, serializers, status 
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from edugway.content.models import Course, PubCourse
from edugway.delivery.serializers import CourseSerializer

class SearchCourseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    Search published courses - only search the current course version.
    '''
    queryset = PubCourse.objects.filter(is_current_version=True)
    serializer_class = CourseSerializer

class CourseViewSet(viewsets.GenericViewSet):
    '''
    Search published courses - only search the current course version.
    '''
    queryset = PubCourse.objects.all()
    serializer_class = CourseSerializer
