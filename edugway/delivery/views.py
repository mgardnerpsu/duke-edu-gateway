from django.shortcuts import render
from edugway import settings
from rest_framework import mixins, viewsets, serializers, status 
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from edugway.content.models import Course
from edugway.content.serializers import CourseSerializer

class CourseViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, 
            viewsets.GenericViewSet):
    '''
    Course resourse actions.
    '''
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # DEPRECATED - only support a single author for alpha.
    # @detail_route(methods=['POST', 'GET'])
    # def authors(self, request, pk=None):
    #     if request.method == 'POST':
    #         course = self.get_object()
    #         course.course_authors.all().delete()
    #         request.data['course_id'] = course.id
    #         serializer = CourseAuthorSerializer(data=request.data, many=False, 
    #             context={'request': request})
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     if request.method == 'GET':
    #         course = self.get_object()
    #         course_authors = course.course_authors.all()
    #         serializer = CourseAuthorSerializer(course_authors, many=True, 
    #             context={'request': request})
    #         return Response(serializer.data, status=status.HTTP_200_OK)
